from waitress import serve
from jobfit.wsgi import application  
import os

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)  # Use the PORT environment variable if available, default to 5000
    serve(application, host='0.0.0.0', port=port)
