import openai
import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import tempfile
import pyttsx3
import pandas as pd
# Set up your OpenAI API credentials
openai.api_key = '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'



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

embeddings = f"""All tourist places to go in Merida by the information of what you have"""
def text_to_speech(text):
    engine = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        temp_audio_path = temp_audio.name + ".wav"
        engine.save_to_file(text, temp_audio_path)
        engine.runAndWait()
        audio_data = open(temp_audio_path, "rb").read()
        return audio_data

def translate_text(text, target_language):
    # Translate text to target language using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following {target_language}:\n\n{text}",
        max_tokens=100,
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        n=1,
    )
    translation = response.choices[0].text.strip()
    return translation

def detect_language(text):
    # Detect language of the text using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"What is the language of the following text: \"{text}\"?",
        max_tokens=50,
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        n=1
    )
    language = response.choices[0].text.strip()
    return language

def customer_support_chat(foreigner_input):
    # Detect foreign language
    foreign_language = detect_language(foreigner_input)

    # Translate local support's input to foreigner's language
    foreigner_message = translate_text(foreigner_input, foreign_language)

    # Prepare the conversation history to be displayed for each user
    foreigner_display = foreigner_message

    return foreigner_display

st.title("Tourism guide")
audio_bytes = audio_recorder()
if audio_bytes:
    with open("audio.wav", "wb") as audio_file:
        audio_file.write(audio_bytes)
    audio_path = os.path.join(os.getcwd(), "audio.wav")
else:
    audio_path = None

result = None
if audio_path is not None:
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("base")
    result = model.transcribe(audio)
else:
    st.write("Hello, I am your tourism guide, how can I help you?")

if result is not None:
    foreigner_input = result["text"]
    foreign_language = detect_language(foreigner_input)
    prompt = f"""Respond this {foreigner_input} with the information of ´´{embeddings}´´ """
    response = get_completion(prompt)

    # Translate local support's input to foreigner's language
    foreigner_message = translate_text(response, foreign_language)

    # Prepare the conversation history to be displayed for each user
    foreigner_display = foreigner_message
    st.write(foreigner_display)

    audio_data = text_to_speech(foreigner_display)
    st.audio(audio_data, format="audio/wav")
else:
    st.write("Write your questions without pity")

foreigner_input = st.text_input("Texto del usuario extranjero")




 
