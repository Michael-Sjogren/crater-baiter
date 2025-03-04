from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from baiter.auth import DiscordAuth


db = SQLAlchemy()
discord = DiscordAuth()
login_manager = LoginManager()
login_manager.login_view = 'main'


def create_app():
    # create the Flask app instance
    app = Flask(__name__)

    # configure app settings and extensions
    app.config.from_object('baiter.config.DevConfig')

    # initialize extensions
    db.init_app(app)
    discord.init_app(app)
    login_manager.init_app(app)

    @app.route('/healthz')
    def healthz():
        return 'OK'

    # Blueprints
    from baiter.main import main_bp
    app.register_blueprint(main_bp)

    # define error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        db.create_all()

    return app
