from django.apps import AppConfig
from fsm.fsm import FileSystemManager

class WebsiteConfig(AppConfig):
    name = 'website'
    fs_manager = FileSystemManager()
