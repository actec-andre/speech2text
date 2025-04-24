import streamlit as st
from audiorecorder import audiorecorder
import whisper
import tempfile
import os
import base64
import pyperclip

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

# Funktion zum Erstellen eines Download-Links für Text
def get_text_download_link(text, filename="transkription.txt", link_text="📥 Text herunterladen"):
    """Generiert einen Link, um Text als Datei herunterzuladen"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="text-decoration:none;color:white;background-color:#4CAF50;padding:8px 16px;border-radius:4px;display:inline-block;text-align:center;width:100%;">{link_text}</a>'
    return href

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
                
                # Text-Area für Transkription und Session State für die Zwischenablage
                if 'transcribed_text' not in st.session_state:
                    st.session_state.transcribed_text = result["text"]
                else:
                    st.session_state.transcribed_text = result["text"]
                    
                text_area = st.text_area("📝 Transkribierter Text:", st.session_state.transcribed_text, height=200)
                
                # Buttons-Container
                col1, col2 = st.columns(2)
                
                # Streamlit-basierter Copy-Button
                with col1:
                    if st.button("📋 In die Zwischenablage kopieren", key="copy_btn", use_container_width=True):
                        try:
                            pyperclip.copy(st.session_state.transcribed_text)
                            st.success("✅ Text in die Zwischenablage kopiert!")
                        except Exception as e:
                            st.error(f"Fehler beim Kopieren: {str(e)}")
                
                # Download-Button
                with col2:
                    st.markdown(get_text_download_link(st.session_state.transcribed_text), unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Fehler beim Transkribieren: {str(e)}")
    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Audiodatei: {str(e)}")
    finally:
        # Temporäre Datei aufräumen
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.unlink(audio_path)
