# agents/email_agent.py
from utils.openai_utils import extract_email_fields_with_openai

class EmailAgent:
    def process(self, email_content):
        return extract_email_fields_with_openai(email_content)
