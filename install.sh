#!/bin/bash

# Logo anzeigen
cat << "EOF"
  _____                                _             _____                                                _             
 / ____|                              | |           / ____|                                              | |            
| |      ___   _ __ __   __ ___  _ __ | |_  ______ | |      ___   _ __ ___   _ __ ___    __ _  _ __    __| |  ___  _ __ 
| |     / _ \ | '_  \ \ / // _ \| '__|| __||______|| |     / _ \ | '_ ` _ \ | '_ ` _ \  / _` || '_ \  / _` | / _ \| '__|
| |____| (_) || | | |\ V /|  __/| |   | |_         | |____| (_) || | | | | || | | | | || (_| || | | || (_| ||  __/| |   
 \_____|\___/ |_| |_| \_/  \___||_|    \__|         \_____|\___/ |_| |_| |_||_| |_| |_| \__,_||_| |_| \__,_| \___||_|   
EOF

echo "Starting Convert-Commander installation..."

# Funktion zur Fortschrittsanzeige
progress_bar() {
    local progress=$1
    local total=12
    local percent=$(( progress * 100 / total ))
    local completed=$(( percent / 5 ))
    local remaining=$(( 20 - completed ))

    # Erzeuge den Fortschrittsbalken
    bar="["
    for ((i=0; i<$completed; i++)); do
        bar+="#"
    done
    for ((i=0; i<$remaining; i++)); do
        bar+=" "
    done
    bar+="] $percent%"

    # Zeige den Fortschrittsbalken an
    echo -ne "$bar\r"
    sleep 1
    if [ "$progress" -lt "$total" ]; then
        tput el
    fi
}

total_steps=11
current_step=0

# Python installieren
echo "Installing Python..."
sudo apt-get install -y python3.6
((current_step++))
progress_bar $current_step

# pip installieren
echo "Installing pip..."
sudo apt install -y python3-pip
((current_step++))
progress_bar $current_step

# Virtuelle Umgebung einrichten
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
((current_step++))
progress_bar $current_step

# Flask installieren
echo "Installing Flask..."
pip install flask
((current_step++))
progress_bar $current_step

# API-Flask installieren
echo "Installing API-Flask..."
pip install apiflask 
pip install flask-cors
((current_step++))
progress_bar $current_step

# Swagger UI installieren
pip install flask-swagger-ui 
((current_step++))
progress_bar $current_step

# LibreOffice installieren
echo "Installing LibreOffice..."
sudo apt-get install -y libreoffice
((current_step++))
progress_bar $current_step

# PyOO installieren
echo "Installing pyoo..."
pip install pyoo 
((current_step++))
progress_bar $current_step

# gunicorn installieren
echo "Installing gunicorn..."
pip install gunicorn
((current_step++))
progress_bar $current_step

# jp installieren
echo "Installing jp..."
sudo apt-get install jq
((current_step++))
progress_bar $current_step


# Ordner erstellen
echo "Creating folders..."
mkdir -p ./convert ./uploads
((current_step++))
progress_bar $current_step

chmod +x create-alias.sh
bash create-alias.sh
sleep 5
source ~/.bashrc
((current_step++))
progress_bar $current_step


# Fertigstellung anzeigen
echo -e "\nConvert-Commander installation completed successfully!"
