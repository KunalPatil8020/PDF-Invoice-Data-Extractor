import os
import pandas as pd
from extractor import extract_with_pdfplumber, extract_with_pytesseract, extract_invoice_data
from utils import track_performance, report_performance
import argparse


def process_pdfs(pdf_folder, output_csv_path, performance_report_csv):
    extracted_data_list = []
    performance_metrics = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            print(f"Processing {filename}...")
            pdf_path = os.path.join(pdf_folder, filename)

            start_time, initial_memory, initial_cpu = track_performance()
            
            extracted_text = extract_with_pdfplumber(pdf_path)
            if not extracted_text.strip():
                extracted_text = extract_with_pytesseract(pdf_path)

            processing_duration, memory_used, cpu_used = report_performance(start_time, initial_memory, initial_cpu)
            
            if extracted_text.strip():
                invoice_data = extract_invoice_data(extracted_text)
                extracted_data_list.append(invoice_data)
            else:
                extracted_data_list.append({"Error": f"No text could be extracted from {pdf_path}"})

            performance_metrics.append({
                "Filename": filename,
                "Processing Time (s)": processing_duration,
                "Memory Used (MB)": memory_used / (1024 * 1024),
                "CPU Utilization (%)": cpu_used
            })

    # Save extracted data to CSV
    df = pd.DataFrame(extracted_data_list)
    df.to_csv(output_csv_path, index=False)
    print(f"Extracted data saved to {output_csv_path}")

    # Save performance metrics to CSV
    df_performance = pd.DataFrame(performance_metrics)
    df_performance.to_csv(performance_report_csv, index=False)
    print(f"Performance report saved to {performance_report_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process PDF invoices from a folder.')
    parser.add_argument('pdf_folder', type=str, help='Folder containing PDF files')
    
    args = parser.parse_args()
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Output CSV paths (stored in the same directory as main.py)
    output_csv_path = os.path.join(current_dir, "extracted_data.csv")
    performance_report_csv = os.path.join(current_dir, "performance_report.csv")
    
    # Process PDFs and generate reports
    process_pdfs(args.pdf_folder, output_csv_path, performance_report_csv)