from flask import Flask
from routes import register_routes

PORT = 9000
app = Flask(__name__)
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
