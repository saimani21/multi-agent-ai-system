# agents/pdf_agent.py
import pdfplumber
import re
from utils.openai_utils import extract_policy_compliance_with_openai

class PDFAgent:
    def process(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        match = re.search(r"Total[:\s]*\$?([0-9,\.]+)", text, re.IGNORECASE)
        total = float(match.group(1).replace(',', '')) if match else None
        compliance_terms = []
        for term in ["GDPR", "FDA"]:
            if term in text:
                compliance_terms.append(term)
        compliance_terms_ai = extract_policy_compliance_with_openai(text)
        for term in compliance_terms_ai:
            if term not in compliance_terms:
                compliance_terms.append(term)
        flags = []
        if total and total > 10000:
            flags.append("Invoice total > 10,000")
        if compliance_terms:
            flags.append(f"Mentions {', '.join(compliance_terms)}")
        return {
            'total': total,
            'compliance_terms': compliance_terms,
            'flags': flags
        }
