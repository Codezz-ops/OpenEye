#!/usr/bin/env python3
import sys
import subprocess
import keyboard
import os
import json
import rich

print("""
     ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗   ██╗███████╗
    ██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝██╔════╝
    ██║   ██║██████╔╝█████╗  ██╔██╗ ██║█████╗   ╚████╔╝ █████╗  
    ██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══╝    ╚██╔╝  ██╔══╝  
    ╚██████╔╝██║     ███████╗██║ ╚████║███████╗   ██║   ███████╗
     ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝""")

# ANSI color codes
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
RESET = '\033[0m'  # No Color

def social_find():
    username = input("Enter username: ")

    # Command to run the Bash script
    command = ['bash', 'scripts/openeye.sh', username]

    # Start the subprocess with stdout and stderr piped to the Python script
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll for output and write it to sys.stdout in real-time
    for line in iter(process.stdout.readline, b''):
        sys.stdout.buffer.write(line)
        sys.stdout.flush()

# Wrapper function for phoneDNS
def phone_dns():
    # Define the path to the JSON file
    area_file = "resources/area_codes.json"

    # Function to extract information from JSON file
    def extract_info(id):
        with open(area_file, 'r') as f:
            data = json.load(f)
            return data[str(id)]

    # Check if the JSON file exists
    if not os.path.isfile(area_file):
        print(f"{RED}Error:{RESET} JSON file '{area_file}' not found.")
        sys.exit(1)

    # Prompt the user for a phone number
    phone_number = input("Enter your phone number: ")

    # Extract ID from phone number
    id = phone_number.split('-')[0]

    # Call function to extract information
    info = extract_info(id)
    print(f"State: {info['State']}")
    print(f"Country: {info['Country']}")
    print(f"Timezone: {info['Timezone']}")
    print(f"Region: {info['Region']}")

# Wrapper function for MXRecords
def mx_record():
    # Prompt the user for site
    site = input("Enter site: ")

    # Perform MX lookup using dig
    mx_records = os.popen(f'dig +short MX {site}').read()

    # Check if any MX record were found
    if not mx_records:
        print(f"No MX record found for {site}.")
    else:
        print(mx_records)

# Wrapper function for nslookup
def ns_lookup():
    # Prompt the user for site
    site = input("Enter site: ")

    # Perform NSlookup using nslookup
    results = os.popen(f'nslookup {site}').read()

    # Check if any results were found
    if not results:
        print(f"No results found for {site}.")
    else:
        print(results)

# Function for prompt
def prompt():
    # Print menu
    print("""
        \t     ╔════════════════════════╗
        \t     ║1. Find Social Media    ║
        \t     ║2. PhoneDNS             ║
        \t     ║3. MX Records           ║
        \t     ║4. NS Lookup            ║
        \t     ╚════════════════════════╝
    """)

    keyboard.add_hotkey("1", social_find)
    keyboard.add_hotkey("2", phone_dns)
    keyboard.add_hotkey("3", mx_record)
    keyboard.add_hotkey("4", ns_lookup)

    # Keep the program running
    keyboard.wait('esc')
    subprocess.run(['bash', 'scripts/deactivate.sh'])   

if __name__ == "__main__":
    prompt()