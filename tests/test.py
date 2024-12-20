import subprocess
from pathlib import Path


import subprocess
from pathlib import Path


def run_extraction(input_folder: str, output_subfolder: str = "text"):
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder

    if not input_path.exists():
        print(f"Error: Directory '{input_folder}' does not exist.")
        return

    command = [
        "python", "../pdf_parser_cli.py",
        "--directory", str(input_path),
        "--output", str(output_path)
    ]

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in iter(process.stdout.readline, ''):
            print(line.strip())

        process.wait()

        if process.returncode != 0:
            stderr_output = process.stderr.read().strip()
            print(f"Extraction failed with error:\n{stderr_output}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def run_single_file_extraction(pdf_file: str, output_folder: str = "text"):
    pdf_path = Path(pdf_file)
    output_path = Path(output_folder)

    if not pdf_path.exists():
        print(f"Error: File '{pdf_file}' does not exist.")
        return

    command = [
        "python", "../pdf_parser_cli.py",
        "--file", str(pdf_path),
        "--output", str(output_path)
    ]

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in iter(process.stdout.readline, ''):
            print(line.strip())

        process.wait()

        if process.returncode != 0:
            stderr_output = process.stderr.read().strip()
            print(f"Extraction failed with error:\n{stderr_output}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def test_folder_extraction():
    input_folder = "test_docs"
    run_extraction(input_folder)


def test_file_extraction():
    pdf_file = "test_docs/fiba.pdf"
    run_single_file_extraction(pdf_file)


if __name__ == "__main__":
    test_file_extraction()
    test_folder_extraction()


