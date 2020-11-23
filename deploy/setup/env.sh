# Where to link the environment variables.
SYS_ENV=$HOME/.bash_profile

# Where to store project-specific settings.
SETTINGS_DIR=$HOME/.openweb
ENV_FILE=$SETTINGS_DIR/environment.sh
PYENV_DIR=$HOME/.pyenv

DO_SETTINGS=true

# Depending on the user's system, some libraries won't be available.
# This can cause pyenv to fail when building Python.
# Install these now.
echo "Installing library dependencies for pyenv."
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git > /dev/null

while [ $? -ne 0 ]; do
    echo "Could not install dependent packages."
    echo "This could be due to apt locking the resources temporarily."
    echo "Trying again in 5 seconds."
    sleep 5

    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git > /dev/null
done;

#    echo "Could not install dependent libraries. Trying again in 5 seconds. Apt might be locking the resources."
#    sleep 5
#    result=`sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git`
#done;

echo "Environment: Setting up."
# Set up the OpenWeb settings directory.
echo "Environment: Creating $SETTINGS_DIR."
if [ ! -d "$SETTINGS_DIR" ]; then
    mkdir "$SETTINGS_DIR"
else
    echo "Environment: Directory $SETTINGS_DIR already exists."
fi

echo "Environment: Creating $ENV_FILE."
if [ -f $ENV_FILE ]; then
    echo "Environment: Settings file $ENV_FILE already exists. Overwrite?"

    select yn in "Yes" "No"; do
        case $yn in 
            Yes)
                DO_SETTINGS=true
                break;;
            No)
                DO_SETTINGS=false
                break;;
        esac
    done
fi

if [ "$DO_SETTINGS" = true ]; then
    # Blank the existing settings if one exists.
    # Else, create it.
    echo "# Settings file for the OpenWeb project." > $ENV_FILE
fi

# Add the environment settings to bashrc so that it may be loaded on
# subsequent logins. Otherwise things like database access (which requires
# username & password environment variables) will not be available.
# We do this here because if we wait for pyenv to install, there is a chance
# that pyenv will encounter an existing install, prompt the user to reinstall,
# and if the user answers with no the entire shell script is exited.
echo "Linking environment settings file from bashrc."
echo "# Import environment variables for the OpenWeb project." >> $SYS_ENV
echo "set -a; source $ENV_FILE; set +a;" >> $SYS_ENV

# We need to know if pyenv has installed in a previous run.
# Because it seems the presence of ~/.pyenv is not reliable.
source $ENV_FILE

echo "Pyenv: Setting up."
# Is Pyenv installed and configured?
if [ ! -d "$PYENV_DIR" -o ! "$PYENV_INSTALLED" = true ]; then
    # Install pyenv to allow easy management of Python and extensions.
    #git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo "Pyenv: Installing to ${PYENV_DIR}."
    git clone https://github.com/pyenv/pyenv.git $PYENV_DIR

    echo "Pyenv: Configuring environment variables."
    # Set the environment variables for pyenv.
    echo "PYENV_ROOT=\"$PYENV_DIR\"" >> $SYS_ENV
    # ... and add it to the path.
    echo "PATH=\"\$PYENV_ROOT/bin:\$PATH\"" >> $SYS_ENV

    # Enable shims and bash autocompletion.
    echo "Pyenv: Configuring autocompletion."
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> $SYS_ENV
    echo "PYENV_INSTALLED=true" >> $SYS_ENV
    source $SYS_ENV
else
    echo "Pyenv: Installation already exists at ${PYENV_DIR}."
    echo "Pyenv: Exiting."
fi

if [ ! $PYENV_INSTALLED ]; then
    echo "Error: Pyenv did not install correctly."
fi

set -a
source $ENV_FILE
#source $SYS_ENV
set +a
