# Invoice Text Extraction and Data Structuring App

This Streamlit application allows users to upload invoices in PDF or image format and extracts the text using OCR. It then uses a large language model (Mistral via Groq API) to extract structured information like invoice number, date, vendor name, total amount, tax, and currency in JSON format.

## Features

- Upload invoices in PDF, JPG, JPEG, or PNG format
- Extract text from:
  - Text-based PDFs using `pdfplumber`
  - Image-based PDFs and images using `pytesseract` OCR
- Call the Groq API with a Mistral model to extract structured invoice data in JSON
- Display raw OCR text and extracted invoice fields

## Tech Stack

- Python
- Streamlit
- pdfplumber
- pytesseract
- Groq API (Mistral models)

## Setup Instructions

1. **Clone the repository:**

   Install dependencies:

Make sure you're using Python 3.9 or newer. Then run:

bash
Copy
Edit
pip install -r requirements.txt
Install system dependencies (for local development only):

Install Tesseract OCR:

Ubuntu: sudo apt install tesseract-ocr

Mac: brew install tesseract

Windows: Download from official repo

For PDF to image conversion, install poppler:

Ubuntu: sudo apt install poppler-utils

Mac: brew install poppler

Set up environment variables:

Create a .env file in the root directory and add your Groq API key:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key_here
Run the app:

bash
Copy
Edit
streamlit run app.py
Deploying to Streamlit Cloud
To deploy on Streamlit Community Cloud:

Push the code and requirements to a GitHub repository.

Make sure .env variables are added in the Streamlit Cloud dashboard as secrets.

Ensure that requirements.txt does not include system-level dependencies like poppler or tesseract (as Streamlit Cloud has limited OS access).

File Structure
bash
Copy
Edit
invoice-text-extraction/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (not to be committed)
Example Output
Raw extracted OCR text is shown on the interface.

Structured invoice fields are displayed in JSON format.

Notes
If the PDF is entirely image-based, OCR accuracy may vary.

LlaMa model is accessed through Groq API using llama3-8b-8192.

This app is suitable for prototyping or demonstration purposes and may require further validation for production use.
   
