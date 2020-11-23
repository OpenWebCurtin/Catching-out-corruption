# Installation

This section describes how to install and configure this webserver. It assumes a 64-bit Ubuntu 16.04 environment.

You can choose to automatically install or to manually install.

## Automatic Installation
To install the OpenWeb project automatically, including any dependencies (Python, Django ...):

1. Clone the project. (git clone <Git URL> <Project Name>)
2. Navigate to the project directory. (cd <Project Name>)
3. Load the setup script into the current shell environment. (source deploy.sh)
4. Done!

## Manual Installation
To install manually, perform all of the following steps.

### Install Pyenv
To install Pyenv from source, run the following command[1]:

  git clone https://github.com/pyenv/pyenv.git ~/.pyenv

Configure Pyenv paths by adding the following code to ~/.bashrc file:

	export PYENV_ROOT="$HOME/.pyenv"
	export PATH="$PYENV_ROOT/bin:$PATH"

The following code will allow autocompletion within the terminal:

	if command -v pyenv 1>/dev/null 2>&1; then
		eval "$(pyenv init -)"
	fi

Refresh your environment variables and aliases by running

	source ~/.bashrc

### Install Python version 3.7.3

Run the following command to install Python 3.7.3:

	pyenv install 3.7.3

(Optional) Run the following command to configure your global Python version to be 3.7.3. This is optional because the .python-version defines the local Python version for the project.

	pyenv global 3.7.3

### Install Django
Run the following command, which should work assuming pyenv was configured correctly in the previous step.

	python -m pip install Django

You can check the version of Django you've installed using:
    
    python
    >>> import django
    >>> django.VERSION
    
You should see (2, 2, 0, 'final', 0).

### Install PostgreSQL
Run the following commands to install the necessary native PostgreSQL libraries[2].

	sudo apt-get install postgresql postgresql-contrib

You can check the version of PostgreSQL using:

    psql --version

You should see psql (PostgreSQL) 9.5.16.

Now that the PostgreSQL database is installed, we need to install a psycopg2, the library to interface between Django and PostgreSQL.

	python -m pip install psycopg2

You can check the version of psycopg2 using:

    pip freeze | grep psycopg2

You should see psycopg2==2.8.2.

### Create web server user and database
Create a database user by running the following commands:

	# Log in as the postgres user
	sudo su - postgres

	# Access the Postgres console.
	psql

	# Create a user account.
	CREATE USER webservice WITH PASSWORD 'CatchTheCorruption96;';

	# Create the database.
	CREATE DATABASE 'corruptioncatcher';

To exit the database terminal press Ctrl+Z. To exit the postgres user enter *exit* twice.

# References
* [1] https://github.com/pyenv/pyenv
* [2] https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

