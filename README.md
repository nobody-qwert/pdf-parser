# PDF Text Extractor CLI

A powerful command-line tool for extracting text from PDF files using Python. It supports single-file extraction, batch processing from directories, and recursive searches through subdirectories. Extracted text files are saved in a specified output directory, with detailed logs and summaries.

---

## **Features**

- 🗂 **Single or Batch Extraction**: Extract text from a single file or an entire directory of PDFs.
- 🔍 **Recursive Search**: Process files in subdirectories with the `--recursive` flag.
- 📊 **Extraction Summary**: Receive comprehensive reports, including success and failure statistics.
- 🖨 **JSON Output**: Print results in JSON format for easy integration into other tools or scripts.
- 🚀 **Multithreading**: Fast processing with support for multiple threads.

---

## **How to Use**

### **Extract a Single File:**
```bash
python pdf_parser_cli.py --file example.pdf --json
```

### **Extract All PDFs in a Directory:**

```bash
python pdf_parser_cli.py --directory my_pdfs --recursive
```

### **Customize Output Directory:**

```bash
python pdf_parser_cli.py --file example.pdf --output output_folder
```

## **Installation**

### **Clone the repository:**

```bash
https://github.com/lazloalexandru/pdf-parser.git
cd pdf-parser
```

### **Create a Virtual Environment**

In your project directory, create a virtual environment to isolate your project dependencies:
```bash
python -m venv .venv
```

### **Activate the Virtual Environment**

To activate the virtual environment, run:
```bash
.venv\Scripts\activate
```

Once activated, you should see the environment name (e.g., .venv) in your command prompt.

### **Install dependencies:**

```bash
pip install -r requirements.txt
```

### **Run the tool:**

```bash
python pdf_parser_cli.py --help
```

# TODO
- test recursive
