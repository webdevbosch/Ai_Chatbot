import streamlit as st
from transformers import pipeline

# Load Hugging Face model for text generation (Free)
nlp_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Bofalgan Plus Knowledge Base
knowledge_base = {
    "bofalgan": "Bofalgan Plus fights pain in two ways: Paracetamol blocks pain signals, while Ibuprofen targets pain at the source.",
    "dosage": "Adults above 50kg: 1000mg Paracetamol + 300mg Ibuprofen every 6 hours as necessary.",
    "safety": "The safety profile of Bofalgan Plus is comparable to that of intravenous paracetamol or ibuprofen alone.",
    "opioids": "Bofalgan Plus reduces opioid dependency by offering superior analgesic effects."
}

def get_response(question):
    """Generate a response based on the knowledge base or AI model."""
    for key in knowledge_base:
        if key in question.lower():
            return knowledge_base[key]
    
    response = nlp_model(question, max_length=1000, do_sample=True)
    return response[0]['generated_text']

# Streamlit UI
st.title("💬 AI Chatbot - Bofalgan Plus")
st.write("Ask me anything about **Bofalgan Plus** (Supports English & Urdu)")

user_input = st.text_input("You:", "")

if user_input:
    response = get_response(user_input)
    st.text_area("Chatbot:", value=response, height=100)

    # Text-to-Speech (TTS)
    st.audio(f"https://api.voicerss.org/?key=YOUR_VOICE_RSS_KEY&hl=en-us&src={response}")

st.write("🚀 **Powered by Hugging Face AI & Streamlit Cloud**")
