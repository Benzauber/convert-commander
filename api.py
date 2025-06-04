from flask import Flask, request, jsonify, send_file, make_response
from flask_swagger_ui import get_swaggerui_blueprint
import os
import pandoc # Annahme: pandoc Modul ist korrekt installiert/verfügbar
# Stelle sicher, dass 'libre' und 'ffmpeg' die korrekten Importnamen für deine Bibliotheken sind.
# Oft sind es z.B. 'libreoffice_convert' oder 'ffmpeg_python'.
# Für dieses Beispiel gehe ich davon aus, dass 'libre' und 'ffmpeg' als Module existieren,
# die eine 'start' Methode haben, wie in deinem Originalcode.
import libre # Platzhalter für deine LibreOffice-Konvertierungsbibliothek
import ffmpeg # Platzhalter für deine FFmpeg-Konvertierungsbibliothek
from flask_cors import CORS
import shutil
import logging
from werkzeug.utils import secure_filename
import mimetypes
import secrets
import hashlib
from functools import wraps
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Für Produktion Origins spezifizieren!

UPLOAD_FOLDER = 'uploads'
CONVERT_FOLDER = 'convert'
TOKEN_FILE = 'TOKENS.txt' # Datei für gehashte Tokens

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERT_FOLDER'] = CONVERT_FOLDER

with open('static/data/formats.json', 'r') as f:
    data = json.load(f)


pandoc_formats = data['pandocGruppe']
libreoffice_formats = data['tabelleGruppe'] + data['persentGruppe']
ffmpeg_formats = data['videoGruppe'] + data['audioGruppe'] + data['imageGruppe']

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Convert-Commander API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

hashed_tokens = set()

def hash_token(token):
    """ Generiert einen SHA-256 Hash des Tokens. """
    return hashlib.sha256(token.encode()).hexdigest()

def load_hashed_tokens(filepath=TOKEN_FILE):
    """ Lädt gehashte Tokens aus einer Datei. """
    global hashed_tokens
    try:
        with open(filepath, 'r') as f:
            for line in f:
                token_hash = line.strip()
                if token_hash: # Überspringe leere Zeilen
                    hashed_tokens.add(token_hash)
        if not hashed_tokens:
            logging.warning(f"Keine Tokens aus {filepath} geladen. Die API ist möglicherweise nicht erreichbar.")
        else:
            logging.info(f"{len(hashed_tokens)} Token(s) erfolgreich aus {filepath} geladen.")
    except FileNotFoundError:
        logging.error(f"Token-Datei {filepath} nicht gefunden! Erstelle sie und füge gehashte Tokens hinzu. Die API wird ohne Tokens nicht funktionieren.")
        # Optional: Erstelle eine leere Datei, um Fehler beim nächsten Start zu vermeiden, falls gewünscht
        # with open(filepath, 'w') as f:
        #     pass # Erstellt eine leere Datei
    except Exception as e:
        logging.error(f"Fehler beim Laden der Tokens aus {filepath}: {e}")

# Lade Tokens beim App-Start
load_hashed_tokens()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if not token:
            return jsonify({'error': 'API token is missing'}), 401
        
        # Vergleiche den Hash des bereitgestellten Tokens mit den geladenen Hashes
        current_token_hash = hash_token(token)
        if current_token_hash not in hashed_tokens:
            logging.warning(f"Ungültiger Token-Versuch. Hash: {current_token_hash}")
            return jsonify({'error': 'Invalid API token'}), 401
        return f(*args, **kwargs)
    return decorated

# Der '/generate_token' Endpunkt wurde entfernt. Tokens werden nun manuell hinzugefügt.

def delete_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f'Error deleting {file_path}. Reason: {e}')
    else:
        logging.warning(f'Folder {folder_path} does not exist')

@app.route('/upload', methods=['POST'])
@token_required
def upload_file():
    """
    Upload a file and convert it to the specified format
    ---
    tags:
      - File Conversion
    consumes:
      - multipart/form-data
    parameters:
      - in: header
        name: X-API-Token
        type: string
        required: true
        description: API token for authentication
      - in: formData
        name: file
        type: file
        required: true
        description: The file to upload
      - in: formData
        name: format
        type: string
        required: true
        description: The target format for conversion
    responses:
      200:
        description: Successfully converted file
        content:
          application/octet-stream: {} # Besser für Dateidownloads
      400:
        description: Invalid request
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    if 'file' not in request.files or 'format' not in request.form:
        return jsonify({'error': 'No file or format specified'}), 400

    file = request.files['file']
    target_format = request.form['format'].lower() # Konsistenz bei Formaten
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    logging.info(f"File uploaded: {filepath}")

    try:
        logging.debug(f"Starting conversion from {filepath} to {target_format}")
        
        base_filename, _ = os.path.splitext(filename)
        converted_filename = f"{base_filename}.{target_format}"
        converted_filepath = os.path.join(app.config['CONVERT_FOLDER'], converted_filename)

        # Stelle sicher, dass die Konvertierungsmodule/-funktionen korrekt aufgerufen werden
        if target_format in libreoffice_formats:
            logging.debug("Using LibreOffice for conversion")
            libre.start(filepath, target_format) # Annahme: libre.start konvertiert und speichert im CONVERT_FOLDER
        elif target_format in pandoc_formats:
            logging.debug("Using Pandoc for conversion")
            pandoc.start(filepath, target_format) # Annahme: pandoc.start konvertiert und speichert im CONVERT_FOLDER
        elif target_format in ffmpeg_formats:
            logging.debug("Using FFmpeg for conversion")
            ffmpeg.start(filepath, target_format) # Annahme: ffmpeg.start konvertiert und speichert im CONVERT_FOLDER
        else:
            # Lösche die hochgeladene Datei, wenn das Format nicht unterstützt wird
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Unsupported target format: {target_format}'}), 400
        
        if not os.path.exists(converted_filepath):
            # Lösche die Originaldatei, wenn die Konvertierung fehlschlägt oder keine Datei erzeugt
            if os.path.exists(filepath):
                os.remove(filepath)
            logging.error(f"Converted file not found at {converted_filepath} after attempting conversion.")
            return jsonify({'error': 'Converted file not found. Conversion might have failed.'}), 500

        logging.debug(f"Sending converted file: {converted_filepath}")
        
        mime_type, _ = mimetypes.guess_type(converted_filepath)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        response = make_response(send_file(converted_filepath, as_attachment=True, download_name=converted_filename, mimetype=mime_type))
        
        # Aufräumen nach dem Senden (optional, aber empfohlen)
        # Defers file deletion until after the request is complete
        @response.call_on_close
        def cleanup_files():
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logging.debug(f"Original file {filepath} deleted.")
                if os.path.exists(converted_filepath):
                    os.remove(converted_filepath)
                    logging.debug(f"Converted file {converted_filepath} deleted.")
            except Exception as e:
                logging.error(f"Error during file cleanup: {e}")
        
        return response

    except Exception as e:
        logging.error(f"Error during conversion or file handling: {str(e)}", exc_info=True)
        # Stelle sicher, dass hochgeladene Dateien bei Fehlern gelöscht werden
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as cleanup_error:
                logging.error(f"Failed to cleanup original file {filepath} after error: {cleanup_error}")
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500


@app.route('/clear', methods=['POST'])
@token_required
def clear_folders():
    """
    Clear all files in the upload and conversion folders
    ---
    tags:
      - Maintenance
    parameters:
      - in: header
        name: X-API-Token
        type: string
        required: true
        description: API token for authentication
    responses:
      200:
        description: Folders successfully cleared
      401:
        description: Unauthorized
    """
    delete_files_in_folder(app.config['UPLOAD_FOLDER'])
    delete_files_in_folder(app.config['CONVERT_FOLDER'])
    return jsonify({'message': 'Folders cleared'}), 200

if __name__ == '__main__':
    # Stelle sicher, dass die Datei TOKENS.txt existiert oder erstelle sie, bevor du versuchst, daraus zu lesen.
    if not os.path.exists(TOKEN_FILE):
        logging.warning(f"{TOKEN_FILE} nicht gefunden. Erstelle eine leere Datei.")
        with open(TOKEN_FILE, 'w') as f:
            f.write("") # Schreibe einen leeren String oder einen Beispiel-Hash mit Kommentar
        logging.info(f"{TOKEN_FILE} wurde erstellt. Bitte füge gehashte API-Tokens hinzu und starte die Anwendung neu.")
    
    app.run(debug=True, host="0.0.0.0", port="9596")