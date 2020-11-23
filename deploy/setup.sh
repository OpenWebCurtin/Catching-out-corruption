# This script will automatically set up the server including
# - setting environment variables
# - database creation and configuration
# To use it, run the following from the project's root directory.
#   source deploy/setup.sh

# Set up the database.
source "deploy/setup/env.sh"
source "deploy/setup/python.sh"

# Now that venv has been set up, we can start using it.
source .venv/bin/activate
source "deploy/setup/db.sh"
source "deploy/setup/driver.sh"
source "deploy/setup/pdfminer.sh"
source "deploy/setup/spacy.sh"
source "deploy/setup/django-reset.sh"
source "deploy/setup/django.sh"
source "deploy/setup/django-seed.sh"
source "deploy/setup/nginx.sh"
source "deploy/setup/email.sh"
source "deploy/setup/cron.sh"

export $OPENWEB_DB_USERNAME
export $OPENWEB_DB_PASSWORD

deactivate
