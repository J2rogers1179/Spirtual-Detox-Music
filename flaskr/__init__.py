import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),  # Secure key from environment or default to 'dev'
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints and initialize components
    from . import auth, db
    app.register_blueprint(auth.bp)
    db.init_app(app)
    from . import route
    
    # Register the Blueprint
    app.register_blueprint(route.site)

    return app

    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler('logs/flaskr.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flaskr startup')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Assuming db.session is your database session
        return render_template('500.html'), 500

    # Example page for testing purposes
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app