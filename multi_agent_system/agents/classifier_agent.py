
from utils.openai_utils import classify_with_openai
import pdfplumber

class ClassifierAgent:
    def process(self, input_data, filename=None):
        if filename and filename.lower().endswith('.pdf'):
            with pdfplumber.open(input_data) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        if len(text) > 1500:
                            break
            content = text
        elif isinstance(input_data, str):
            content = input_data
        else:
            content = str(input_data)
        return classify_with_openai(content, filename)
