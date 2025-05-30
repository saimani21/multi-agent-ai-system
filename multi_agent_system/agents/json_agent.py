# agents/json_agent.py
import json
from pydantic import BaseModel, ValidationError

class WebhookSchema(BaseModel):
    id: str
    event_type: str
    amount: float
    customer: str
    date: str

class JSONAgent:
    def process(self, json_content):
        try:
            data = json.loads(json_content)
            validated = WebhookSchema(**data)
            anomalies = []
        except ValidationError as e:
            anomalies = [str(e)]
            data = None
        except Exception as e:
            anomalies = [str(e)]
            data = None
        return {'data': data, 'anomalies': anomalies}
