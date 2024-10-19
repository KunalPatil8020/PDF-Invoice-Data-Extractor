# PDF Invoice Data Extractor

This project extracts structured data (such as invoice numbers, customer details, total amounts, and item details) from PDF invoices using a combination of `pdfplumber` for text-based PDFs and `pytesseract` for scanned or image-based PDFs. The extracted data is saved to a CSV file along with performance metrics (processing time, memory usage, and CPU utilization).

## Features
- Extract text from PDFs using `pdfplumber` (text-based PDFs) and `pytesseract` (image-based PDFs).
- Preprocesses scanned PDFs to improve OCR accuracy.
- Extract key invoice details like Invoice Number, Date, Customer Name, Items, and Amount.
- Generates CSV files for extracted data and performance metrics.

## Documentation and Reports:
All detailed reports and documentation, including the Technical Documentation, Accuracy and Trust Assessment Report, and Performance Analysis are available at the following link:
[Link Text](https://drive.google.com/drive/folders/1cu1Gr1HbtxWsipZWwOyacuVhLVuwG3A_?usp=sharing)


## Installation

#### 1. Clone the repository:
```bash
git clone https://github.com/your-repo/pdf-invoice-extractor.git
cd pdf-invoice-extractor
```


#### 2. Set up a Python virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

#### 3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Script
Command Line Usage:

Run the script by providing the folder containing the PDF files:
```bash
python main.py <path_to_pdf_folder>
```
<path_to_pdf_folder>: Path to the folder containing the PDF invoices.

## Project Structure
```bash
.
├── extractor.py          # Core functions for extracting data from PDFs
├── utils.py              # Helper functions for preprocessing and performance tracking
├── main.py               # Main entry point for running the script
├── requirements.txt      # Python dependencies
```
