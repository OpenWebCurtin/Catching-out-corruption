echo "Setting up Nginx and Gunicorn."

sudo apt-get -y install nginx

# Install Gunicorn
python -m pip install gunicorn

# Copy the configuration.
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/systemd/system/gunicorn
sudo mkdir -p /etc/tmpfiles.d

# Navigate to the template directory, get the relative files, and go back to the
# current working directory.
DIR_PREV=`pwd`
cd deploy/templates
FILES=`find * -type f`
cd $DIR_PREV

# This can be used for testing before files get overwritten.
# For deployment, this would be set to empty.
OUT_DIR=

# List of parameters that will be expanded.
LIST_ARGS="OPENWEB_USER OPENWEB_PATH OPENWEB_DOMAIN_NAME OPENWEB_PORT"

OPENWEB_USER=$USER

read -p "Where is the path [/home/$USER/openweb]? /home/$USER/" OPENWEB_PATH
OPENWEB_PATH=${OPENWEB_PATH:-openweb}

read -p "Domain name for the website [localhost]: " OPENWEB_DOMAIN_NAME
OPENWEB_DOMAIN_NAME=${OPENWEB_DOMAIN_NAME:-localhost}

read -p "Port for the web server [8080]: " OPENWEB_PORT
OPENWEB_PORT=${OPENWEB_PORT:-8080}

ARG_STR=''

for file in $FILES; do
    # Make files along the directory of the output path.
    mkdir -p $OUT_DIR/$(dirname $file)

    # Build the parameters to sed.
    for arg in $LIST_ARGS; do
        ARG_STR+='-e s/${'$arg'}/'${!arg}'/g '
    done;

    # Replace all the variables.
    sed $ARG_STR deploy/templates/$file > deploy/tmp
    sudo mv deploy/tmp $OUT_DIR/$file
done;

# The default sites-available might conflict with the website depending
# upon its settings.
sudo rm /etc/nginx/sites-available/default

# Create a symlink in the sites-enabled so that changes in sites-available are
# automatically reflected in sites-enabled.
sudo ln -s /etc/nginx/sites-available/openweb.conf \
    /etc/nginx/sites-enabled/openweb.conf

echo "Configuring Gunicorn socket to start listening automatically."
sudo systemctl enable gunicorn.socket

echo "Starting Gunicorn socket."
sudo systemctl start gunicorn.socket

echo "Restarting Nginx web server."
sudo systemctl restart nginx
