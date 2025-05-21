import streamlit as st
from audiorecorder import audiorecorder
import whisper
import tempfile
import os
import base64
import pyperclip
import hashlib

st.set_page_config(page_title="🗣️ Sprach-Diktierer", layout="centered")
st.title("🎤 Sprache zu Text")

st.write("Drücke den Button, sprich deinen Text, und lass Whisper ihn transkribieren.")

# Session State initialisieren
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ''
if 'initial_prompt' not in st.session_state:
    st.session_state.initial_prompt = ''
if 'alternative_results' not in st.session_state:
    st.session_state.alternative_results = []
if 'last_audio_hash' not in st.session_state:
    st.session_state.last_audio_hash = None

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
    
    # Radio-Buttons für den technischen Kontext statt Dropdown
    st.subheader("Technischer Kontext")
    tech_contexts = ["Allgemein", "Programmierung", "Web-Entwicklung", "Data Science", "DevOps", "Odoo (ERP)"]
    tech_mode = st.radio(
        "Wähle den Kontext durch Klicken",
        tech_contexts,
        index=5,  # Standardmäßig "Odoo (ERP)"
        label_visibility="collapsed",  # Verstecke das Label, da wir schon eine Überschrift haben
        help="Optimiert die Erkennung für spezifische technische Begriffe"
    )
    
    multilingual = st.checkbox(
        "Mehrsprachig", 
        True,
        help="Optimiert für gemischtes Deutsch/Englisch"
    )
    
    st.info("⏱️ Hinweis: Das erste Laden des Modells kann einige Zeit dauern, besonders bei 'small'.")

# Technische Begriffe nach Kategorie
tech_context = {
    "Programmierung": [
        "Variablen", "Funktionen", "Klassen", "Objekte", "Methoden", "Arrays", "Listen", 
        "Dictionaries", "Hashmaps", "Boolean", "Integer", "String", "Float", "Double", 
        "Exception", "Try-Catch", "Konstruktor", "Interface", "Vererbung", "Polymorphismus", 
        "API", "Framework", "Library", "Repository", "Dependency", "Compiler", "Interpreter",
        "Runtime", "Debugging", "Refactoring", "Codebase", "Algorithm", "Data Structure",
        "Stack", "Queue", "Tree", "Graph", "Linked List", "Big O Notation"
    ],
    "Web-Entwicklung": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", "Vue", "DOM", "HTTP", 
        "REST", "GraphQL", "Frontend", "Backend", "Full-Stack", "Responsive Design", "Bootstrap", 
        "SASS", "LESS", "Webpack", "NPM", "Yarn", "Node.js", "Express", "Django", "Flask", 
        "API", "Middleware", "Authentication", "Authorization", "JWT", "OAuth", "Cookies", 
        "Local Storage", "Session Storage", "CORS", "CDN"
    ],
    "Data Science": [
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "TensorFlow", "PyTorch", "Scikit-learn",
        "Regression", "Classification", "Clustering", "PCA", "SVM", "Random Forest", "Neural Network",
        "Deep Learning", "Machine Learning", "AI", "GPU", "CUDA", "Dataset", "Training", "Testing",
        "Validation", "Overfitting", "Underfitting", "Features", "Labels", "Normalization", 
        "Standardization", "Hyperparameter", "Batch Size", "Epoch", "Learning Rate"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "CI/CD", "Pipeline", "Jenkins", "GitHub Actions", "GitLab CI",
        "Terraform", "Ansible", "Chef", "Puppet", "Infrastructure as Code", "Monitoring", "Logging",
        "Prometheus", "Grafana", "ELK Stack", "AWS", "Azure", "GCP", "Load Balancing", "Auto-scaling",
        "High Availability", "Disaster Recovery", "Microservices", "Service Mesh", "Istio", "Deployment",
        "Release", "Rollback", "Blue-Green Deployment", "Canary Deployment"
    ],
    "Odoo (ERP)": [
        "Odoo", "ERP", "CRM", "Module", "Addon", "Model", "Field", "View", "Controller", "Odoo Studio", 
        "ORM", "API", "Record", "Recordset", "Domain", "XML-RPC", "JSON-RPC", "Many2one", "One2many", 
        "Many2many", "Computed Field", "Onchange", "Depends", "Inheritance", "Extension", "Override", 
        "Environment", "Registry", "Cursor", "Transaction", "Workflow", "Business Process", "Business Logic", 
        "Sales Order", "Purchase Order", "Invoice", "Accounting", "Manufacturing", "MRP", "Inventory", 
        "Stock", "Warehouse", "Point of Sale", "POS", "Website Builder", "eCommerce", "Project Management", 
        "Human Resources", "Timesheet", "Expense", "Recruitment", "Asset", "Maintenance", "Quality Control",
        "Kanban View", "List View", "Form View", "Calendar View", "Pivot View", "Graph View", "Activity View",
        "QWeb", "Report", "Reporting", "Security", "Access Rights", "Access Control", "Groups", "Users",
        "Company", "Multi-company", "Partner", "Contact", "Product", "Product Variant", "Product Template",
        "Pricelist", "Tax", "UoM", "Unit of Measure", "BOM", "Bill of Materials", "Routing", "Workorder",
        "Workcenter", "Lead", "Opportunity", "Quotation", "RFQ", "Request for Quotation", "Picking",
        "Shipment", "Procurement", "Forecasting", "Budgeting", "Reconciliation", "Journal", "Journal Entry",
        "Fiscal Position", "Chart of Accounts", "Payment Term", "EDI", "Electronic Data Interchange",
        "Webhook", "Cron Job", "Scheduled Action", "Server Action", "Client Action", "Automation",
        "Workflow Engine", "State Machine", "Sequence", "Attachment", "Chatter", "Message", "Follower",
        "Activity", "Mail Template", "Email Template", "Notification", "Alert", "Python", "PostgreSQL"
    ],
    "Allgemein": []  # Leere Liste für allgemeinen Kontext ohne spezifische Begriffe
}

# Odoo-spezifische Begriffskombinationen für bessere Erkennung
odoo_phrase_context = [
    # Häufige Begriffskombinationen
    "Odoo ERP", "Odoo Module", "Odoo Addon", "Odoo Studio", "Odoo CRM", 
    "Odoo POS", "Point of Sale", "Odoo Accounting", "Odoo Manufacturing",
    
    # Entwickler-Terminologie
    "QWeb Template", "QWeb Reports", "XML-RPC API", "JSON-RPC API", "Odoo ORM",
    "Odoo Models", "Odoo Fields", "Computed Fields", "Related Fields",
    "Many2one Field", "One2many Field", "Many2many Field", "Onchange Method",
    
    # UI-Elemente
    "Kanban View", "List View", "Form View", "Calendar View", "Pivot View",
    "Graph View", "Activity View", "Search View", "Gantt View",
    
    # Häufige Fehlerkorrekturen (falsch → richtig)
    "Q-Web → QWeb", "Odo → Odoo", "Oh du → Odoo", "Grundjob → Cron Job", 
    "Access Rights", "User Groups", "Web Client", "Odoo Framework",
    
    # Business-Prozesse
    "Sales Order", "Purchase Order", "Invoice Matching", "Warehouse Management",
    "Inventory Valuation", "Payment Terms", "Chart of Accounts", "Tax Configuration",
    "Customer Portal", "Vendor Portal", "Multi Currency", "Multi Company",
    
    # Technische Konzepte
    "Business Logic", "Server Actions", "Automated Actions", "Scheduled Actions",
    "Workflow States", "State Machine", "Email Templates", "Report Designer",
    "Database Structure", "Python Model", "PostgreSQL Database", "Data Migration"
]

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

# Generiere einen optimierten Prompt basierend auf den ausgewählten Einstellungen
def generate_prompt(tech_mode, multilingual):
    base_prompt = "Dies ist ein technisches Diktat"
    
    # Sprachkontext hinzufügen
    if multilingual:
        base_prompt += " mit gemischtem Deutsch und Englisch"
    
    # Spezifische technische Begriffe basierend auf dem Modus hinzufügen
    if tech_mode != "Allgemein" and tech_mode in tech_context:
        # Wir fügen bis zu 15 zufällige technische Begriffe hinzu
        import random
        selected_terms = random.sample(tech_context[tech_mode], min(15, len(tech_context[tech_mode])))
        base_prompt += f". Es enthält Fachbegriffe wie: {', '.join(selected_terms)}"
        
        # Für Odoo-spezifische Prompt-Verbesserungen
        if tech_mode == "Odoo (ERP)":
            # Füge Odoo-spezifische Begriffskombinationen hinzu
            selected_phrases = random.sample(odoo_phrase_context, min(10, len(odoo_phrase_context)))
            base_prompt += f". Beachte folgende typische Begriffskombinationen: {', '.join(selected_phrases)}"
            
            # Hinweise für bessere Erkennung
            base_prompt += ". Bei 'Odo' oder 'Oh du' ist wahrscheinlich 'Odoo' gemeint. Bei 'Q-Web' ist 'QWeb' gemeint. Bei 'Grundjob' ist 'Cron Job' gemeint."
    
    return base_prompt

# Verbesserte Prompt-Varianten für Odoo
def generate_odoo_prompts():
    """Generiert drei verschiedene optimierte Prompts für Odoo-Kontext"""
    
    # Basis-Information
    base_info = "Dies ist ein technisches Diktat über Odoo ERP mit Fachbegriffen aus Entwicklung und Business-Prozessen."
    
    # Prompt 1: Fokus auf Entwicklung
    dev_prompt = f"{base_info} Es geht um Odoo-Entwicklung mit Models, Fields, Views und Controllers. Technische Begriffe wie ORM, QWeb, XML-RPC, JSON-RPC und API kommen vor. Odoo Module und Addons mit Vererbung und Erweiterung werden behandelt. Bei 'Q-Web' ist 'QWeb' gemeint und bei 'Odo' ist 'Odoo' gemeint."
    
    # Prompt 2: Fokus auf Business-Prozesse
    business_prompt = f"{base_info} Es geht um Odoo Business-Prozesse wie Sales Order, Purchase Order, Invoice, Accounting, Inventory und Manufacturing. CRM, POS (Point of Sale), eCommerce und Project Management werden erwähnt. Odoo Studio, Workflow und Automatisierung sind Teil der Diskussion."
    
    # Prompt 3: Fokus auf Administration und Konfiguration
    admin_prompt = f"{base_info} Es geht um Odoo Administration und Konfiguration mit Access Rights, User Groups, Multi-company, Security, und Datenbank-Verwaltung. Cron Jobs, Server Actions und Scheduled Actions werden erwähnt. Beachte dass 'Grundjob' oft als 'Cron Job' zu verstehen ist. PostgreSQL, Backup und Restore sind wichtige Themen."
    
    return [dev_prompt, business_prompt, admin_prompt]

# Korrekte Verwendung von audiorecorder gemäß Dokumentation
audio = audiorecorder("🎙️ Aufnahme starten", "🛑 Aufnahme stoppen")

# Immer den copy_success-Status zurücksetzen, wenn eine neue Audio-Aufnahme gemacht wird
if "copy_success" in st.session_state:
    st.session_state.copy_success = False

current_audio_hash = hashlib.md5(audio.raw_data).hexdigest() if len(audio) > 0 else None

if len(audio) > 0:
    # Zeige Audio-Player im Browser
    st.audio(audio.export().read(), format="audio/wav")

    transcribe_needed = st.session_state.last_audio_hash != current_audio_hash

    if transcribe_needed:
        st.session_state.last_audio_hash = current_audio_hash
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                audio.export(tmpfile.name, format="wav")
                audio_path = tmpfile.name

            with st.spinner(f"🔍 Whisper ({model_type}) transkribiert dein Audio..."):
                try:
                    model = load_whisper_model(model_type)

                    if tech_mode == "Odoo (ERP)":
                        odoo_prompts = generate_odoo_prompts()
                        initial_prompt = odoo_prompts[0]
                        transcription_options = {
                            "language": None if language == "auto" else language,
                            "initial_prompt": initial_prompt,
                            "task": "transcribe"
                        }
                        result = model.transcribe(audio_path, **transcription_options)
                        st.success("✅ Fertig!")

                        alternative_results = []
                        for i, prompt in enumerate(odoo_prompts[1:], 1):
                            with st.spinner(f"🔄 Alternative Transkription {i} wird erstellt..."):
                                alt_options = transcription_options.copy()
                                alt_options["initial_prompt"] = prompt
                                alt_result = model.transcribe(audio_path, **alt_options)
                                alternative_results.append({
                                    "text": alt_result["text"],
                                    "prompt": prompt
                                })
                    else:
                        initial_prompt = generate_prompt(tech_mode, multilingual)
                        transcription_options = {
                            "language": None if language == "auto" else language,
                            "initial_prompt": initial_prompt,
                            "task": "transcribe"
                        }
                        result = model.transcribe(audio_path, **transcription_options)
                        st.success("✅ Fertig!")
                        alternative_results = []

                    st.session_state.transcribed_text = result["text"]
                    st.session_state.initial_prompt = initial_prompt
                    st.session_state.alternative_results = alternative_results
                except Exception as e:
                    st.error(f"Fehler beim Transkribieren: {str(e)}")
        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der Audiodatei: {str(e)}")
        finally:
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.unlink(audio_path)

    text_area = st.text_area("📝 Transkribierter Text:", st.session_state.transcribed_text, height=200)

    with st.expander("Verwendeter Prompt"):
        st.code(st.session_state.initial_prompt)

    if tech_mode == "Odoo (ERP)" and st.session_state.alternative_results:
        for i, alt in enumerate(st.session_state.alternative_results, 1):
            with st.expander(f"Alternative Transkription {i}"):
                st.text_area(f"Text (Variante {i}):", alt["text"], height=100)
                st.code(alt["prompt"], language="text")

                if st.button(f"Diese Variante verwenden", key=f"use_alt_{i}"):
                    st.session_state.transcribed_text = alt["text"]
                    st.experimental_rerun()

    col1, col2 = st.columns(2)

    with col1:
        if "copy_success" not in st.session_state:
            st.session_state.copy_success = False

        if st.button("📋 In die Zwischenablage kopieren", key="copy_btn", use_container_width=True):
            try:
                pyperclip.copy(st.session_state.transcribed_text)
                st.session_state.copy_success = True
            except Exception as e:
                st.error(f"Fehler beim Kopieren: {str(e)}")

        if st.session_state.copy_success:
            st.success("✅ Text in die Zwischenablage kopiert!")

    with col2:
        st.markdown(get_text_download_link(st.session_state.transcribed_text), unsafe_allow_html=True)
