import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    database_path = os.path.join(app.instance_path, 'app.sqlite')
    if os.environ.get('VERCEL'):
        database_path = '/tmp/app.sqlite'

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=database_path,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

        os.makedirs(app.instance_path, exist_ok=True)

    os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    if os.environ.get('VERCEL'):
        with app.app_context():
            db.ensure_db()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import task
    app.register_blueprint(task.bp)
    app.add_url_rule('/', endpoint='index')

    return app