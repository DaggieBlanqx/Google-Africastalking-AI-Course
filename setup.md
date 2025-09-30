Step 1: Create project folder

In your terminal:

```bash
mkdir at-ai
cd at-ai
```

Step 2: Create and activate a virtual environment

```bash
python3 -m venv venv
# Activate it
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows PowerShell
```

Step 3: Install dependencies

```bash
pip install flask
```

Step 4: Create the folder structure
at-ai/
│
├── app.py
└── routes/
    ├── __init__.py
    ├── airtime.py
    ├── sms.py
    ├── voice.py
    ├── simswap.py
    └── ussd.py


```bash

mkdir routes
touch app.py
touch routes/__init__.py routes/airtime.py routes/sms.py routes/voice.py routes/simswap.py routes/ussd.py
```

Step 5: app.py
- This is the main entry point of your Flask application.
- It needs to import the route modules and register them with the Flask app.
- However we will simplify by making routes auto-discovered as long as they are in the routes folder and have a blueprint defined.

```python
from flask import Flask
from routes import register_routes

PORT = 9000
app = Flask(__name__)
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)

```

Step 6: routes/__init__.py
- This file will handle the automatic registration of all route modules in the routes folder.

```python
import os
import importlib
from flask import Blueprint

def register_routes(app):
    routes_dir = os.path.dirname(__file__)

    for filename in os.listdir(routes_dir):
        if filename.startswith("__") or not filename.endswith(".py"):
            continue

        module_name = f"routes.{filename[:-3]}"
        module = importlib.import_module(module_name)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                prefix = f"/api/{attr.name}"
                app.register_blueprint(attr, url_prefix=prefix)
                print(f"✅ Registered {attr.name} at {prefix}")

```

Step 7: Example route file (sms.py)
- Each route file will define a Flask Blueprint and its routes.
- Ensure each blueprint has a unique name and that it uses the convention of ``*_bp`` for the blueprint variable.

```python
from flask import Blueprint, jsonify, request

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/", methods=["GET"])
def get_sms_status():
    return jsonify({"service": "sms", "status": "ready"})

@sms_bp.route("/send", methods=["POST"])
def send_sms():
    data = request.get_json()
    to = data.get("to")
    message = data.get("message")

    if not to or not message:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    return jsonify({
        "service": "sms",
        "action": "send",
        "to": to,
        "message": message,
        "status": "sent"
    })

```

(Repeat Step 7 for other route files: airtime.py, voice.py, simswap.py, ussd.py etcetera)

Step 8: Run the server

```bash
python app.py
```

The expected output should show that all routes have been registered:

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:9000
 * Running on http://192.168.8.91:9000
Press CTRL+C to quit
 * Restarting with stat
✅ Registered sms at /api/sms
 * Debugger is active!
 * Debugger PIN: 542-650-670

```

Step 9: Test endpoints

Open a browser or use curl/Postman to test:
- http://localhost:9000/api/sms/

For example:
- If use a terminal command to GET the SMS endpoint:

```bash
curl -X GET http://127.0.0.1:9000/api/sms/
```

It will return:

```json
{"service":"sms","status":"ready"}
```

- If you use a terminal command to POST to the SMS send endpoint:

```bash
curl -X POST http://127.0.0.1:9000/api/sms/send -H "Content-Type: application/json" -d '{"to":"+254700123456","message":"Hello"}'
```

It should return the expected JSON responses.

```bash
{
  "action": "send",
  "message": "Hello",
  "service": "sms",
  "status": "sent",
  "to": "+254700123456"
}
```

Step 10: Expose the local server (optional) to the internet
- We can use a tool like ngrok to expose the local server to the internet for testing webhooks.
E.g Ngrok, LocalTunnel, Cloudflare Tunnel etcetera.

- For ngrok, after installing it, run:
```bash
ngrok http 9000
```

- For LocalTunnel, after installing it, run:
```bash
lt --port 9000
```

- For Cloudflare Tunnel, after installing it, run:
```bash
cloudflared tunnel --url http://localhost:9000
```

Step 11: Wrapping into a Makefile (optional)
- Create a Makefile to simplify common tasks like running the server and installing dependencies.

```bash
touch Makefile
```

- Then add the following content to the Makefile:

```Makefile

PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

dev:
	FLASK_ENV=development $(PYTHON) app.py

run:
	$(PYTHON) app.py

tunnel:
	ngrok http 9000

```

- Then create a requirements.txt (if it doesn't exist) file to track dependencies:

```bash
touch requirements.txt
```

- Inside requirements.txt, add:

```txt
flask=3.0.2
requests==2.32.3
```

- Then you can use it as follows:

```bash
make run
make dev
make tunnel
```

Step 12: Create a .gitignore file (optional but recommended)
- To avoid committing unnecessary files to version control, create a .gitignore file.
```bash
touch .gitignore
```

- Add the following content to .gitignore:

```
venv/ # Ignore virtual environment folder
.env # Ignore environment variable files
```

Step 13: Create .env.example file (optional but recommended)
- To provide a template for environment variables, create a .env.example file.
```bash
touch .env.example
```

- Add the following content to .env.example:

```
# Flask configuration
FLASK_ENV=development
PORT=9000

# Ngrok / Cloudflared
NGROK_AUTHTOKEN=your-ngrok-auth-token-here

# Africastalking API credentials
USERNAME=your-AT-username-here
API_KEY=your-AT-api-key-here

```

Step 14: Clone .env.example to .env (optional)
- Create a .env file from the .env.example file to store your actual environment variables.
```bash
cp .env.example .env
```

Step 15: Initialize a Git repository (optional)
- If you want to use version control, initialize a Git repository and make your first commit.
```bash
git init
git add .
git commit -m "Initial commit - setup Flask project with dynamic routing"
```

Step 16: Next Steps
- Implement actual logic in each route file to interact with the Africastalking API.
- Add error handling and logging as needed.