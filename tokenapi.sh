#!/bin/bash

# Default name for the token file.
# Can be passed as the first argument when calling the script, e.g., ./generate_api_token.sh my_tokens.txt
TOKEN_FILE="${1:-TOKENS.txt}"

# --- Helper functions for colored output (optional, for better readability) ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function for log outputs
log_info() {
    echo -e "[${BLUE}INFO${NC}] $1"
}

log_success() {
    echo -e "[${GREEN}SUCCESS${NC}] $1"
}

log_warning() {
    echo -e "[${YELLOW}WARNING${NC}] $1"
}

log_error() {
    echo -e "[${RED}ERROR${NC}] $1" >&2 # Output errors to stderr
}

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    log_error "python3 could not be found. Please ensure Python 3 is installed and in your PATH."
    exit 1
fi

# Check if the token file exists, create it if necessary.
if [ ! -f "$TOKEN_FILE" ]; then
    log_warning "The file '$TOKEN_FILE' does not exist. It will be created now."
    touch "$TOKEN_FILE"
    if [ $? -ne 0 ]; then
        log_error "Could not create the file '$TOKEN_FILE'. Check permissions in the current directory."
        exit 1
    fi
fi

# Generate a secure token
TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
if [ -z "$TOKEN" ]; then
    log_error "Could not generate a token. The Python script might have an error."
    exit 1
fi

# Generate the SHA-256 hash of the token
HASHED_TOKEN=$(python3 -c 'import hashlib; print(hashlib.sha256(input().encode("utf-8")).hexdigest())' <<< "$TOKEN")
if [ -z "$HASHED_TOKEN" ]; then
    log_error "Could not hash the token. The Python script might have an error."
    exit 1
fi

echo -e "\n========================================================================="
log_info "Generating new API Token and adding it to '$TOKEN_FILE'"
echo -e "=========================================================================\n"

echo -e "${BLUE}API Token (for client use):${NC}"
echo "-------------------------------------------------------------------------"
echo "$TOKEN"
echo ""
echo -e "${BLUE}Hashed Token (will be added to '$TOKEN_FILE'):${NC}"
echo "-------------------------------------------------------------------------"
echo "$HASHED_TOKEN"
echo ""

# Check if the hash already exists in the file (exact line match)
if grep -qFx "$HASHED_TOKEN" "$TOKEN_FILE"; then
    log_warning "The hash '$HASHED_TOKEN' already exists in '$TOKEN_FILE'."
    log_info "No new entry was added."
else
    # Add the hash as a new line to the file
    if echo "$HASHED_TOKEN" >> "$TOKEN_FILE"; then
        log_success "The hash '$HASHED_TOKEN' was successfully added to '$TOKEN_FILE'."
    else
        log_error "Could not add the hash to '$TOKEN_FILE'. Check write permissions for the file."
        exit 1
    fi
fi

echo -e "\n========================================================================="
echo -e "${YELLOW}IMPORTANT:${NC} Restart your Flask application for the new token to be recognized!"
echo -e "=========================================================================\n"

exit 0