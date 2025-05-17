Invoice Extractor App (OCR + JSON Structuring with Mistral)
This project is a Streamlit web application that allows users to upload invoices (PDF or image) and extract structured information such as Invoice Number, Date, Vendor, Amounts, etc. using OCR and Mistral language models via the Groq API.
________________________________________
 Features
•	Upload invoice files (PDF, JPG, PNG)
•	OCR using Tesseract
•	Extract structured data using Groq's Mistral model
•	Outputs clean JSON with:
o	Invoice Number
o	Invoice Date
o	Vendor Name
o	Vendor Tax ID
o	Total Amount
o	Tax Amount
o	Currency
________________________________________
Tech Stack
•	Frontend: Streamlit
•	OCR Engine: Tesseract OCR
•	LLM API: Groq API using Mistral models
•	File Handling: Pillow, fitz (PyMuPDF) for PDFs
________________________________________
Installation
1. Clone the repository
bash
CopyEdit
git clone https://github.com/yourusername/invoice-extractor-app.git
cd invoice-extractor-app
2. Create and activate virtual environment (optional)
bash
CopyEdit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
CopyEdit
pip install -r requirements.txt
Note: You must install Tesseract separately. See below.
________________________________________
Install Tesseract OCR
On Ubuntu/Debian:
bash
CopyEdit
sudo apt update
sudo apt install tesseract-ocr
On macOS (with Homebrew):
bash
CopyEdit
brew install tesseract
On Windows:
•	Download from: https://github.com/UB-Mannheim/tesseract/wiki
•	Add the installed path (e.g., C:\Program Files\Tesseract-OCR) to your system's PATH.
________________________________________
Setup .env
Create a .env file in the root directory:
ini
CopyEdit
GROQ_API_KEY=your_actual_groq_api_key_here
________________________________________
Run the App
bash
CopyEdit
streamlit run app.py
Then open http://localhost:8501 in your browser.
________________________________________
Example Output
json
CopyEdit
{
  "Invoice Number": "INV-2024-00123",
  "Invoice Date": "2024-05-01",
  "Vendor Name": "ABC Supplies Pvt. Ltd.",
  "Vendor Tax ID": "GSTIN12345678",
  "Total Amount": "$1250.00",
  "Tax Amount": "$112.50",
  "Currency": "USD"
}
______________________________________
Troubleshooting
•	TesseractNotFoundError: Make sure Tesseract is installed and in your system PATH.
•	API Error 404: model not found:
o	Use "mixtral-8x7b" instead of "mistral-7b" — it's the default available model on Groq.
o	Confirm your API key and model access at https://console.groq.com.
•	PDFs not working: Ensure PyMuPDF is installed (pip install pymupdf) and works with your system.
________________________________________
To-Do / Future Improvements
•	Add authentication for multi-user use
•	Save extracted data to a database
•	 Bulk invoice uploads
•	Deploy to cloud (Streamlit Sharing, AWS, etc.)

