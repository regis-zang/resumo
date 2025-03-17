import os
import streamlit as st
import vosk
import soundfile as sf
import json
import tempfile

# Baixar e carregar o modelo Vosk
MODEL_PATH = "model"  # Substitua pelo caminho correto do modelo
if not os.path.exists(MODEL_PATH):
    st.error("O modelo Vosk não foi encontrado! Baixe um modelo de https://alphacephei.com/vosk/models e extraia para a pasta 'model'.")

# Inicializa o modelo de reconhecimento de voz
model = vosk.Model(MODEL_PATH)

def transcribe_audio(audio_file):
    # Salvar temporariamente o arquivo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_filename = temp_file.name

    # Ler o áudio
    wf, sr = sf.read(temp_filename)

    # Criar reconhecedor de áudio
    rec = vosk.KaldiRecognizer(model, sr)

    # Processar o áudio
    for chunk in wf:
        rec.AcceptWaveform(chunk)

    os.remove(temp_filename)

    # Retornar a transcrição
    return json.loads(rec.Result())["text"]

# Interface Streamlit
st.title("Transcrição de Áudio para Texto (Vosk - Offline)")
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
