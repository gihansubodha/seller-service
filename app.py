from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Import routes after app is defined
from routes.blanket_routes import *

if __name__ == "__main__":
    app.run(debug=True)
