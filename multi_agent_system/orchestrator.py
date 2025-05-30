# orchestrator.py
from agents.classifier_agent import ClassifierAgent
from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from agents.pdf_agent import PDFAgent
from router.action_router import ActionRouter
from memory.shared_memory import save_to_memory
import time

def process_input(input_data, filename=None):
    classifier = ClassifierAgent()
    email_agent = EmailAgent()
    json_agent = JSONAgent()
    pdf_agent = PDFAgent()
    router = ActionRouter()
    
    metadata = {
        "source": filename,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    classification = classifier.process(input_data, filename=filename)
    save_to_memory('classification', {**metadata, **classification})

    if classification['format'] == 'Email':
        result = email_agent.process(input_data)
    elif classification['format'] == 'JSON':
        result = json_agent.process(input_data)
    elif classification['format'] == 'PDF':
        result = pdf_agent.process(input_data)
    else:
        result = {'error': 'Unknown format'}
    save_to_memory('result', {**metadata, **result})
    
    action = router.process(result)
    save_to_memory('action', {**metadata, **action})
    return {'classification': classification, 'result': result, 'action': action}
