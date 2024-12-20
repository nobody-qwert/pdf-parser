import subprocess
from pathlib import Path


def run_extraction(input_folder: str, output_subfolder: str = "text"):
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder

    if not input_path.exists():
        print(f"Error: Directory '{input_folder}' does not exist.")
        return

    command = [
        "python", "pdf_parser_cli.py",
        "--directory", str(input_path),
        "--output", str(output_path)
    ]

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in iter(process.stdout.readline, ''):
            print(line.strip())

        process.stdout.close()
        process.wait()

    except subprocess.CalledProcessError as e:
        print(f"Extraction failed: {e.stderr}")


if __name__ == "__main__":
    input_folder = "test_docs"
    run_extraction(input_folder)
