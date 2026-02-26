# WSGI configuration for EduQuP on PythonAnywhere
# This file should be placed at: /var/www/votre-username_pythonanywhere_com_wsgi.py

import os
import sys

# Add your project directory to the sys.path
project_home = '/home/votre-username/edututor'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to tell django where to find settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'edututor_ai.settings'

# Activate your virtualenv (if using one)
activate_this = '/home/votre-username/.virtualenvs/edututor/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import django and start WSGI application
import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()