"""
WSGI config for greenenergy_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

# Load environment variables from .env file
load_dotenv()

# Set the default settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenenergy_backend.settings')

# Get the WSGI application
application = get_wsgi_application()
