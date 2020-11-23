# From https://code.djangoproject.com/wiki/SplitSettings
# In order to enable multiple environments, permit multiple "split" settings
# files which are selectively loaded at runtime.

# Django project settings loader
import os

import importlib


# Environment can be production or test.
ENV_NAME=os.environ.get('OPENWEB_ENVIRONMENT') or 'production'

# Different configuration files.
config_paths = {
    'production': 'default',
    'test': 'test'
}

# Import the configuration file.
module_path = 'OpenWeb.config.%s' % (config_paths[ENV_NAME],)

config_module = importlib.import_module(module_path)

#config_module = __import__('OpenWeb.settings.%s' % settings_paths[ENVIRONMENT_NAME],
#    globals(), locals(), 'OpenWeb')

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)
