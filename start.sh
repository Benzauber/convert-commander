#!/bin/bash

# Activate virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Path to the Python scripts
PYTHON_SCRIPT_WEB="index:app"  # Format: "filename:app_name"
PYTHON_SCRIPT_API="api:app"    # Format: "filename:app_name"

# PID files for the Gunicorn processes
PID_FILE_WEB="/tmp/gunicorn_web.pid"
PID_FILE_API="/tmp/gunicorn_api.pid"

# Gunicorn command to start the process, including ports and error logging
GUNICORN_CMD_WEB="gunicorn --bind 0.0.0.0:9595 --daemon --pid $PID_FILE_WEB --error-logfile /tmp/gunicorn_web_error.log"
GUNICORN_CMD_API="gunicorn --bind 0.0.0.0:9596 --daemon --pid $PID_FILE_API --error-logfile /tmp/gunicorn_api_error.log"

# Function to check if a process is running
check_status() {
    local PID_FILE=$1
    local SERVICE_NAME=$2

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "$SERVICE_NAME is running (PID: $PID)"
        else
            echo "$SERVICE_NAME is not running, PID file found, but process is not active"
            rm "$PID_FILE"
        fi
    else
        echo "$SERVICE_NAME is not running"
    fi
}

# Start the Gunicorn process
start_service() {
    local SCRIPT_NAME=$1
    local PID_FILE=$2
    local GUNICORN_CMD=$3

    if [ -f "$PID_FILE" ] && ps -p "$(cat $PID_FILE)" > /dev/null; then
        echo "$SCRIPT_NAME is already running"
    else
        $GUNICORN_CMD "$SCRIPT_NAME" &
        echo "$SCRIPT_NAME has started"
    fi
}

# Stop the Gunicorn process
stop_service() {
    local PID_FILE=$1
    local SERVICE_NAME=$2

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        kill "$PID" 2>/dev/null
        rm "$PID_FILE"
        echo "$SERVICE_NAME has been stopped"
    else
        echo "$SERVICE_NAME is not running"
    fi
}

# Function to execute a Bash script
run_bash_script() {
    local SCRIPT_NAME=$1
    if [ -x "$SCRIPT_NAME" ]; then
        ./"$SCRIPT_NAME"
    else
        echo "The script '$SCRIPT_NAME' is not executable or not found."
    fi
}

# Main logic to select the service and action
case "$1" in
    web)
        case "$2" in
            start)
                start_service "$PYTHON_SCRIPT_WEB" "$PID_FILE_WEB" "$GUNICORN_CMD_WEB"
                ;;
            stop)
                stop_service "$PID_FILE_WEB" "Web service"
                ;;
            status)
                check_status "$PID_FILE_WEB" "Web service"
                ;;
            *)
                echo "Usage: $0 {web|api|update} {start|stop|status}"
                exit 1
                ;;
        esac
        ;;
    api)
        case "$2" in
            start)
                start_service "$PYTHON_SCRIPT_API" "$PID_FILE_API" "$GUNICORN_CMD_API"
                ;;
            stop)
                stop_service "$PID_FILE_API" "API service"
                ;;
            status)
                check_status "$PID_FILE_API" "API service"
                ;;
            token)
                run_bash_script "tokenapi.sh" 
                ;;
            *)
                echo "Usage: $0 {web|api|update} {start|stop|status|token}"
                exit 1
                ;;
        esac
        ;;
    update)
        run_bash_script "update.sh"
        ;;
    *)
        echo "Usage: $0 {web|api|update} {start|stop|status|token}"
        exit 1
        ;;
esac

exit 0
