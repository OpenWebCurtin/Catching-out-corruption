# Database
OWNER_USERNAME=postgres
WEB_USERNAME=webservice
WEB_DATABASE_NAME=openweb

WEB_TEST_USERNAME=webservice_test
WEB_TEST_DATABASE_NAME=openweb_test

# ENV_FILE is set in env.sh but may not be defined if this is called separately.
# Set a default value for it.
ENV_FILE=${ENV_FILE:=$HOME/.openweb/environment.sh}

echo "Postgres: Installing."

echo -e "Please enter the desired username and password for the website database access.\nThis is used internally and is not related to website user accounts.\nThe user will be created automatically."
read -p "Username [default: webservice]: " WEB_USERNAME
WEB_USERNAME=${WEB_USERNAME:-webservice}
read -s -p "Password for ${WEB_USERNAME}: " WEB_PASSWORD

echo -e "Please enter the desired username and password for the testing account.\nThis user account is used behind-the-scenes to test database access before the website is moved to production.\nThe user will be created automatically."

read -p "Username [default: webservice_test]: " WEB_TEST_USERNAME
WEB_TEST_USERNAME=${WEB_TEST_USERNAME:-webservice_test}
read -s -p "Password for ${WEB_TEST_USERNAME}: " WEB_TEST_PASSWORD

# Install PostgreSQL.
echo "Postgres: Installing PostgreSQL and dependencies using APT."
sudo apt-get -y install postgresql postgresql-contrib > /dev/null

# Allow refreshing db.
echo "Do you wish to purge existing databases?"
select yn in "Yes" "No"; do
    case $yn in
        Yes)
			# Drop the database.

			# For the following psql commands:
            # 1) We should not specify a psql username (-U) to use the default.
            # 2) The default authentication will be the logged in user,
            #    which in this case is the postgres user.

            # First kill any connections to the database.
            # This is necessary because sometimes even when the web server is not
            # running the connections will persist. Databases cannot be dropped in this
            # state until the connections are terminated.
            # We can do this by restarting the postgres service.
			# Another solution that won't work due to permission issues is described
            # in the following resource:
			# https://stackoverflow.com/a/5408501
            echo "Postgres: Restarting service.";
            sudo service postgresql restart

            # Drop the existing database.
            echo "Postgres: Deleting database $WEB_DATABASE_NAME.";
            sudo -H -i -u postgres psql -c "DROP DATABASE $WEB_DATABASE_NAME" > /dev/null;
            echo "Postgres: Deleting database $WEB_TEST_DATABASE_NAME.";
            sudo -H -i -u postgres psql -c "DROP DATABASE $WEB_TEST_DATABASE_NAME" > /dev/null;
            echo "Postgres: Deleting user $WEB_USERNAME.";
            sudo -H -i -u postgres psql -c "DROP USER IF EXISTS $WEB_USERNAME" > /dev/null;
            echo "Postgres: Deleting user $WEB_TEST_USERNAME.";
            sudo -H -i -u postgres psql -c "DROP USER IF EXISTS $WEB_TEST_USERNAME" > /dev/null;
            break;;
        No)
            break;;
    esac
done

echo "Postgres: Configuring PostgreSQL as user $OWNER_USERNAME."
echo "Postgres: Logging in as $OWNER_USERNAME."

# Log in as the postgres user to...
# ...create the users.
# Breakdown of this command:
# -H sets the $HOME to the postgres home directory, e.g. /var/lib/postgres
# -i makes it interactive mode, required because some commands (i.e. cd) are defined by
# the shell.
# -u postgres - execute command as the postgres user.
# everything else is the command.
echo "Postgres: Creating user $WEB_USERNAME with specified password."
sudo -H -i -u postgres psql -c "CREATE USER $WEB_USERNAME WITH PASSWORD '$WEB_PASSWORD'" > /dev/null

echo "Postgres: Creating user $WEB_TEST_USERNAME with specified password."
sudo -H -i -u postgres psql -c "CREATE USER $WEB_TEST_USERNAME WITH PASSWORD '$WEB_TEST_PASSWORD'" > /dev/null
sudo -H -i -u postgres psql -c "ALTER USER $WEB_TEST_USERNAME CREATEDB" > /dev/null

# ...create databases.
echo "Postgres: Creating database $WEB_DATABASE_NAME."
sudo -H -i -u postgres psql -c "CREATE DATABASE $WEB_DATABASE_NAME" > /dev/null

echo "Postgres: Creating database $WEB_TEST_DATABASE_NAME."
sudo -H -i -u postgres psql -c "CREATE DATABASE $WEB_TEST_DATABASE_NAME" > /dev/null

echo "OPENWEB_DB_USERNAME=$WEB_USERNAME" >> "$ENV_FILE"
export OPENWEB_DB_USERNAME=$WEB_USERNAME
echo "OPENWEB_DB_PASSWORD=$WEB_PASSWORD" >> "$ENV_FILE"
export OPENWEB_DB_PASSWORD=$WEB_PASSWORD

echo "OPENWEB_DB_TEST_USERNAME=$WEB_TEST_USERNAME" >> "$ENV_FILE"
export OPENWEB_DB_TEST_USERNAME=$WEB_TEST_USERNAME
echo "OPENWEB_DB_TEST_PASSWORD=$WEB_TEST_PASSWORD" >> "$ENV_FILE"
export OPENWEB_DB_TEST_PASSWORD=$WEB_TEST_PASSWORD
