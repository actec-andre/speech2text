# 🎤 Sprache zu Text Diktierer (Speech2Text)

Eine Streamlit-App zur Umwandlung von gesprochener Sprache in Text mit Unterstützung für technische Diktate und gemischte Deutsch/Englisch-Inhalte.

## 📋 Funktionen

- 🎙️ Einfache Audioaufnahme direkt im Browser
- 🔄 Transkription mit OpenAI Whisper
- 🌐 Unterstützung für gemischte Deutsch/Englisch Diktate
- 💻 Optimiert für technische Begriffe und Code
- ⚡ Verschiedene Modellgrößen für unterschiedliche Performance-Anforderungen

## 🛠️ Installation

### Systemvoraussetzungen

- Python 3.8 oder höher
- FFmpeg (für die Audioverarbeitung)

### FFmpeg installieren

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Lade FFmpeg von [ffmpeg.org](https://ffmpeg.org/download.html) herunter und füge es zum PATH hinzu.

### Python-Umgebung einrichten

1. Repository klonen oder Dateien herunterladen:
```bash
git clone https://github.com/actec-andre/speech2text.git
cd speech2text
```

2. Virtuelle Umgebung erstellen (optional, aber empfohlen):
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

3. Erforderliche Pakete installieren:
```bash
pip install -r requirements.txt
```

## 🚀 Anwendung starten

Starte die App mit:
```bash
streamlit run app.py
```

Die App ist dann verfügbar unter: http://localhost:8501

## 💡 Verwendung

1. Öffne die App im Browser
2. Wähle deine bevorzugten Einstellungen in der Seitenleiste:
   - Whisper-Modell (tiny, base, small)
   - Hauptsprache
   - Mehrsprachigkeitsoption für technische Inhalte
3. Klicke auf "🎙️ Aufnahme starten" und sprich dein Diktat
4. Klicke auf "🛑 Aufnahme stoppen", wenn du fertig bist
5. Warte auf die Transkription und kopiere das Ergebnis

## ⚙️ Modellauswahl

- **tiny**: Schnell, niedrigerer Ressourcenverbrauch, weniger genau
- **base**: Gutes Gleichgewicht zwischen Geschwindigkeit und Genauigkeit
- **small**: Genauer, aber langsamer und ressourcenintensiver

## 📝 Hinweise

- Das erste Laden des Modells kann einige Zeit dauern, besonders bei größeren Modellen
- Für beste Ergebnisse verwende ein externes Mikrofon
- Stelle sicher, dass dein Browser Zugriff auf das Mikrofon hat
- Die Audioqualität beeinflusst die Genauigkeit der Transkription

## 📄 Lizenz

Veröffentlicht unter der [MIT-Lizenz](LICENSE).
