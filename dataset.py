import requests
import os
import json

# Define the download path
download_path = '/Users/sivanagendra/Documents/devel/multimodal/data/aria_digital_twin_dataset/'

# Function to download a file given a URL
def download_file(url, path):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check if the download is successful

    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
            f.write(chunk)
    print(f"Downloaded {path}")

# Function to recursively parse the JSON structure and download files
def parse_json_and_download(data, path=download_path):
    if isinstance(data, dict):
        # Check if the dictionary has 'download_url' and 'filename' keys
        if 'download_url' in data and 'filename' in data:
            file_path = os.path.join(path, data['filename'])
            download_file(data['download_url'], file_path)
        else:
            for key, value in data.items():
                # Create a directory for each key
                new_path = os.path.join(path, key)
                # Recurse into the next level of the dictionary
                parse_json_and_download(value, new_path)

# Load the JSON structure from the file
json_file_path = '/Users/sivanagendra/Documents/devel/multimodal/aria_digital_twin_dataset.json'
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Start the recursive parsing and downloading process
parse_json_and_download(json_data)
