import logging
import os
import sys
from pathlib import Path
from datetime import datetime
import fitz


def get_module_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def display_help(run_command):
    help_text = f"""******************************************
** \                                   /**
**  *    PDF Text Extraction Tool     * **
** /                                   \**
******************************************

Usage:
{run_command} <PDF_file_path | Input_Directory> <Output_Directory>

Examples:
{run_command} sample.pdf extracted_docs
{run_command} sample_pdfs extracted_docs
"""
    print(help_text)


class ExtractionResult:
    def __init__(self, filename, text, page_count, output_path=None, error=None, extraction_time=0.0):
        self.filename = filename
        self.text = text
        self.page_count = page_count
        self.output_path = output_path
        self.error = error
        self.extraction_time = extraction_time


class PDFTextExtractor:
    def __init__(self, output_dir="extracted_text"):
        self.output_dir = Path(output_dir)
        self.logger = get_module_logger("pdf_extraction")

    def save_text_to_file(self, text, pdf_path):
        output_filename = pdf_path.stem + "_pdf.txt"
        output_path = self.output_dir / output_filename

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved extracted text to {output_path}", flush=True)
            return output_path
        except Exception as e:
            print(f"Error saving text file {output_path}: {str(e)}", flush=True)
            raise

    def extract_from_file(self, pdf_path):
        start_time = datetime.now()
        pdf_path = Path(pdf_path)

        try:
            if not pdf_path.exists():
                raise FileNotFoundError(f"File not found: {pdf_path}")

            if pdf_path.suffix.lower() != '.pdf':
                raise ValueError(f"Not a PDF file: {pdf_path}")

            with fitz.open(pdf_path) as doc:
                text_content = [page.get_text() for page in doc]
                full_text = "\n".join(text_content)
                output_path = self.save_text_to_file(full_text, pdf_path)
                result = ExtractionResult(
                    filename=pdf_path.name,
                    text=full_text,
                    page_count=len(doc),
                    output_path=str(output_path),
                    extraction_time=(datetime.now() - start_time).total_seconds()
                )
                print(f"[OK] Processed \"{pdf_path.name}\" -> {result.page_count} pages")
                return result
        except Exception as e:
            print(f"[ERROR] Failed to process {pdf_path.name}: {str(e)}")
            return ExtractionResult(
                filename=pdf_path.name,
                text="",
                page_count=0,
                error=str(e),
                extraction_time=(datetime.now() - start_time).total_seconds()
            )

    def extract_from_directory(self, directory, recursive=False):
        directory = Path(directory)
        if not directory.exists():
            raise NotADirectoryError(f"Directory not found: {directory}")

        pattern = '**/*.pdf' if recursive else '*.pdf'
        pdf_files = list(directory.glob(pattern))

        if not pdf_files:
            print(f"No PDF files found in {directory}")
            return []

        print(f"Found {len(pdf_files)} PDF files to process")

        results = []
        for pdf_file in pdf_files:
            result = self.extract_from_file(pdf_file)
            results.append(result)
        return results

    def get_extraction_summary(self, results):
        successful = [r for r in results if not r.error]
        failed = [r for r in results if r.error]

        summary = {
            "total_files": len(results),
            "successful_extractions": len(successful),
            "failed_extractions": len(failed),
            "total_pages_processed": sum(r.page_count for r in successful),
            "total_processing_time": sum(r.extraction_time for r in results),
            "output_directory": str(self.output_dir) if successful else None,
            "extracted_files": [
                {"input": r.filename, "output": r.output_path} for r in successful
            ],
            "failed_files": [
                {"filename": r.filename, "error": r.error} for r in failed
            ]
        }
        return summary


def main():
    if sys.argv[0].endswith('.exe'):
        run_command = os.path.basename(sys.argv[0])

        if len(sys.argv) != 3:
            display_help(run_command)
            return
    else:
        run_command = "python.exe " + sys.argv[0]

        if len(sys.argv) != 3:
            display_help(run_command)
            return

    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: Path '{input_path}' does not exist.")
        return

    results = []
    extractor = PDFTextExtractor(output_dir=output_dir)

    if input_path.is_file():
        results.append(extractor.extract_from_file(input_path))
    elif input_path.is_dir():
        results = extractor.extract_from_directory(input_path)
    else:
        print("Error: Specify a valid file or directory")
        return

    if not results:
        return

    summary = extractor.get_extraction_summary(results)

    print(f"Processed {summary['total_files']} files.")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"Failed extractions: {summary['failed_extractions']}")
    if summary['output_directory']:
        print(f"Output directory: {summary['output_directory']}")


if __name__ == "__main__":
    main()
