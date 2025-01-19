import subprocess
import shutil
import os

def start(input_file, output_extension):
    def convert_file(input_file, output_file):
        if not os.path.exists(input_file):
            print(f"The input file '{input_file}' does not exist.")
            return

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            print(f"The output folder '{output_dir}' does not exist.")
            return

        # The LibreOffice command to convert the file
        command = [
            'libreoffice',
            '--headless',
            '--convert-to', output_extension,
            '--outdir', output_dir,
            input_file
        ]

        try:
            result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print(f"Conversion completed successfully: {result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e.stderr.decode()}")
            print(f"Output: {e.stdout.decode()}")

    # Dynamic target path for the converted document
    input_ext = os.path.splitext(input_file)[1].lstrip('.')
    file_name = os.path.basename(input_file).replace(f'.{input_ext}', '')
    output_file = os.path.join('convert', f'{file_name}.{output_extension}')

    # Debug output for the working directory
    print(f"Working directory: {os.getcwd()}")
    print(f"Output folder: {os.path.dirname(output_file)}")

    convert_file(input_file, output_file)
    print(f"The file '{input_file}' has been successfully converted to '{output_file}'.")
