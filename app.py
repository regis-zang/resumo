import os
import streamlit as st
import whisper
import tempfile
import soundfile as sf

# Certifica que o ffmpeg está no caminho do sistema
os.environ["PATH"] += os.pathsep + "/usr/bin"

def transcribe_audio(audio_file):
    model = whisper.load_model("base")

    # Salva o arquivo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_filename = temp_file.name

    # Transcreve o áudio
    result = model.transcribe(temp_filename)
    os.remove(temp_filename)

    return result["text"]

# Interface do Streamlit
st.title("Transcrição de Áudio para Texto")
st.write("Faça o upload de um arquivo de áudio e veja a transcrição.")

audio_file = st.file_uploader("Upload de áudio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    st.write("Transcrevendo...")

    try:
        transcript = transcribe_audio(audio_file)
        st.subheader("Texto Transcrito:")
        st.write(transcript)
    except Exception as e:
        st.error(f"Erro ao processar o áudio: {e}")
