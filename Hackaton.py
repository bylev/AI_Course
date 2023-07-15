import openai  
import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import tempfile
from PIL import Image
import requests
from io import BytesIO

openai.api_key  = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
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


    # Cargar el modelo Whisper
    model = whisper.load_model("base")
    if audio is not None:
        result = model.transcribe(audio)
        st.write(result["text"])
    else:
        st.write("No se ha proporcionado ningún audio.")

    model = whisper.load_model("base")


    
if __name__ == "__main__":
    main()