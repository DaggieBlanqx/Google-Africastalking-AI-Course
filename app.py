from flask import Flask
from routes import register_routes

import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()

PORT = int(os.getenv("PORT", 9000))  # default 5000 if not set

DEBUG = os.getenv("FLASK_ENV", "production") == "development"

app = Flask(__name__)
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
