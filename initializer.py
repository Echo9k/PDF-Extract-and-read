# initializer.py
import json
import os
import requests
from huggingface_hub import snapshot_download

def download_json(url):
    """Download JSON content from the given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Check if request was successful
    return response.json()

def download_and_modify_json(url, local_filename, modifications):
    """Download JSON from URL and modify its contents based on modifications."""
    if os.path.exists(local_filename):
        with open(local_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config_version = data.get('config_version', '0.0.0')
        # If the version is older than desired, re-download
        if config_version < '1.1.1':
            data = download_json(url)
    else:
        data = download_json(url)

    # Apply modifications
    data.update(modifications)

    # Save the modified JSON locally
    with open(local_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def initialize_app(force=False):
    """Initialize models and configuration.
    
    This function downloads the required models and modifies the configuration file.
    It will only perform these actions if they have not been done before.
    """
    # Define the path to the configuration file in the user's home directory.
    home_dir = os.path.expanduser('~')
    config_file_name = 'magic-pdf.json'
    config_file = os.path.join(home_dir, config_file_name)
    
    # If the config file exists, assume initialization is complete.
    if os.path.exists(config_file):
        print(f"Initialization already completed. Using existing configuration at {config_file}")
        return
    elif force:
        print(f"Forced initialization.")

    # Define patterns for model download
    mineru_patterns = [
        "models/Layout/LayoutLMv3/*",
        "models/Layout/YOLO/*",
        "models/MFD/YOLO/*",
        "models/MFR/unimernet_small_2501/*",
        "models/TabRec/TableMaster/*",
        "models/TabRec/StructEqTable/*",
    ]
    model_dir = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=mineru_patterns)

    layoutreader_pattern = [
        "*.json",
        "*.safetensors",
    ]
    layoutreader_model_dir = snapshot_download('hantian/layoutreader', allow_patterns=layoutreader_pattern)

    model_dir = os.path.join(model_dir, 'models')
    print(f"Downloaded model_dir is: {model_dir}")
    print(f"Downloaded layoutreader_model_dir is: {layoutreader_model_dir}")

    # Download and modify JSON configuration
    json_url = 'https://github.com/opendatalab/MinerU/raw/master/magic-pdf.template.json'
    json_mods = {
        'models-dir': model_dir,
        'layoutreader-model-dir': layoutreader_model_dir,
    }
    download_and_modify_json(json_url, config_file, json_mods)
    print(f"The configuration file has been configured successfully, the path is: {config_file}")

# This block will run if the module is executed directly.
if __name__ == '__main__':
    initialize_app()
