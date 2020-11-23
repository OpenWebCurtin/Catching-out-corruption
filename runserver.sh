# This file is for running the web server on-demand.
# It bypasses Nginx and starts the web server directly.

# Ensure we're working in the virtual environment.
source .venv/bin/activate

# Get the variables declared in the environment settings file.
# We need to use set -a and set +a to toggle whether we export
# variables by default (i.e. without an export statement).
# Otherwise we would need export statements for each of the
# settings, and systemd service <EnvironmentFile> parameter
# does not work with shell files (i.e. export causes errors).
# So this is the ideal solution.
set -a
source $HOME/.openweb/environment.sh
set +a

# Run the web server.
gunicorn --bind 0.0.0.0:8000 OpenWeb.wsgi:application

# Finished: end the virtual environment session.
deactivate
