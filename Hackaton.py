import openai  
import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import tempfile
from PIL import Image
import requests
from io import BytesIO
import pyttsx3
from IPython.display import Audio

openai.api_key  = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
def text_to_speech(text):
    engine = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        temp_audio_path = temp_audio.name + ".wav"
        engine.save_to_file(text, temp_audio_path)
        engine.runAndWait()
        audio_data = open(temp_audio_path, "rb").read()
        return audio_data
def main(): 
    st.title("Oral Essay")
    audio_bytes = audio_recorder()
    if audio_bytes:
        with open("audio.wav", "wb") as audio_file:
            audio_file.write(audio_bytes)
        audio_path = os.path.join(os.getcwd(), "audio.wav")  
        # Cargar el audio desde el archivo grabado previamente
        
    else:
        audio_path = None
    if audio_path is not None:
            audio = whisper.load_audio(audio_path)
    else:
            audio = None

    result = None
    # Cargar el modelo Whisper
    model = whisper.load_model("base")
    if audio is not None:
        result = model.transcribe(audio)
        st.write(result["text"])
    else:
        st.write("No se ha proporcionado ningún audio.")

    model = whisper.load_model("base")
    if result is not None:
        prompt = f"Responde esto: '{result}'"
        response = get_completion(prompt)
        st.write(response)

        audio_data = text_to_speech(response)
        st.audio(audio_data, format="audio/wav")
    else:
        st.write("No se ha proporcionado ningún texto de entrada.")
 
if __name__ == "__main__":
    main()