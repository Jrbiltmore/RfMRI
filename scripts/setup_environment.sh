
# /RfMRI/scripts/setup_environment.sh

#!/bin/bash

# Set up the necessary environment variables
export FLASK_APP="run.py"
export FLASK_ENV="development"
export DATABASE_URI="postgresql://username:password@localhost/rfmri"
export SECRET_KEY="your_secret_key_here"
export LOG_CFG="path_to_logging_configuration_file"

echo "Environment variables set."

# Check for and install any missing dependencies
echo "Installing project dependencies from requirements.txt..."
pip install -r ../requirements.txt

# Initialize the database
echo "Initializing the database..."
python -c 'from src.db.database import init_db; init_db()'

echo "Setup completed successfully."
