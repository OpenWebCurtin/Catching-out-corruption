source .venv/bin/activate

# Record the results of this execution.
# Based on the following reference:
# https://stackoverflow.com/a/17066323
timestamp=$( date +%T )

# Load the passwords etc.
set -a; source $HOME/.openweb/environment.sh; set +a;

# Print the timestamp but don't print newline to allow the Django command to
# provide a job ID.
echo -n "[${timestamp}] Running job: " >> cron.log

# Run the management command. This should produce a job ID (on stdout) as well as
# any relevant diagnostic information (optional).
python manage.py runjob >> cron.log

deactivate
