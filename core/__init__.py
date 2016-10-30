from flask import Flask
from gaeopenidstore import NDBOpenIDStore
from flask_openid import OpenID

store_factory = lambda: NDBOpenIDStore()
oid = OpenID(store_factory=store_factory,safe_roots=[])

def create_app(config_name):
    app = Flask(__name__)
    app.config.update(config_name)

    #init apps
    oid.init_app(app)

    #import blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    return app
