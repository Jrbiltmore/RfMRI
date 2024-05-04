
# /RfMRI/deploy/deploy_script.sh

#!/bin/bash

# Define deployment directories and variables
APP_DIR="/var/www/rfmri"
LOG_DIR="/var/log/rfmri"
CONFIG_DIR="/etc/rfmri"
VENV_PATH="/var/www/rfmri/venv"

# Ensure necessary directories exist
mkdir -p $APP_DIR
mkdir -p $LOG_DIR
mkdir -p $CONFIG_DIR

echo "Directories created or verified."

# Set permissions for the log directory
chown www-data:www-data $LOG_DIR
chmod 755 $LOG_DIR

echo "Permissions set for log directory."

# Check if virtual environment exists and create it if not
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_PATH
    echo "Virtual environment created."
fi

# Activate virtual environment
source $VENV_PATH/bin/activate

# Install or update Python dependencies
echo "Installing/updating Python dependencies..."
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

# Copy configuration files to the appropriate directory
cp $APP_DIR/config/production.py $CONFIG_DIR/production_config.py

echo "Configuration files copied."

# Initialize the database, migrate, and upgrade to the latest version
echo "Initializing database..."
python $APP_DIR/src/db/database.py init_db
python $APP_DIR/src/db/database.py migrate
python $APP_DIR/src/db/database.py upgrade

echo "Database initialized and updated."

# Start the Gunicorn server to serve the Flask app
echo "Starting Gunicorn server..."
gunicorn --workers 4 --bind unix:$APP_DIR/rfmri.sock -m 007 wsgi:app

echo "Deployment completed successfully."
    