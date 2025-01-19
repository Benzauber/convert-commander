#!/bin/bash

# URL of your Flask application
API_URL="http://localhost:9596"

# Make a POST request to the /generate_token endpoint
response=$(curl -s -X POST "${API_URL}/generate_token")

# Check if the request was successful
if [[ $? -ne 0 ]]; then
    echo "Error: Unable to connect to the API."
    exit 1
fi

# Extract the token from the JSON response using jq
token=$(echo "$response" | jq -r '.token')

# Check if the token was extracted successfully
if [[ $token == "null" ]]; then
    echo "Error: Token not found in the response."
    exit 1
fi

# Output the token
echo "Token: $token"
