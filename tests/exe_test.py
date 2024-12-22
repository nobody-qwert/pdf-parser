import os.path
import subprocess


def execute_command(command):
    print(f"------------{command}-------------------")

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


def test_1():
    input_folder = "test_docs"
    pdf_file = "test_docs/fiba.pdf"
    output_folder = "test_docs/text"
    output_txt_file = os.path.join(output_folder, "extracted.txt")

    exe_path = "../build_executable/dist/pdf-parser.exe"
    execute_command([exe_path])
    execute_command([exe_path, "aa", "bb", "ccccc"])
    execute_command([exe_path, input_folder, output_folder])
    execute_command([exe_path, pdf_file, output_txt_file])


if __name__ == "__main__":
    test_1()



