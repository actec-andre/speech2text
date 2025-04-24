# 🎤 Sprach-Diktierer als PWA (Progressive Web App)

Dies ist eine experimentelle PWA-Version des Sprach-Diktierer-Projekts, die mit Stlite erstellt wurde, um die App vollständig im Browser laufen zu lassen und als Progressive Web App installierbar zu machen.

## 📋 Überblick

- 🌐 Vollständig browserbasiert ohne Server-Backend
- 📱 Als App auf dem Homescreen installierbar
- 🔄 Teilweise offline nutzbar
- ⚠️ Eingeschränkte Funktionalität im Vergleich zur Server-Version

## 🛠️ Technische Details

Diese Version nutzt:

- **Stlite**: Eine WebAssembly-basierte Version von Streamlit, die Pyodide verwendet
- **PWA-Funktionalität**: Mit Service Worker und Manifest für die Installation als App
- **Vereinfachte Funktionalität**: Da nicht alle Python-Pakete in Pyodide verfügbar sind

## ❗ Einschränkungen

- Die Whisper-Integration wurde entfernt, da sie in der Browser-Umgebung nicht ohne Weiteres funktioniert
- Die Audio-Aufnahme ist in dieser Demo-Version noch nicht implementiert
- Größere initiale Ladezeit für das Laden der Python-Umgebung im Browser

## 🚀 Verwendung

1. Öffne die `index.html` in einem Webserver (lokale Dateien funktionieren nicht aufgrund von CORS)
2. Die App sollte im Browser geladen werden
3. In Chrome klicke auf das Installations-Icon in der Adressleiste, um die App zu installieren

## 📦 Lokaler Test mit einem einfachen HTTP-Server

```bash
# Python 3 HTTP-Server
python -m http.server 8000

# Oder mit Node.js (npm install -g http-server)
http-server -p 8000
```

Dann öffne http://localhost:8000 in deinem Browser.

## 🔮 Zukünftige Entwicklung

- Integration einer WebAssembly-kompatiblen Spracherkennungslösung
- Unterstützung für Audio-Aufnahme im Browser
- Offline-Funktionalität verbessern

## 🔧 Anpassen und Weiterentwickeln

Um diese PWA-Version anzupassen:

1. Bearbeite den Code in der `index.html`-Datei im `files`-Bereich
2. Ändere die PWA-Konfiguration in `manifest.json` nach Bedarf
3. Erstelle eigene App-Icons und ersetze sie im `icons`-Verzeichnis

## 📄 Weitere Informationen

- [Stlite GitHub Repository](https://github.com/whitphx/stlite)
- [Progressive Web Apps - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) 