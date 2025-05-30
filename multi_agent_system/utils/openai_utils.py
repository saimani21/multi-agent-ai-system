
import openai
import os
from dotenv import load_dotenv
import re
import ast

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_with_openai(content, filename=None):
    improved_prompt = f'''
You are an expert business document classifier.
Given the following, classify:
- format: [Email, JSON, PDF, Unknown]
- intent: [RFQ, Complaint, Invoice, Regulation, Fraud Risk, Other]

Examples:
Filename: complaint_escalation_urgent.eml
Content: "Subject: URGENT: Unacceptable Service...I will escalate..."
Format: Email, Intent: Complaint

Filename: invoice_valid.json
Content: '{{"event_type":"invoice","amount":9500}}'
Format: JSON, Intent: Invoice

Filename: policy_gdpr.pdf
Content: "This policy describes how we comply with GDPR and FDA regulations."
Format: PDF, Intent: Regulation

Filename: rfq_request.eml
Content: "Request for quotation on 100 units of product X."
Format: Email, Intent: RFQ

Filename: fraud_alert.json
Content: '{{"event_type":"fraud_alert","details":"Suspicious transaction detected."}}'
Format: JSON, Intent: Fraud Risk

Now classify:
Filename: {filename}
Content: "{content[:1000]}"

Respond ONLY in this JSON format:
{{"format": "...", "intent": "..."}}
'''
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": improved_prompt}],
        temperature=0
    )
    # ...rest of code...

    import json
    try:
        text = response.choices[0].message.content
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception as e:
        print("OpenAI classification failed:", e)
        return {"format": "Unknown", "intent": "Other"}


def extract_email_fields_with_openai(email_content):
    prompt = f"""
Extract these fields from the email:
- sender (email address)
- urgency (high/low)
- issue/request (main problem or request)
- tone (escalation, polite, threatening, neutral, routine)

Email:
\"\"\"
{email_content}
\"\"\"

Respond ONLY in this JSON format:
{{"sender":"...","urgency":"...","issue":"...","tone":"..."}}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    import json
    try:
        text = response.choices[0].message.content
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception as e:
        print("OpenAI extraction failed:", e)
        return {
            "sender": "unknown@example.com",
            "urgency": "low",
            "issue": "",
            "tone": "neutral"
        }

import re
import ast

def extract_policy_compliance_with_openai(policy_text):
    prompt = f"""
From the following policy document, list all compliance terms mentioned (choose from: GDPR, FDA, HIPAA, PCI, SOC2, or others you find).

Policy Text:
\"\"\"
{policy_text[:1500]}
\"\"\"

Respond with a Python list of strings, e.g. ["GDPR", "PCI"]
Do NOT wrap your answer in triple backticks or a code block.
"""
    # Simulated response for testing parser logic
    # In production, replace with actual LLM call:
    # response_text = client.chat.completions.create(...).choices[0].message.content
    response_text = "``````"  # Example with code block

    try:
        text = response_text.strip()
        # Remove code block formatting if present
        text = re.sub(r"^``````$", "", text).strip()
        if text.startswith("[") and text.endswith("]"):
            result = ast.literal_eval(text)
            # Only return non-empty, real terms
            return [t for t in result if t and t.strip()]
        # Fallback: split by comma if not a list
        return [t.strip().strip('"').strip("'") for t in text.split(",") if t.strip()]
    except Exception as e:
        print("OpenAI compliance extraction failed:", e)
        return []
def robust_parse_llm_output(text):
    # Remove code block formatting
    text = re.sub(r'```[\w]*\n?', '', text).strip()

    try:
        if text.startswith('[') and text.endswith(']'):
            result = ast.literal_eval(text)
            return [t for t in result if t and t.strip()]
        # fallback: split by comma
        return [t.strip().strip('"').strip("'") for t in text.split(',') if t.strip()]
    except Exception as e:
        print(f"Parsing failed: {e}")
        return []