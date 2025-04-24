import streamlit as st
from audiorecorder import audiorecorder
import whisper
import tempfile
import os

st.set_page_config(page_title="🗣️ Sprach-Diktierer", layout="centered")
st.title("🎤 Sprache zu Text")

st.write("Drücke den Button, sprich deinen Text, und lass Whisper ihn transkribieren.")

# Konfigurationsoptionen
with st.sidebar:
    st.header("Einstellungen")
    model_type = st.selectbox(
        "Whisper Modell",
        ["tiny", "base", "small"],
        help="Größere Modelle sind genauer, aber langsamer. 'tiny' ist am schnellsten, 'small' am genauesten."
    )
    
    language = st.selectbox(
        "Hauptsprache",
        ["German", "English", "auto"],
        help="Die Hauptsprache des Diktats. 'auto' für automatische Erkennung."
    )
    
    multilingual = st.checkbox(
        "Mehrsprachig (Code/Technisch)", 
        True,
        help="Optimiert für Diktate mit gemischtem Deutsch/Englisch und Codepassagen."
    )
    
    st.info("⏱️ Hinweis: Das erste Laden des Modells kann einige Zeit dauern, besonders bei 'small'.")

# Cache für das Whisper-Modell
@st.cache_resource
def load_whisper_model(model_name):
    with st.spinner(f"🔄 Lade Whisper {model_name}-Modell (nur beim ersten Mal nötig)..."):
        return whisper.load_model(model_name)

# Korrekte Verwendung von audiorecorder gemäß Dokumentation
audio = audiorecorder("🎙️ Aufnahme starten", "🛑 Aufnahme stoppen")

if len(audio) > 0:
    # Zeige Audio-Player im Browser
    st.audio(audio.export().read(), format="audio/wav")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            audio.export(tmpfile.name, format="wav")
            audio_path = tmpfile.name

        with st.spinner(f"🔍 Whisper ({model_type}) transkribiert dein Audio..."):
            try:
                model = load_whisper_model(model_type)
                
                # Optimierte Transkription für gemischtes Deutsch/Englisch
                transcription_options = {
                    "language": None if language == "auto" else language,
                    "initial_prompt": "Dies ist ein technisches Diktat mit gemischtem Deutsch und Englisch sowie Codepassagen." if multilingual else None,
                    "task": "transcribe"
                }
                
                result = model.transcribe(audio_path, **transcription_options)
                st.success("✅ Fertig!")
                st.text_area("📝 Transkribierter Text:", result["text"], height=200)
            except Exception as e:
                st.error(f"Fehler beim Transkribieren: {str(e)}")
    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Audiodatei: {str(e)}")
    finally:
        # Temporäre Datei aufräumen
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.unlink(audio_path)
