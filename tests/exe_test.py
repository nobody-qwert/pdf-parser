import subprocess
from pathlib import Path


def run_extraction(input_folder: str, output_subfolder: str = "text"):
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder

    if not input_path.exists():
        print(f"Error: Directory '{input_folder}' does not exist.")
        return

    command = [
        "../build_executable/dist/pdf-parser.exe",
        "--directory", str(input_path),
        "--output", str(output_path)
    ]

    execute_command(command)


def run_single_file_extraction(pdf_file: str, output_folder: str = "text"):
    pdf_path = Path(pdf_file)
    output_path = Path(output_folder)

    if not pdf_path.exists():
        print(f"Error: File '{pdf_file}' does not exist.")
        return

    command = [
        "../build_executable/dist/pdf-parser.exe",
        "--file", str(pdf_path),
        "--output", str(output_path)
    ]

    execute_command(command)


def execute_command(command):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in iter(process.stdout.readline, ''):
            print(line.strip())

        process.wait()

        if process.returncode != 0:
            stderr_output = process.stderr.read().strip()
            print(f"Execution failed with error:\n{stderr_output}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def test_folder_extraction():
    input_folder = "test_docs"
    run_extraction(input_folder)


def test_file_extraction():
    pdf_file = "test_docs/fiba.pdf"
    run_single_file_extraction(pdf_file)


def run_without_params():
    command = ["../build_executable/dist/pdf-parser.exe",]
    execute_command(command)


if __name__ == "__main__":
    print("\nRunning test without params:")
    run_without_params()

    print("\nRunning file extraction test:")
    test_file_extraction()

    print("\nRunning folder extraction test:")
    test_folder_extraction()
