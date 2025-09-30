import os
import importlib
from flask import Blueprint


# Dynamically import and register all blueprints from the routes directory
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

    @app.route("/", methods=["GET"])
    def index():
        return "Welcome to the API service. Available endpoints: " + ", ".join(
            [f"/api/{bp.name}" for bp in app.blueprints.values()]
        )
