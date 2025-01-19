from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import os
import pandoc
import libre
import ffmpeg
from flask_cors import CORS
import shutil
from threading import Timer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store filetest
global_filetest = None
folder_path_1 = 'uploads'
folder_path_2 = 'convert'

pandoc_formats = [
    "markdown", "rst", "asciidoc", "org", "muse", "textile", "markua", "txt2tags", "djot",
    "html", "xhtml", "html5", "chunked-html",
    "epub", "fictionbook2",
    "texinfo", "haddock",
    "roff-man", "roff-ms", "mdoc-man",
    "latex", "context",
    "docbook", "jats", "bits", "tei", "opendocument", "opml",
    "bibtex", "biblatex", "csl-json", "csl-yaml", "ris", "endnote",
    "docx", "rtf", "odt",
    "ipynb",
    "icml", "typst",
    "mediawiki", "dokuwiki", "tikimediawiki", "twiki", "vimwiki", "xwiki", "zimwiki", "jira-wiki", "creole",
    "beamer", "pptx", "slidy", "revealjs", "slideous", "s5", "dzslides",
    "csv", "tsv",
    "ansi-text",
    "pdf", "txt"
]

libreoffice_formats = ["xls", "xlsx", "ods", "ppt", "pptx", "odp"]

ffmpeg_formats = [
    'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'mpeg', 'mpg', 'ts', '3gp', 'mp3', 'wav', 'aac', 'flac',
    'ogg', 'm4a', 'wma', 'ac3', 'amr', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'mxf', 'vob',
    'asf', 'dv', 'm3u8', 'mpd'
    ]

def delete_files_in_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate through all files and subfolders in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Check if it is a file or a folder
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Delete file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Delete folder and its content
            except Exception as e:
                print(f'Error deleting {file_path}. Reason: {e}')
    else:
        print(f'Folder {folder_path} does not exist')

def download_file(filepath, global_filetest):    
    filename = os.path.splitext(os.path.basename(filepath))[0]
    filethepath = f'convert/{filename}.{global_filetest}'
    try:
        print(f"Ready for download: {filethepath}")
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
            return redirect(url_for('index', status='No file selected'))
        file = request.files['file']
        
        if file.filename == '':
            return redirect(url_for('index', status='No file selected'))
        
        if file and global_filetest is not None:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
    
            if global_filetest in libreoffice_formats:
                print("Libreoffice")
                libre.start(filepath, global_filetest)
            elif global_filetest in pandoc_formats:
                print("Pandoc")
                pandoc.start(filepath, global_filetest)
            elif global_filetest in ffmpeg_formats:
                print("Ffmpeg")
                ffmpeg.start(filepath, global_filetest)
 
            response = redirect(url_for('download', filename=file.filename))
    
            Timer(5, delete_files_after_delay).start()
    
            return response

        
        elif file:
            return redirect(url_for('index', status='File uploaded, but file type not selected'))

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
    print(f"Received data: {daten}")

    return jsonify({"status": "successfully received", "message": "Please upload a file now"})

@app.route('/docs')
def doc():
    return render_template("docs.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
