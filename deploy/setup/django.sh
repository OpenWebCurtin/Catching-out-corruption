
# Use Pip to install the Django module.
python -m pip install Django

# Assume this is being run in the project's root, so the manage.py script is in the current directory.

# For some reason Django chooses not to migrate the project apps.
# Do this manually.
python manage.py makemigrations website
python manage.py makemigrations database
python manage.py makemigrations esp
python manage.py makemigrations pdfparser

# Create the migrations for the models, if necessary.
python manage.py makemigrations

# Perform the migrations.
python manage.py migrate

