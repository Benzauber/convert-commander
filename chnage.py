import subprocess
import shutil
import os

def start(input_file, output_extension):
    def convert_file(input_file, output_file):
        if not os.path.exists(input_file):
            print(f"Die Eingabedatei '{input_file}' existiert nicht.")
            return

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            print(f"Der Ausgabeordner '{output_dir}' existiert nicht.")
            return

        # Der LibreOffice-Befehl zum Konvertieren der Datei
        command = [
            'libreoffice',
            '--headless',
            '--convert-to', output_extension,
            '--outdir', output_dir,
            input_file
        ]

        try:
            result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print(f"Konvertierung erfolgreich abgeschlossen: {result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Konvertieren: {e.stderr.decode()}")
            print(f"Ausgabe: {e.stdout.decode()}")

    # Dynamischer Zielpfad für das konvertierte Dokument
    input_ext = os.path.splitext(input_file)[1].lstrip('.')
    file_name = os.path.basename(input_file).replace(f'.{input_ext}', '')
    output_file = os.path.join('convert', f'{file_name}.{output_extension}')

    # Debug-Ausgabe für das Arbeitsverzeichnis
    print(f"Arbeitsverzeichnis: {os.getcwd()}")
    print(f"Ausgabeordner: {os.path.dirname(output_file)}")

    convert_file(input_file, output_file)
    print(f"Die Datei '{input_file}' wurde erfolgreich in '{output_file}' konvertiert.")



