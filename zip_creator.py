import os
import zipfile
import shutil

def create_zip_file(convert_folder, zip_filename="converted_files.zip"):
    """
    Creates a ZIP file from all files in the convert folder
    Args:
        convert_folder: Path to the folder containing converted files
        zip_filename: Name of the ZIP file to create
    Returns:
        Path to the created ZIP file
    """
    zip_path = os.path.join(convert_folder, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(convert_folder):
                for file in files:
                    if file != zip_filename:  # Don't include the zip file itself
                        file_path = os.path.join(root, file)
                        # Add file to ZIP with just the filename (not full path)
                        zipf.write(file_path, file)
        
        print(f"ZIP file created: {zip_path}")
        return zip_path
        
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        return None

def cleanup_convert_folder(convert_folder, keep_zip=True):
    """
    Cleans up the convert folder, optionally keeping the ZIP file
    Args:
        convert_folder: Path to the folder to clean
        keep_zip: Whether to keep ZIP files
    """
    try:
        for filename in os.listdir(convert_folder):
            if keep_zip and filename.endswith('.zip'):
                continue
            file_path = os.path.join(convert_folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        print(f"Error cleaning up folder: {e}")