import streamlit as st
from transformers import pipeline
import requests
import os
from gtts import gTTS

# Load Hugging Face API
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

# Knowledge Base
knowledge_base = {
    "bofalgan": "Bofalgan Plus fights pain in two ways: Paracetamol blocks pain signals, while Ibuprofen targets pain at the source.",
    "dosage": "Adults above 50kg: 1000mg Paracetamol + 300mg Ibuprofen every 6 hours as necessary.",
    "safety": "The safety profile of Bofalgan Plus is comparable to that of intravenous paracetamol or ibuprofen alone.",
    "opioids": "Bofalgan Plus reduces opioid dependency by offering superior analgesic effects."
}

def get_response(question):
    """Generate response from knowledge base or AI model"""
    for key in knowledge_base:
        if key in question.lower():
            return knowledge_base[key]

    # Use Hugging Face API for AI-generated responses
    response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json={"inputs": question})
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    return "I'm sorry, I couldn't process that."

def generate_speech(response_text, language="en"):
    """Convert chatbot response to speech using gTTS"""
    tts = gTTS(response_text, lang=language)
    speech_file = "response.mp3"
    tts.save(speech_file)
    return speech_file

# Streamlit UI
st.title("🗣️ AI Chatbot (Speaks & Listens!)")
st.write("Ask me about **Bofalgan Plus** (Supports English & Urdu)")

# Inject HTML for voice input
st.components.v1.html(
    """
    <button onclick="startSpeechRecognition()">🎙️ Speak</button>
    <input type="text" id="userInput" style="width:100%; padding:10px; font-size:16px; margin-top:10px;" placeholder="Speak or type here...">
    
    <script>
        function startSpeechRecognition() {
            let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-GB';  // Change to 'ur-PK' for Urdu
            recognition.start();
            
            recognition.onresult = function(event) {
                document.getElementById("userInput").value = event.results[0][0].transcript;
                document.getElementById("sendButton").click();
            };
        }
    </script>
    """,
    height=100
)

user_input = st.text_input("Or Type Here:", "")

if user_input:
    response = get_response(user_input)
    st.text_area("Chatbot:", value=response, height=100)

    # Generate speech and play
    speech_file = generate_speech(response, "en")
    st.audio(speech_file, format="audio/mp3")

st.write("🚀 **Powered by Hugging Face AI & Streamlit Cloud**")
