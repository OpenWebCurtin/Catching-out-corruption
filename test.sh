source .venv/bin/activate
OPENWEB_ENVIRONMENT=test source deploy/test.sh
OPENWEB_ENVIRONMENT=test python manage.py test
deactivate
