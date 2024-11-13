from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import os
import chnage
from flask_cors import CORS
import shutil
from threading import Timer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stelle sicher, dass der Upload-Ordner existiert
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Globale Variable zur Speicherung von filetest
global_filetest = None
folder_path_1 = 'uploads'
folder_path_2 = 'convert'

def delete_files_in_folder(folder_path):
    # Überprüfen, ob der Ordner existiert
    if os.path.exists(folder_path):
        # Durch alle Dateien und Unterordner im Ordner iterieren
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Überprüfen, ob es eine Datei oder ein Ordner ist
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Datei oder symbolischen Link löschen
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Ordner und dessen Inhalt löschen
            except Exception as e:
                print(f'Fehler beim Löschen {file_path}. Grund: {e}')
    else:
        print(f'Ordner {folder_path} existiert nicht')

def download_file(filepath, global_filetest):    
    filename = os.path.splitext(os.path.basename(filepath))[0]
    filethepath = f'convert/{filename}.{global_filetest}'
    try:
        print(f"Bereit zum Download: {filethepath}")
        return send_file(filethepath, as_attachment=True)
    except Exception as e:
        return str(e)

def delete_files_after_delay():
    delete_files_in_folder(folder_path_1)
    delete_files_in_folder(folder_path_2)

@app.route('/', methods=['GET', 'POST'])
def index():
    global global_filetest


    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index', status='Keine Datei ausgewählt'))
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(url_for('index', status='Keine Datei ausgewählt'))
        
        if file and global_filetest is not None:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
    
            chnage.start(filepath, global_filetest)
    
            response = redirect(url_for('download', filename=file.filename))
    
            Timer(5, delete_files_after_delay).start()
    
            return response

        
        elif file:
            return redirect(url_for('index', status='Datei hochgeladen, aber Dateityp nicht ausgewählt'))





    return render_template('index.html', status=request.args.get('status'))

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    global global_filetest
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return download_file(filepath, global_filetest)
    

@app.route('/empfange_daten', methods=['POST'])
def empfange_daten():
    global global_filetest
    daten = request.json['daten']
    global_filetest = daten
    print(f"Empfangene Daten: {daten}")

    return jsonify({"status": "erfolgreich empfangen", "message": "Bitte laden Sie jetzt eine Datei hoch"})

@app.route('/docs')
def doc():
    return render_template("docs.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
