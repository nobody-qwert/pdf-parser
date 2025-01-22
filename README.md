# PDF Text Extractor CLI

A powerful command-line tool for extracting text from PDF files using Python. It supports single-file extraction, batch processing from directories, and recursive searches through subdirectories. Extracted text files are saved in a specified output directory, with detailed logs and summaries.

---

## **Features**

- 🗂 **Single or Batch Extraction**: Extract text from a single file or an entire directory of PDFs.

---

## **How to Use**

### **Extract a Single File:**
```bash
python pdf_parser_cli.py example.pdf out.txt
```

### **Extract All PDFs in a Directory:**

```bash
python pdf_parser_cli.py my_pdfs out_dir
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
python pdf_parser_cli.py
```
