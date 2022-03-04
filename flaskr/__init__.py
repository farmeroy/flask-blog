import os

from flask import Flask
# this file contains the application factor
# it also tells python that flaskr directory is a package

# create_app is the application factory function
def create_app(test_config=None):
    # create and configure the app
    # create a new instance of Flask
    # __name__ is the current Python module, its location
    # instance_relative_config config files are relative to this folder
    app = Flask(__name__, instance_relative_config=True)
    # default configuration. Secret key should really be secret to deploy
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )
    if test_config is None:
        # load the instance config, if it exits, when not testing
        # this allows us to set a secret key
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # simple hello world
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    # import and call the db app
    from . import db
    db.init_app(app)
    
    # register the auth blueprint
    # this is where we have out views for authentication
    from . import auth
    app.register_blueprint(auth.bp)

    return app
