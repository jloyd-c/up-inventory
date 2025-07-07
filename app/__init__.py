from flask import Flask

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')

    from app.inventory.routes import inventory_bp
    app.register_blueprint(inventory_bp)

    return app
