# This script will automatically set up the testing environment including
# - setting environment variables
# - database creation and configuration
# To use it, run the following from the project's root directory.
#   source deploy/test.sh

# Set up the database.
# Assume most of the configuration has already been done.
source "$HOME/.openweb/environment.sh"
#source "deploy/setup/env.sh"
#source "deploy/setup/python.sh"
#source "deploy/setup/db.sh"
#source "deploy/setup/driver.sh"
#source "deploy/setup/django-reset.sh"
source "deploy/setup/django.sh"
#source "deploy/setup/django-seed.sh"
#source "deploy/setup/nginx.sh"
#source "deploy/setup/email.sh"

export $OPENWEB_DB_TEST_USERNAME
export $OPENWEB_DB_TEST_PASSWORD
