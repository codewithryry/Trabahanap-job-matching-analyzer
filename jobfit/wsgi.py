"""
WSGI config for jobfit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""



import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfit.settings')

application = get_wsgi_application()

# Serve static files using WhiteNoise
application = WhiteNoise(application)

# Optionally, specify the static files location (already handled by STATIC_ROOT in settings.py)
application.add_files(os.path.join(os.getcwd(), 'staticfiles'), prefix='static/')
