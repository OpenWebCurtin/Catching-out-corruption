#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # This will load the default settings when no settings settings file has been
    # defined at the command line.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpenWeb.settings')
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpenWeb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()