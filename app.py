import streamlit as st
import pytesseract
from PIL import Image
import io
import requests
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# OCR Function
def extract_text_from_file(file):
    ext = file.name.split('.')[-1].lower()
    
    if ext in ['jpg', 'jpeg', 'png']:
        image = Image.open(file).convert("RGB")
        text = pytesseract.image_to_string(image)
        return text.strip()
    
    elif ext == 'pdf':
        text = ""
        pdf_data = file.read()
        doc = fitz.open("pdf", pdf_data)
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
        return text.strip()
    
    else:
        return "Unsupported file type."

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
        "model": "llama3-8b-8192",
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

# Streamlit App
st.set_page_config(page_title="📄 Invoice Extractor", layout="centered")
st.title("📄 Invoice Uploader & Extractor")

st.markdown("Upload an invoice file (PDF or image). We'll extract key invoice fields using OCR + Mistral (via Groq API).")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    with st.spinner("🔍 Performing OCR..."):
        ocr_text = extract_text_from_file(uploaded_file)

    st.subheader("📄 OCR Extracted Text:")
    st.text_area("Raw Invoice Text", ocr_text, height=200)

    if ocr_text:
        with st.spinner("🤖 Extracting structured info with Mistral..."):
            extracted_json = extract_invoice_info_with_mistral(ocr_text)

        st.subheader("📦 Extracted Invoice Data (JSON):")
        st.code(extracted_json, language="json")
else:
    st.info("Please upload an invoice to begin.")
