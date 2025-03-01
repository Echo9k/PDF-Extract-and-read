# utils.py
import os
import zipfile
import base64
import re
import logging


def compress_directory_to_zip(directory_path, output_zip_path):
    """
    Compresses the specified directory into a ZIP file.
    """
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)
        return True
    except Exception as e:
        logging.exception("Error compressing directory: %s", e)
        return False

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def replace_image_with_base64(markdown_text, image_dir_path):
    """
    Finds markdown image tags and replaces file paths with embedded base64 data.
    """
    pattern = r'\!\[(?:[^\]]*)\]\(([^)]+)\)'
    
    def replace(match):
        relative_path = match.group(1)
        full_path = os.path.join(image_dir_path, relative_path)
        base64_image = image_to_base64(full_path)
        return f"![{relative_path}](data:image/jpeg;base64,{base64_image})"
    
    return re.sub(pattern, replace, markdown_text)
