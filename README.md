# multi-agent-ai-system
Multi-Format Autonomous AI System with Contextual Decisioning &amp; Chained Actions
🚀 Overview
This project is a robust, modular multi-agent AI system that processes Email, JSON, and PDF documents. It classifies both format and business intent, routes to specialized agents, extracts structured data, and dynamically chains follow-up actions such as escalation, alerting, or compliance flagging.
All processing steps and decisions are logged in a shared memory store for full auditability.

🏗️ Architecture
text
User Upload (via Streamlit UI)
   │
   ▼
Classifier Agent ──► [Email Agent / JSON Agent / PDF Agent]
   │                          │          │
   ▼                          ▼          ▼
Action Router ◄───────────────┴──────────┘
   │
   ▼
Shared Memory Store (Redis)
Classifier Agent: Uses OpenAI LLM to detect document format and business intent.

Specialized Agents: Extract/validate fields from Email, JSON, or PDF.

Action Router: Triggers follow-up actions (escalate, alert, compliance flag) via REST API.

Shared Memory: Stores all metadata, agent outputs, and action traces for audit.

🧩 Agent Logic
1. Classifier Agent
Input: Raw content + filename.

Logic:

Uses OpenAI LLM with few-shot prompt examples and schema cues.

Detects format: Email, JSON, PDF.

Detects intent: RFQ, Complaint, Invoice, Regulation, Fraud Risk.

Output:

{ "format": "...", "intent": "..." }

Writes classification metadata (source, timestamp, result) to Redis.

2. Email Agent
Input: Email content.

Logic:

Uses OpenAI to extract sender, urgency, issue/request, and tone (escalation, polite, threatening, etc.).

Output:

{ "sender": "...", "urgency": "...", "issue": "...", "tone": "..." }

Writes extraction result to Redis.

3. JSON Agent
Input: JSON string (webhook data).

Logic:

Validates required schema using Pydantic.

Flags anomalies (missing fields, type errors).

Output:

{ "data": {...}, "anomalies": [...] }

Writes result to Redis; logs alert if anomalies found.

4. PDF Agent
Input: PDF file path.

Logic:

Uses pdfplumber to extract text and parse line-item invoice or policy.

Extracts invoice total, compliance terms ("GDPR", "FDA", etc.).

Flags if total > 10,000 or compliance terms found.

Robust parsing of LLM output for compliance terms.

Output:

{ "total": ..., "compliance_terms": [...], "flags": [...] }

Writes result to Redis.

5. Action Router
Input: Agent outputs.

Logic:

If urgent escalation: POST to CRM escalate API.

If anomalies: POST to risk alert API.

If compliance flag: POST to compliance API.

Else: log and close.

Includes retry logic and error handling.

Output:

{ "action": "...", "api_response": ... }

Writes action trace to Redis.

🔁 End-to-End Flow Example
User uploads an email file.

Classifier Agent: Detects Email + Complaint.

Email Agent: Extracts sender, urgency=high, tone=escalation.

Action Router: Calls (simulated) POST /crm/escalate.

Shared Memory: Logs classification, extraction, and action for audit.

🖥️ User Interface
Streamlit app for uploading files and visualizing the classification, extraction, and action routing.

Step-by-step output with clear, human-readable summaries.

Agent trace for full auditability.

Download button to export output logs as JSON.

🛠️ Tech Stack
Python 3.10+

OpenAI LLM (gpt-4o or gpt-3.5-turbo)

Streamlit (UI)

Redis (shared memory)

pdfplumber (PDF parsing)

Pydantic (JSON validation)

requests (REST calls)

🧪 How to Run
Clone the repo and install requirements:

bash
pip install -r requirements.txt
Set up your .env file:

text
OPENAI_API_KEY=your-openai-key
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=yourpassword
CRM_API_URL=https://httpbin.org/post
RISK_API_URL=https://httpbin.org/post
COMPLIANCE_API_URL=https://httpbin.org/post
Start Redis (locally or via Docker).

Run the UI:

bash
streamlit run app.py
Upload sample files (Email, JSON, PDF) and view step-by-step results.

🗂️ Sample Inputs
Email: .eml or .txt files with various tones/intents.

JSON: Valid and invalid webhook samples.

PDF: Invoices and policy docs with/without compliance terms.

See the sample_inputs/ folder.

📤 Output Logs
After processing, click "💾 Save Output Logs as JSON" in the UI.

The logs are exported as output_logs.json for audit or submission.

📸 Screenshots & Diagrams
See /screenshots/ for UI and output examples.

See /docs/architecture.png or /screenshots/agent_flow_diagram.png for the agent flow diagram.

🖼️ Agent Flow Diagram
![Agent Flow Diagram](screenshots/agent 📝 Submission Checklist

 README.md (this file)

 Sample inputs (email, JSON, PDF) in sample_inputs/

 Output logs (output_logs.json)

 Screenshots/post-action outputs (/screenshots/)

 Agent flow diagram (/screenshots/agent_flow_diagram.png or /docs/architecture.png)

 Working video demo (see submission instructions)
