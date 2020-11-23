# ENV_FILE is set in env.sh but may not be defined if this is called separately.
# Set a default value for it.
ENV_FILE=${ENV_FILE:=$HOME/.openweb/environment.sh}

echo "Setting up the email verification system for account creation."
echo "Please create a Gmail account for the OpenWeb project and provide the details."
echo "This account will be used to send email verifications."

read -p "Email (Gmail only): " EMAIL
echo "Please enable 2FA and generate an app password for your Google account."
read -s -p "App Password: " APP_PW

echo "# Email verification." >> $ENV_FILE
echo "OPENWEB_EMAIL_USE_TLS=True" >> $ENV_FILE
echo "OPENWEB_EMAIL_HOST='smtp.gmail.com'" >> $ENV_FILE
echo "OPENWEB_EMAIL_HOST_USER=$EMAIL" >> $ENV_FILE
echo "OPENWEB_EMAIL_PORT=587" >> $ENV_FILE
echo "OPENWEB_EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'" >> $ENV_FILE
echo "OPENWEB_EMAIL_HOST_PASSWORD=$APP_PW" >> $ENV_FILE

set -a
source $ENV_FILE
set +a
