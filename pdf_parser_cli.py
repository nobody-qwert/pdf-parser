import os
import sys
from pathlib import Path
from datetime import datetime
import fitz

MAX_FILE_SIZE_BYTES = 1024 * 1024 * 1024
MAX_FILE_SIZE_MB = int(MAX_FILE_SIZE_BYTES / (1024 * 1024))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def display_help(script_name):
    t = f"""******************************************
** \\                                   /**
**  *    PDF Text Extraction Tool     * **
** /                                   \\**
******************************************

Usage:
{script_name} <PDF_file_path|Input_Directory> <Output>

Examples:
{script_name} sample.pdf out.txt
{script_name} sample_pdfs out_dir

Max PDF size: {MAX_FILE_SIZE_MB} MB
"""
    print(t)


def save_text_to_file(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved extracted text to {output_path}")
    return str(output_path)


def extract_pdf(pdf_path, output_path):
    start = datetime.now()
    try:
        p = Path(pdf_path)
        if not p.exists():
            return dict(filename=p.name, text="", page_count=0, error="File not found", extraction_time=0)
        if p.suffix.lower() != ".pdf":
            return dict(filename=p.name, text="", page_count=0, error="Not a PDF file", extraction_time=0)
        if p.stat().st_size > MAX_FILE_SIZE_BYTES:
            return dict(filename=p.name, text="", page_count=0, error="File size too large", extraction_time=0)
        doc = fitz.open(p)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        out_path = save_text_to_file(text, output_path)
        return dict(
            filename=p.name,
            text=text,
            page_count=len(text.split("\n")) if text else 0,
            error=None,
            output_path=out_path,
            extraction_time=(datetime.now() - start).total_seconds()
        )
    except Exception as e:
        return dict(filename=str(pdf_path), text="", page_count=0, error=str(e), extraction_time=0)


def extract_directory(input_dir, output_dir):
    d = Path(input_dir)
    pdf_files = list(d.glob("*.pdf"))
    results = []
    for pdf_file in pdf_files:
        if pdf_file.stat().st_size > MAX_FILE_SIZE_BYTES:
            results.append(dict(filename=pdf_file.name, text="", page_count=0, error="File size too large", extraction_time=0))
            continue
        out_name = pdf_file.stem + "_pdf.txt"
        out_path = Path(output_dir) / out_name
        r = extract_pdf(pdf_file, out_path)
        results.append(r)
    return results


def get_summary(results):
    ok = [r for r in results if not r.get("error")]
    bad = [r for r in results if r.get("error")]
    return dict(
        total_files=len(results),
        successful=len(ok),
        failed=len(bad),
        total_pages=sum(r.get("page_count", 0) for r in ok),
        total_time=sum(r.get("extraction_time", 0) for r in results)
    )


def main():
    if len(sys.argv) != 3:
        display_help(os.path.basename(sys.argv[0]))
        return
    inp = Path(sys.argv[1])
    outp = Path(sys.argv[2])
    if not inp.exists():
        print(f"Error: '{inp}' does not exist.")
        return
    results = []
    if inp.is_file():
        results.append(extract_pdf(inp, outp))
    elif inp.is_dir():
        results = extract_directory(inp, outp)
    else:
        print("Error: Not a valid file or directory.")
        return
    if not results:
        return
    s = get_summary(results)
    print(f"Processed {s['total_files']} files.")
    print(f"Successful extractions: {s['successful']}")
    print(f"Failed extractions: {s['failed']}")
    for r in results:
        if r.get("error"):
            print(r["filename"], "->", r["error"])


if __name__ == "__main__":
    main()
