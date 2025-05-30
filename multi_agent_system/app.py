import streamlit as st
from orchestrator import process_input
import os
import json

st.set_page_config(page_title="Multi-Format Autonomous AI System", page_icon="🤖", layout="centered")

st.title("🤖 Multi-Format Autonomous AI System")
st.markdown("""
Upload an Email (.eml/.txt), JSON (.json), or PDF (.pdf) and watch the AI classify, extract, and route your document in real time.
""")

uploaded_file = st.file_uploader("📤 Drag & drop or browse your file", type=["eml", "txt", "json", "pdf"])

if uploaded_file is not None:
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    st.success(f"File Uploaded: {filename}")

    # Handle file input for PDF or text-based files
    if ext == ".pdf":
        temp_path = f"temp_{filename}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        input_data = temp_path
    else:
        input_data = uploaded_file.read().decode("utf-8")

    if st.button("🚀 Process Document"):
        with st.spinner("🤖 AI is analyzing your document..."):
            result = process_input(input_data, filename=filename)
        st.success("✅ Processing complete!")

        # --- Step 1: Classification ---
        st.header("Step 1: Classification")
        classification = result.get("classification", {})
        st.markdown(f"""
        - **Source File:** `{filename}`
        - **Document Format:** `{classification.get('format', 'N/A')}`
        - **Business Intent:** `{classification.get('intent', 'N/A')}`
        """)

        # --- Step 2: Extraction/Validation ---
        st.header("Step 2: Extraction / Validation")
        extraction = result.get("result", {})
        if classification.get('format') == "Email":
            st.markdown(f"""
            - **Sender:** `{extraction.get('sender', 'N/A')}`
            - **Urgency Level:** `{extraction.get('urgency', 'N/A')}`
            - **Issue/Request:** `{extraction.get('issue', 'N/A')}`
            - **Tone Detected:** `{extraction.get('tone', 'N/A')}`
            """)
        elif classification.get('format') == "JSON":
            st.markdown(f"- **Extracted Data:**")
            st.json(extraction.get('data', {}))
            if extraction.get('anomalies'):
                st.warning(f"Anomalies: {extraction['anomalies']}")
        elif classification.get('format') == "PDF":
            st.markdown(f"""
            - **Invoice Total:** `{extraction.get('total', 'N/A')}`
            - **Compliance Terms:** `{', '.join(extraction.get('compliance_terms', [])) or 'None'}`
            - **Flags:** `{', '.join(extraction.get('flags', [])) or 'None'}`
            """)
        else:
            st.write(extraction)

        # --- Step 3: Action Routing ---
        st.header("Step 3: Action Routing")
        action = result.get("action", {})
        action_type = action.get('action', 'N/A')
        st.markdown(f"- **Action Taken:** `{action_type.capitalize()}`")
        if action_type == 'escalate':
            st.info("The issue was escalated to CRM (simulated API call).")
        elif action_type == 'log_alert':
            st.warning("An anomaly was detected and logged as an alert.")
        elif action_type == 'flag_compliance':
            st.warning("A compliance issue was flagged (simulated API call).")
        elif action_type == 'log_and_close':
            st.success("Routine case. Logged and closed.")
        elif action_type == 'error':
            st.error(f"Error during action: {action.get('error', '')}")

        # --- Step 4: Agent Trace for Audit ---
        st.header("Agent Trace (for Audit)")
        from memory.shared_memory import read_from_memory, export_all_logs
        trace_class = read_from_memory('classification')
        trace_result = read_from_memory('result')
        trace_action = read_from_memory('action')
        st.markdown("**Classification:**")
        st.json(trace_class)
        st.markdown("**Extraction Result:**")
        st.json(trace_result)
        st.markdown("**Action:**")
        st.json(trace_action)

        # --- Save Output Logs Button ---
        if st.button("💾 Save Output Logs as JSON"):
            output_file = export_all_logs("output_logs.json")
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download output_logs.json",
                    data=f,
                    file_name="output_logs.json",
                    mime="application/json"
                )
            st.success("Output logs saved and ready for download!")

        # Clean up temp file if needed
        if ext == ".pdf":
            os.remove(temp_path)

    st.info("💡 Tip: Try uploading different file types to see how the AI routes and processes each one!")

else:
    st.markdown("<div style='color:#888;'>No file uploaded yet. Try an email, JSON, or PDF sample!</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("Made by Sai Mani")
