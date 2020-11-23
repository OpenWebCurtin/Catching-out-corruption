# Assumes we're running from project directory /.
# Assumes we have access to $OPENWEB_USER and $OPENWEB_PATH

# Setup the crontab file.
echo "Setting up Crontab to run jobs..."

echo "# OpenWeb Crontab script." > deploy/crontab
echo "# Attempts to run a job every minute." >> deploy/crontab
echo "*/1 * * * * /bin/bash -c 'cd /home/${OPENWEB_USER}/${OPENWEB_PATH} && ./runjob.sh'" >> deploy/crontab


# Make sure the run script can be executed.
chmod +x runjob.sh

# Register the crontab.
crontab deploy/crontab
