import streamlit as st
import whisper
import tempfile
import os

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_filename = temp_file.name
    
    result = model.transcribe(temp_filename)
    os.remove(temp_filename)
    
    return result["text"]

# Configuração da Página do Streamlit
st.title("Transcrição de Áudio para Texto")
st.write("Faça o upload de um arquivo de áudio e transcreva-o para texto usando Whisper.")

# Upload do Arquivo
audio_file = st.file_uploader("Faça o upload do arquivo de áudio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    st.write("Transcrevendo...")
    transcript = transcribe_audio(audio_file)
    st.subheader("Texto Transcrito:")
    st.write(transcript)
