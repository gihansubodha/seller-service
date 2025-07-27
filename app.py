from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Import routes after app is defined
from routes.blanket_routes import *

if __name__ == "__main__":
    # Render requires host="0.0.0.0" and port from environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
