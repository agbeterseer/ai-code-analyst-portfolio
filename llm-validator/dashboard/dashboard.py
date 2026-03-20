import streamlit as st
import requests
import json

st.title("LLM Output Validator")

prompt = st.text_area("Prompt")
response = st.text_area("Response")
expected_schema = st.text_area("Expected JSON Schema", value='{}')

if st.button("Validate"):
    payload = {
        "prompt": prompt,
        "response": response,
        "expected_schema": json.loads(expected_schema)
    }
    result = requests.post("http://localhost:8000/validate", json=payload)
    st.json(result.json())