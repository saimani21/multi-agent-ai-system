import os
from orchestrator import process_input
from memory.shared_memory import read_from_memory

def read_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return filepath  # Pass path for PDF
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    base_dirs = {
        "email": "sample_inputs/email",
        "json": "sample_inputs/json",
        "pdf": "sample_inputs/pdf"
    }
    for doc_type, folder in base_dirs.items():
        print(f"\n--- Testing {doc_type.upper()} files ---")
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            content = read_file(fpath)
            print(f"\nFile: {fname}")
            result = process_input(content, filename=fname)
            print(result)
            print("Memory classification:", read_from_memory('classification'))
            print("Memory result:", read_from_memory('result'))
            print("Memory action:", read_from_memory('action'))
