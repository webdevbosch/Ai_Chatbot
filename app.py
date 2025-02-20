import streamlit as st
import requests

# Hugging Face API Endpoint (Free Tier)
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}  # Replace with your API Key

# Knowledge Base (Predefined Answers for Common Questions)
knowledge_base = {
    "bofalgan": "Bofalgan Plus fights pain in two ways: Paracetamol blocks pain signals, while Ibuprofen targets pain at the source.",
    "dosage": "Adults above 50kg: 1000mg Paracetamol + 300mg Ibuprofen every 6 hours as necessary.",
    "safety": "The safety profile of Bofalgan Plus is comparable to that of intravenous paracetamol or ibuprofen alone.",
    "opioids": "Bofalgan Plus reduces opioid dependency by offering superior analgesic effects."
}

def get_response(question):
    """Generate a response using the knowledge base or Hugging Face API."""
    for key in knowledge_base:
        if key in question.lower():
            return knowledge_base[key]
    
    # Request AI response from Hugging Face
    payload = {"inputs": question}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["generated_text"]
    else:
        return "I'm sorry, but I couldn't generate a response right now."

# Streamlit UI
st.title("💬 AI Chatbot - Bofalgan Plus")
st.write("Ask me anything about **Bofalgan Plus** (Supports English & Urdu)")

user_input = st.text_input("You:", "")
if user_input:
    response = get_response(user_input)
    st.text_area("Chatbot:", value=response, height=100)

st.write("🚀 **Powered by Hugging Face API & Streamlit Cloud**")
