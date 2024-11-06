# Convert-Commander
![img1](https://github.com/Benzauber/convert-commander/blob/main/pictures/1.png?raw=true)

## What is Convert-Commander
You can see this on the [website](https://cc.bleibundgut.ch/).
 
# Installation Convert-Commander

## Installation

1. **Clone Repository**
   
   First, clone the repository to your system:

   ```bash
   git clone https://github.com/Benzauber/convert-commander.git
   ```

2. **Run Installation Script**
   
   Navigate to the cloned directory and execute the `install.sh` script:

   ```bash
   cd convert-commander
   ./install.sh
   ```

## Usage

After installation, the following commands are available:

* **Start**
  
  To start the service, run `ccommander`:

  ```bash
  ccommander web start
  ```

* **Stop**
  
  To stop the service, use:

  ```bash
  ccommander web stop
  ```

* **Check Status**
  
  To check the status of the service, use:

  ```bash
  ccommander web status
  ```
The Web will then be running on `http://0.0.0.0:5000`.

# API Documentation

## Starting the API



* **Start**
* To start the API, run the following command in the command line:
  ```bash
  ccommander api start
  ```

* **Stop**
  
  To stop the service, use:

  ```bash
  ccommander api stop
  ```

* **Check Status**
  
  To check the status of the service, use:

  ```bash
  ccommander api status
  ```

* **Generate token**
  
   To generate the token, use:

  ```bash
  ccommander api startus
  ```

The API will then be running on `http://0.0.0.0:5001`.

## API Routes

### Generate a new API Token

**Endpoint:** `/generate_token`  
**Method:** `POST`  
**Description:** Generates a new API token that must be used for authentication in other API calls.

**Example Request:**

```bash
curl -X POST http://0.0.0.0:5001/generate_token
```

### Upload and Convert a File

**Endpoint:** `/upload`  
**Method:** `POST`  
**Description:** Uploads a file and converts it to the specified format.

**Parameters:**
* `file`: The file to be uploaded
* `format`: The target format for conversion
* `X-API-Token`: The generated API token for authentication

**Example Request:**

```bash
curl -X POST -H "X-API-Token: <api_token>" -F "file=@/path/to/file.txt" -F "format=pdf" http://0.0.0.0:5001/upload
```

### Clear Folders

**Endpoint:** `/clear`  
**Method:** `POST`  
**Description:** Deletes all files in the upload and conversion folders.

**Parameters:**
* `X-API-Token`: The generated API token for authentication

**Example Request:**

```bash
curl -X POST -H "X-API-Token: <api_token>" http://0.0.0.0:5001/clear
```

## External Script File (sendapi.sh)

Here is an example script that uses the API functionality from the command line:

```bash
#!/bin/bash

FILE_PATH=$1
TARGET_FORMAT=$2
API_TOKEN="<api_token>"
API_URL="http://0.0.0.0:5001/upload"

if [ -z "$FILE_PATH" ] || [ -z "$TARGET_FORMAT" ] || [ -z "$API_TOKEN" ]; then
    echo "Usage: $0 <file_path> <target_format> <api_token>"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "File not found!"
    exit 1
fi

# Extract filename without path
FILENAME=$(basename "$FILE_PATH")
# Remove original file extension
FILENAME_WITHOUT_EXT="${FILENAME%.*}"
# Create new filename with target format extension
NEW_FILENAME="${FILENAME_WITHOUT_EXT}.${TARGET_FORMAT}"

# Send the file with the target format to the API, including the API token in the header
response_file=$(mktemp)
http_code=$(curl -s -w "%{http_code}" -o "$response_file" -X POST \
    -H "X-API-Token: $API_TOKEN" \
    -F "file=@$FILE_PATH" \
    -F "format=$TARGET_FORMAT" \
    $API_URL)

if [ $http_code -eq 200 ]; then
    # Save the API response to the new file
    mv "$response_file" "$NEW_FILENAME"
    echo "Conversion successful. The converted file has been saved as '$NEW_FILENAME'."
    rm -f "$response_file" # Remove the temporary file if not needed anymore
elif [ $http_code -eq 401 ]; then
    echo "Error: Invalid API token. Please check your token and try again."
    rm -f "$response_file"
else
    echo "Error during conversion. Server response (HTTP $http_code):"
    cat "$response_file"
    rm -f "$response_file"
fi
```

To use this script, save it as `sendapi.sh` and run it with the following parameters:

```bash
./sendapi.sh /path/to/file.txt pdf <api_token>
```

This script sends the file to the `/upload` API endpoint, converts it to the specified format, and saves the converted file in the current directory.

Additionally, the script also provides an endpoint `/clear` to delete all files in the upload and conversion folders. This can be called as follows:

```bash
./sendapi.sh "" "" <api_token>
```

Please replace `<api_token>` with the actual generated API token.


