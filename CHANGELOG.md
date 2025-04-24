# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt der [Semantischen Versionierung](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - Unreleased

### Hinzugefügt
- Drei spezialisierte Odoo-Prompts für unterschiedliche Fachbereiche:
  - Entwicklung (Models, Fields, Views, Controllers)
  - Business-Prozesse (Sales, Purchase, Accounting)
  - Administration (Access Rights, Cron Jobs, Security)
- Direkte Anzeige alternativer Transkriptionen für Odoo-Kontext
- Vereinfachte Auswahl des technischen Kontexts durch Radiobuttons statt Dropdown
- Odoo (ERP) als Standard-Kontext voreingestellt

### Verbessert
- Optimierte Prompt-Generierung für Odoo-Fachterminologie
- Bessere Erkennung typischer Odoo-Begriffskombinationen
- Automatische Korrektur häufiger Erkennungsfehler (z.B. "Q-Web" → "QWeb")
- Leistungsoptimierung des Kopiervorgangs ohne Neuberechnung der Transkription
- Session-Management für nahtlose Benutzererfahrung

## [0.4.0] - Unreleased

### Hinzugefügt
- Kategorie-spezifische Erkennung technischer Begriffe für verschiedene Bereiche:
  - Programmierung
  - Web-Entwicklung
  - Data Science
  - DevOps
  - Odoo (ERP)
- Anzeige des verwendeten Prompts für mehr Transparenz
- Automatische Einbeziehung relevanter Fachbegriffe in den Whisper-Prompt

## [0.3.0] - Unreleased

### Hinzugefügt
- "In die Zwischenablage kopieren"-Button für transkribierte Texte
- Download-Funktion für transkribierte Texte als Textdatei

## [0.2.0] - Unreleased

### Hinzugefügt
- Streamlit UI für Audioaufnahme und Transkription
- Unterstützung für mehrere Whisper Modelle (tiny, base, small)
- Optimierung für gemischte Deutsch/Englisch-Transkription
- Fehlerbehandlung für robustere Ausführung

## [0.1.0] - Unreleased

### Hinzugefügt
- Basis-Implementierung mit Whisper
- Audioaufnahme und -wiedergabe
- Transkription von Sprache zu Text 