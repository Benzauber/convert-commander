#!/bin/bash

# Display logo
cat << "EOF"
  _____                                _             _____                                                _             
 / ____|                              | |           / ____|                                              | |            
| |      ___   _ __ __   __ ___  _ __ | |_  ______ | |      ___   _ __ ___   _ __ ___    __ _  _ __    __| |  ___  _ __ 
| |     / _ \ | '_  \ \ / // _ \| '__|| __||______|| |     / _ \ | '_ ` _ \ | '_ ` _ \  / _` || '_ \  / _` | / _ \| '__|
| |____| (_) || | | |\ V /|  __/| |   | |_         | |____| (_) || | | | | || | | | | || (_| || | | || (_| ||  __/| |   
 \_____|\___/ |_| |_| \_/  \___||_|    \__|         \_____|\___/ |_| |_| |_||_| |_| |_| \__,_||_| |_| \__,_| \___||_|   
EOF

echo "Starting Convert-Commander installation..."

# Function for progress bar display
progress_bar() {
    local progress=$1
    local total=8
    local percent=$(( progress * 100 / total ))
    local completed=$(( percent / 5 ))
    local remaining=$(( 20 - completed ))

    bar="["
    for ((i=0; i<$completed; i++)); do
        bar+="#"
    done
    for ((i=0; i<$remaining; i++)); do
        bar+=" "
    done
    bar+="] $percent%"

    echo -ne "$bar\r"
    sleep 1
    if [ "$progress" -lt "$total" ]; then
        tput el
    fi
}

total_steps=8
current_step=0

# Installing Python
echo "Installing Python..."
sudo apt-get install -y python3 python3-pip
((current_step++))
progress_bar $current_step

# Setting up virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
((current_step++))
progress_bar $current_step

# Installing dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
((current_step++))
progress_bar $current_step

# Installing LibreOffice
echo "Installing LibreOffice..."
sudo apt-get install libreoffice
((current_step++))
progress_bar $current_step

# Installing ffmpeg
echo "Installing ffmpeg..."
sudo apt-get install ffmpeg
((current_step++))
progress_bar $current_step

# Installing pandoc
echo "Installing pandoc..."
sudo apt-get install pandoc
((current_step++))
progress_bar $current_step

# Creating folders
echo "Creating folders..."
mkdir -p ./convert ./uploads
((current_step++))
progress_bar $current_step

# Making scripts executable
chmod +x create-alias.sh tokenapi.sh
bash create-alias.sh
sleep 5
source ~/.bashrc
((current_step++))
progress_bar $current_step

# Completion message
echo -e "\nConvert-Commander installation completed successfully!"
