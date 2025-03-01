import json
import os

import requests
from huggingface_hub import snapshot_download


def download_json(url):
    """Download JSON file from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_and_modify_json(url, local_filename, modifications):
    """Download and modify a JSON file if it doesn't exist or if it's outdated."""
    if os.path.exists(local_filename):
        with open(local_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config_version = data.get('config_version', '0.0.0')

        # Only re-download if the version is outdated
        if config_version < '1.1.1':
            data = download_json(url)
    else:
        data = download_json(url)

    # Apply modifications
    for key, value in modifications.items():
        data[key] = value

    # Save modified JSON
    with open(local_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def check_and_download_models():
    """Download models only if they are not already present."""
    model_base_path = os.path.expanduser("~/.cache/huggingface/hub")

    mineru_models_path = os.path.join(model_base_path, "opendatalab__PDF-Extract-Kit-1.0")
    layoutreader_models_path = os.path.join(model_base_path, "hantian__layoutreader")

    # Check if models exist before downloading
    if not os.path.exists(mineru_models_path):
        mineru_patterns = [
            "models/Layout/LayoutLMv3/*",
            "models/Layout/YOLO/*",
            "models/MFD/YOLO/*",
            "models/MFR/unimernet_small_2501/*",
            "models/TabRec/TableMaster/*",
            "models/TabRec/StructEqTable/*",
        ]
        mineru_models_path = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=mineru_patterns)
    
    if not os.path.exists(layoutreader_models_path):
        layoutreader_pattern = [
            "*.json",
            "*.safetensors",
        ]
        layoutreader_models_path = snapshot_download('hantian/layoutreader', allow_patterns=layoutreader_pattern)

    # Print paths
    print(f'model_dir is: {mineru_models_path}/models')
    print(f'layoutreader_model_dir is: {layoutreader_models_path}')

    # JSON configuration update
    json_url = 'https://github.com/opendatalab/MinerU/raw/master/magic-pdf.template.json'
    config_file_name = 'magic-pdf.json'
    home_dir = os.path.expanduser('~')
    config_file = os.path.join(home_dir, config_file_name)

    json_mods = {
        'models-dir': f"{mineru_models_path}/models",
        'layoutreader-model-dir': layoutreader_models_path,
    }

    download_and_modify_json(json_url, config_file, json_mods)
    print(f'The configuration file has been configured successfully, the path is: {config_file}')


if __name__ == '__main__':
    check_and_download_models()
