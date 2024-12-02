import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfit.settings')

application = get_wsgi_application()

# Use WhiteNoise to serve static files
from whitenoise import WhiteNoise
application = WhiteNoise(application, root='C:/Users/reymel mislang/OneDrive/Desktop/jobfit/staticfiles')

# Run the server on 0.0.0.0 and the port specified in the environment variable, defaulting to 5000
port = os.environ.get('PORT', 5000)
serve(application, host='0.0.0.0', port=port)
