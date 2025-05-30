# 🤖 FlowBit AI – Multi-Agent Document Intake System

FlowBit AI is a robust, modular multi-agent AI system that processes **Email**, **JSON**, and **PDF** documents. It classifies document format and business intent, routes content to specialized agents, extracts structured data, and dynamically chains follow-up actions such as escalation, alerting, or compliance flagging.

All steps are logged in a shared memory store (**Redis**) for full auditability.

---

## 🚀 Overview

### Core Capabilities:
- Detect format (Email, JSON, PDF)
- Classify intent (Invoice, Complaint, RFQ, Fraud, etc.)
- Extract structured data
- Trigger follow-up actions (escalation, alerts)
- Maintain audit log in shared memory

---

## 🏗️ Architecture

```text
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
```

### Components:
- **Classifier Agent** – Uses OpenAI LLM to detect format and intent
- **Specialized Agents** – Extract/validate fields based on document type
- **Action Router** – Triggers follow-up REST actions
- **Shared Memory** – Redis-based central store for metadata and logs

---

## 🧩 Agent Logic

### 1. 🧠 Classifier Agent
- **Input:** Raw content + filename  
- **Logic:** Uses LLM to classify format and business intent  
- **Output:**
```json
{ "format": "email", "intent": "complaint" }
```
- **Audit:** Writes classification metadata to Redis

---

### 2. 📧 Email Agent
- **Input:** Email content  
- **Logic:** Extracts sender, urgency, issue, and tone (e.g., escalation)  
- **Output:**
```json
{ "sender": "...", "urgency": "...", "issue": "...", "tone": "..." }
```

---

### 3. 🧾 JSON Agent
- **Input:** Webhook JSON  
- **Logic:** Validates schema using Pydantic, flags anomalies  
- **Output:**
```json
{ "data": {...}, "anomalies": [...] }
```

---

### 4. 📄 PDF Agent
- **Input:** PDF file path  
- **Logic:** Parses invoice total and compliance terms (e.g., GDPR, HIPAA)  
- **Output:**
```json
{ "total": 11000, "compliance_terms": ["GDPR"], "flags": ["high_amount"] }
```

---

### 5. 🔁 Action Router
- **Input:** Outputs from agents  
- **Logic:**
  - Escalates via CRM API  
  - Alerts risk via webhook  
  - Flags compliance issues  
- **Output:**
```json
{ "action": "escalate", "api_response": 200 }
```

---

## 🔁 End-to-End Flow Example

1. User uploads an `.eml` file  
2. **Classifier Agent**: Detects `email` + `complaint`  
3. **Email Agent**: Extracts sender, urgency=`high`, tone=`escalation`  
4. **Action Router**: Sends to `/crm/escalate`  
5. **Redis**: Stores full trace for audit

---

## 🖥️ User Interface

- Built using **Streamlit**
- Drag-and-drop upload
- Step-by-step agent trace
- Final output summary with download option
- Save output logs as `output_logs.json`

---

## 🛠️ Tech Stack

- Python 3.10+
- OpenAI GPT-4o / GPT-3.5-turbo
- Streamlit
- Redis
- pdfplumber
- Pydantic
- requests

---

## 🧪 How to Run

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file:

```env
OPENAI_API_KEY=your-openai-key
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=yourpassword

CRM_API_URL=https://httpbin.org/post
RISK_API_URL=https://httpbin.org/post
COMPLIANCE_API_URL=https://httpbin.org/post
```

### 3. Start Redis locally or via Docker

### 4. Run the Streamlit UI:

```bash
streamlit run app.py
```

---

## 🗂️ Sample Inputs

Available in the `/sample_inputs/` directory:
- **Email:** `.txt` or `.eml` files with various tones/intents
- **JSON:** Valid and invalid webhook samples
- **PDF:** Invoices and policy documents

---

## 📤 Output Logs

- All results are written to Redis for traceability
- Use the UI button to download: `output_logs.json`

---

## 📸 Screenshots & Diagrams

- Screenshots: `/screenshots/`
- Architecture Diagram: `/screenshots/agent_flow_diagram.png` or `/docs/architecture.png`

### 🖼️ Agent Flow Diagram

![Agent Flow Diagram](screenshots/agent_flow_diagram.png)

---

## 📝 Submission Checklist

- ✅ `README.md`
- ✅ Sample inputs in `/sample_inputs/`
- ✅ Output logs: `output_logs.json`
- ✅ Screenshots: `/screenshots/`
- ✅ Architecture diagram: `/screenshots/agent_flow_diagram.png`
- ✅ Video demo (if applicable)

---

## 📬 Contact

Created by **[@saimani21](https://github.com/saimani21)**  
Feel free to open issues or pull requests!
