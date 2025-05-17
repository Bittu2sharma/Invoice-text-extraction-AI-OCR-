import streamlit as st
import pytesseract
from PIL import Image
import io
import requests
import os
import pdfplumber
from pdf2image import convert_from_bytes
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Extract text
def extract_text_from_pdf(file):
    file.seek(0)
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass

    if not text.strip():
        file.seek(0)
        images = convert_from_bytes(file.read(), dpi=300)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return text.strip()

# Mistral via Groq
def extract_invoice_info_with_mistral(ocr_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert invoice parser. Extract the following fields from the invoice text below and return them in JSON format:

- Invoice Number
- Invoice Date
- Vendor Name
- Vendor Tax ID
- Total Amount
- Tax Amount
- Currency (if available)

Return only JSON (no explanation).

Invoice Text:
\"\"\"
{ocr_text}
\"\"\"
"""

    data = {
        "model": "llama3-8b-8192",  # Use available Groq model
        "messages": [
            {"role": "system", "content": "You are a helpful AI that extracts structured data from invoices."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content']
        except:
            return "❌ Failed to parse Mistral response."
    else:
        return f"❌ API Error {response.status_code}: {response.text}"

# Streamlit UI
st.set_page_config(page_title="📄 Invoice Extractor", layout="centered")
st.title("📄 Invoice Uploader & Extractor")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    with st.spinner("🔍 Performing OCR..."):
        if uploaded_file.name.lower().endswith(".pdf"):
            ocr_text = extract_text_from_pdf(uploaded_file)
        else:
            img = Image.open(uploaded_file).convert("RGB")
            ocr_text = pytesseract.image_to_string(img)

    st.subheader("📄 OCR Extracted Text:")
    st.text_area("Raw Invoice Text", ocr_text, height=200)

    if ocr_text:
        with st.spinner("🤖 Extracting structured info with Mistral..."):
            extracted_json = extract_invoice_info_with_mistral(ocr_text)

        st.subheader("📦 Extracted Invoice Data (JSON):")
        st.code(extracted_json, language="json")
else:
    st.info("Please upload an invoice to begin.")
