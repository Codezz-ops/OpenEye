#!/bin/bash

# ANSI color codes
YELLOW='\033[1;33m'
RESET='\033[0m' # No Color

# Check if necessary dependencies are installed
command -v curl >/dev/null 2>&1 || {
    printf "${RED}Error:${RESET} curl is required but not installed. Please install curl.\n"
    exit 1
}

command -v jq >/dev/null 2>&1 || {
    printf "${RED}Error:${RESET} jq is required but not installed. Please install jq.\n"
    exit 1
}

# Wrapper function for soical finding
social_find() {
    # Define the path to the JSON file
    site_file="resources/data.json"

    # Function to read JSON value
    read_json_value() {
        local key="$1"
        local site_file="$2"
        jq -r ".$key" "$site_file"
    }
    
    username=$1

    # Check if the username matches regex pattern
    if [[ ! $username =~ ^[a-zA-Z0-9_\-]{3,15}$ ]]; then
        printf "${RED}Invalid username format.$RESET\n"
        exit 1
    fi

    # Check if the JSON file exists
    if [ ! -f "$site_file" ]; then
        printf "${RED}Error:${RESET} JSON file '$site_file' not found.\n"
        exit 1
    fi

    printf "$YELLOW[*] Checking username $RESET$username ${YELLOW}on:\n $RESET"

    # Initialize counter
    success_count=0

    # Loop through each entry in the JSON file
    jq -r 'keys[] as $k | "\($k):\(.[$k].url)"' "$site_file" |
    while IFS=: read -r site_name url; do
        # Replace {} in the URL with the username
        url="${url/\{\}/$username}"

        # Send a GET request to the site
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        # Check the response status code
        if [ "$response" == "200" ]; then
            printf "[$YELLOW+$RESET]$YELLOW$site_name:$RESET '$username'\n"
        fi
    done
}

export -f social_find

social_find "$@"    