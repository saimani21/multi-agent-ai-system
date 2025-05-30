import os
import requests
from utils.retry import retry

class ActionRouter:
    def __init__(self):
        # Load API endpoints from environment variables with defaults for testing
        self.crm_url = os.getenv("CRM_API_URL", "https://httpbin.org/post")  # e.g., https://yourcrm.com/api/escalate
        self.risk_url = os.getenv("RISK_API_URL", "https://httpbin.org/post")  # e.g., https://yourrisk.com/api/alert
        self.compliance_url = os.getenv("COMPLIANCE_API_URL", "https://httpbin.org/post")  # e.g., https://yourcompliance.com/api/flag

        self.session = requests.Session()
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry as RequestsRetry

        retries = RequestsRetry(
            total=3,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    @retry(max_retries=3, delay=2, exceptions=(requests.RequestException,))
    def post_with_retry(self, url, json):
        response = self.session.post(url, json=json, timeout=5)
        response.raise_for_status()
        print(f"POST to {url} succeeded with status {response.status_code}")
        return response

    def process(self, agent_outputs):
        try:
            if agent_outputs.get('tone') in ['escalation', 'threatening'] and agent_outputs.get('urgency') == 'high':
                print(f"Calling CRM escalate API at {self.crm_url}...")
                resp = self.post_with_retry(self.crm_url, agent_outputs)
                action = 'escalate'
            elif agent_outputs.get('anomalies'):
                print(f"Calling Risk Alert API at {self.risk_url}...")
                resp = self.post_with_retry(self.risk_url, agent_outputs)
                action = 'log_alert'
            elif agent_outputs.get('flags'):
                print(f"Calling Compliance Flag API at {self.compliance_url}...")
                resp = self.post_with_retry(self.compliance_url, agent_outputs)
                action = 'flag_compliance'
            else:
                print("Routine case: log and close (no external API call).")
                action = 'log_and_close'

            # Optionally return API response content for logging/audit
            return {
                'action': action,
                'api_response': resp.json() if 'resp' in locals() else None
            }

        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return {'action': 'error', 'error': str(e)}
