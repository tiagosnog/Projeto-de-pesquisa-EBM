#!/usr/bin/env python3
import fitz  # PyMuPDF
import sys
import os

def extract_pdf_text(pdf_path):
    """Extract text from PDF file using PyMuPDF"""
    try:
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return None

        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += f"--- Page {page_num + 1} ---\n"
            text += page.get_text() + "\n\n"
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_path = "docs/referencias/liu2000.pdf"
    print(f"Attempting to read PDF: {pdf_path}")
    print(f"File exists: {os.path.exists(pdf_path)}")

    text = extract_pdf_text(pdf_path)

    if text:
        # Save to text file for analysis
        try:
            with open("liu2000_extracted.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("Text file saved successfully!")
        except Exception as e:
            print(f"Error saving file: {e}")

        # Print first part to see content
        print("PDF text extracted successfully!")
        print("First 2000 characters:")
        print("=" * 50)
        print(text[:2000])
        print("=" * 50)
        print(f"Total length: {len(text)} characters")
        print("Full text saved to liu2000_extracted.txt")
    else:
        print("Failed to extract text from PDF")
