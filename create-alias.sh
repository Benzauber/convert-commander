#!/bin/bash

# Make the start script executable
echo "Setting executable permission for start.sh..."
chmod +x start.sh

# Make the update script executable
echo "Setting executable permission for update.sh..."
chmod +x update.sh

# Create and load alias for Convert-Commander
echo "Creating alias for Convert-Commander..."
echo "alias ccommander='./start.sh'" >> ~/.bash_aliases
source ~/.bash_aliases

# Set up bash completion for ccommander
echo "Setting up bash completion for ccommander..."
sudo mkdir -p /etc/bash_completion.d

# Create completion script
sudo tee /etc/bash_completion.d/ccommander-completion.bash > /dev/null << 'EOF'
_ccommander_completion() {
    local cur prev opts sub_opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main options
    opts="web api update"

    # Sub-options based on the first argument
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

# Make the completion script executable and activate it
sudo chmod +x /etc/bash_completion.d/ccommander-completion.bash
source /etc/bash_completion.d/ccommander-completion.bash

echo "Installation completed. Bash completion for ccommander is now active."