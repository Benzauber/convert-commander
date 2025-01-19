import subprocess
import shutil
import os

def start(input_file, output_extension):
    """
    Converts a file to the desired format using Pandoc.
    
    Args:
        input_file (str): Path to the input file
        output_extension (str): Desired output format (e.g., 'pdf', 'docx', 'html')
    """
    def convert_file(input_file, output_file):
        if not os.path.exists(input_file):
            print(f"Input file '{input_file}' does not exist.")
            return False

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Output directory '{output_dir}' has been created.")
            except OSError as e:
                print(f"Error creating output directory: {e}")
                return False

        # Pandoc command for file conversion
        command = [
            'pandoc',
            input_file,
            '-o', output_file,
            '--standalone'  # Creates a complete document
        ]

        try:
            result = subprocess.run(
                command,
                check=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True  # Returns text instead of bytes
            )
            print("Conversion completed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e.stderr}")
            print(f"Output: {e.stdout if hasattr(e, 'stdout') else 'No output available'}")
            return False
        except FileNotFoundError:
            print("Pandoc is not installed or not available in PATH.")
            print("Please install Pandoc: https://pandoc.org/installing.html")
            return False

    # Dynamic target path for the converted document
    input_ext = os.path.splitext(input_file)[1].lstrip('.')
    file_name = os.path.basename(input_file).replace(f'.{input_ext}', '')
    output_file = os.path.join('convert', f'{file_name}.{output_extension}')

    # Debug output
    print(f"Working directory: {os.getcwd()}")
    print(f"Output directory: {os.path.dirname(output_file)}")
    print(f"Converting '{input_file}' to '{output_file}'")

    if convert_file(input_file, output_file):
        print(f"File was successfully converted: '{output_file}'")
    else:
        print("Conversion was not completed successfully.")