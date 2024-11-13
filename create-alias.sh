#!/bin/bash

# Start-Skript ausführbar machen
echo "Setting executable permission for start.sh..."
chmod +x start.sh

# Alias für Convert-Commander erstellen und laden
echo "Creating alias for Convert-Commander..."
echo "alias ccommander='./start.sh'" >> ~/.bash_aliases
source ~/.bash_aliases

# Bash-Completion für ccommander erstellen
echo "Setting up bash completion for ccommander..."
sudo mkdir -p /etc/bash_completion.d

# Completion-Skript erstellen
sudo tee /etc/bash_completion.d/ccommander-completion.bash > /dev/null << 'EOF'
_ccommander_completion() {
    local cur prev opts sub_opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Hauptoptionen
    opts="web api"

    # Unteroptionen basierend auf dem ersten Argument
    case "${prev}" in
        "web")
            sub_opts="start stop status"
            COMPREPLY=( $(compgen -W "${sub_opts}" -- ${cur}) )
            return 0
            ;;
        "api")
            sub_opts="start stop status token"
            COMPREPLY=( $(compgen -W "${sub_opts}" -- ${cur}) )
            return 0
            ;;
        "ccommander")
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
    esac
}

complete -F _ccommander_completion ccommander
EOF

# Completion-Skript ausführbar machen und aktivieren
sudo chmod +x /etc/bash_completion.d/ccommander-completion.bash
source /etc/bash_completion.d/ccommander-completion.bash

echo "Installation completed. Bash completion for ccommander is now active."