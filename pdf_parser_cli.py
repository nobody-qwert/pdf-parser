import argparse
import logging
from pathlib import Path
from typing import Union, List, Dict, Optional
from datetime import datetime
import fitz
from dataclasses import dataclass
import json


def get_module_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

@dataclass
class ExtractionResult:
    filename: str
    text: str
    page_count: int
    output_path: Optional[str] = None
    error: str = None
    extraction_time: float = 0.0


class PDFTextExtractor:
    def __init__(self, max_workers: int = 4, output_dir: Union[str, Path] = "extracted_text"):
        self.max_workers = max_workers
        self.output_dir = Path(output_dir)
        self.logger = get_module_logger("pdf_extraction")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_text_to_file(self, text: str, pdf_path: Path) -> Path:
        output_filename = pdf_path.stem + "_pdf.txt"
        output_path = self.output_dir / output_filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"Saved extracted text to {output_path}", flush=True)
            return output_path
        except Exception as e:
            print(f"Error saving text file {output_path}: {str(e)}", flush=True)
            raise

    def extract_from_file(self, pdf_path: Union[str, Path]) -> ExtractionResult:
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

    def extract_from_directory(self, directory: Union[str, Path], recursive: bool = False) -> List[ExtractionResult]:
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


    def get_extraction_summary(self, results: List[ExtractionResult]) -> Dict:
        successful = [r for r in results if not r.error]
        failed = [r for r in results if r.error]

        summary = {
            "total_files": len(results),
            "successful_extractions": len(successful),
            "failed_extractions": len(failed),
            "total_pages_processed": sum(r.page_count for r in successful),
            "total_processing_time": sum(r.extraction_time for r in results),
            "output_directory": str(self.output_dir),
            "extracted_files": [
                {"input": r.filename, "output": r.output_path} for r in successful
            ],
            "failed_files": [
                {"filename": r.filename, "error": r.error} for r in failed
            ]
        }
        return summary


def main():
    parser = argparse.ArgumentParser(description="PDF Text Extraction Tool")
    parser.add_argument("--file", type=str, help="Path to the PDF file to extract")
    parser.add_argument("--directory", type=str, help="Directory containing PDF files")
    parser.add_argument("--recursive", action='store_true', help="Process files in subdirectories")
    parser.add_argument("--output", type=str, default="extracted_text", help="Output directory")
    parser.add_argument("--json", action='store_true', help="Return results as JSON")

    args = parser.parse_args()

    if args.directory and not Path(args.directory).exists():
        print(f"Error: Directory '{args.directory}' does not exist.")
        return

    results = []
    if args.file:
        extractor = PDFTextExtractor(output_dir=args.output)
        result = extractor.extract_from_file(args.file)
        results.append(result)
    elif args.directory:
        extractor = PDFTextExtractor(output_dir=args.output)
        results = extractor.extract_from_directory(args.directory, args.recursive)
    else:
        print("Error: Specify either --file or --directory")
        return

    if not results:
        return

    summary = extractor.get_extraction_summary(results)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Processed {summary['total_files']} files.")
        print(f"Successful extractions: {summary['successful_extractions']}")
        print(f"Failed extractions: {summary['failed_extractions']}")
        print(f"Output directory: {summary['output_directory']}")


if __name__ == "__main__":
    main()
