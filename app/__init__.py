import os
from flask import Flask, send_from_directory
from app.config import config_map
from app.extensions import db, migrate, jwt, cors


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_map.get(config_name, config_map['development']))

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_jwt_callbacks(app)
    register_spa_serve(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})


def register_jwt_callbacks(app):
    from app.models.user import User

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.get(User, identity)


def register_blueprints(app):
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.user import user_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(api_bp, url_prefix='/api')


def register_spa_serve(app):
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_spa(path):
        if os.path.exists(frontend_dist):
            if path and os.path.exists(os.path.join(frontend_dist, path)):
                return send_from_directory(frontend_dist, path)
            return send_from_directory(frontend_dist, 'index.html')
        return '{"success":false,"message":"Frontend not built. Run: cd frontend && npm run build"}'


def register_commands(app):
    from app.seed import seed_command
    app.cli.add_command(seed_command)
