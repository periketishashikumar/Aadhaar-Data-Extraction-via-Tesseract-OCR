from waitress import serve
from Adhaar_API.wsgi import application  # Ensure this is correct

import logging
logging.basicConfig(level=logging.DEBUG)

print("Starting Waitress server...")

try:
    import warnings
    warnings.filterwarnings("ignore", category=ResourceWarning)

    # Start the server on 0.0.0.0:8281
    serve(application, host='0.0.0.0', port=8281)
    print("Server running on http://0.0.0.0:8281")

except Exception as e:
    print(f"Error starting the server: {e}")
