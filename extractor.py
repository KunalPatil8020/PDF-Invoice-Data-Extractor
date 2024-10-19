import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from utils import preprocess_image


# Function to extract text using pdfplumber
def extract_with_pdfplumber(pdf_path):
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""
    except Exception as e:
        print(f"Error using pdfplumber: {e}")
    return extracted_text


# Function to extract text using pytesseract
def extract_with_pytesseract(pdf_path):
    extracted_text = ""
    try:
        images = convert_from_path(pdf_path)
        for image in images:
            preprocessed_image = preprocess_image(image)
            extracted_text += pytesseract.image_to_string(preprocessed_image)
    except Exception as e:
        print(f"Error using pytesseract OCR: {e}")
    return extracted_text


# Function to extract invoice items from the PDF text
def extract_invoice_items(text):
    pattern = r"(\d+)\s([A-Za-z\s\-]+)\s+\d+\s+[A-Za-z]+\s+[\d\.]+"
    items = re.findall(pattern, text)
    item_names = [item[1].strip() for item in items]
    return item_names if item_names else []


# Function to extract invoice data from the text
def extract_invoice_data(text):
    data = {}
    invoice_number_match = re.search(r'Invoice #:\s*(\S+)', text)
    data['Invoice Number'] = invoice_number_match.group(1) if invoice_number_match else "Not Found"
    invoice_date_match = re.search(r'Invoice Date:\s*(\d{1,2} \w{3} \d{4})', text)
    data['Invoice Date'] = invoice_date_match.group(1) if invoice_date_match else "Not Found"
    due_date_match = re.search(r'Due Date:\s*(\d{1,2} \w{3} \d{4})', text)
    data['Due Date'] = due_date_match.group(1) if due_date_match else "Not Found"
    customer_name_match = re.search(r'Customer Details:\s*([\w\s]+?)(?:Ph|Place of Supply)', text)
    data['Customer Name'] = customer_name_match.group(1).strip() if customer_name_match else "Not Found"
    phone_match = re.search(r'Ph:\s*(\d{10})', text)
    data['Phone Number'] = phone_match.group(1) if phone_match else "Not Found"
    place_of_supply_match = re.search(r'Place of Supply:\s*([\w\s\-]+)', text)
    data['Place of Supply'] = place_of_supply_match.group(1).strip() if place_of_supply_match else "Not Found"
    total_amount_match = re.search(r'Total\s*₹([\d,]+\.\d{2})', text)
    data['Total Amount'] = total_amount_match.group(1) if total_amount_match else "Not Found"
    total_discount_match = re.search(r'Total Discount\s*₹([\d,]+\.\d{2})', text)
    data['Total Discount'] = total_discount_match.group(1) if total_discount_match else "Not Found"
    cgst_match = re.search(r'CGST\s*\d+\.\d+%\s*₹([\d,]+\.\d{2})', text)
    sgst_match = re.search(r'SGST\s*\d+\.\d+%\s*₹([\d,]+\.\d{2})', text)
    data['CGST'] = cgst_match.group(1) if cgst_match else "Not Found"
    data['SGST'] = sgst_match.group(1) if sgst_match else "Not Found"
    item_names = extract_invoice_items(text)
    data['Items'] = ", ".join(item_names)
    bank_details_match = re.search(r'Bank:\s*(.+)\nAccount #:\s*(\d+)\nIFSC Code:\s*(\S+)', text)
    if bank_details_match:
        data['Bank Name'] = bank_details_match.group(1)
        data['Account Number'] = bank_details_match.group(2)
        data['IFSC Code'] = bank_details_match.group(3)
    else:
        data['Bank Details'] = "Not Found"
    return data