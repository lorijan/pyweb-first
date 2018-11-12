import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    '''
    __name__ is the name of the current Python module. The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.

    instance_relative_config=True tells the app that configuration files are relative to the instance folder.
    The instance folder is located outside the myapp package and can hold local data that shouldn’t be committed to version control,such as configuration secrets and the database file.
    '''
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myapp.sqlite'),
    )
    '''
    SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during development, but it should be overridden with a random value when deploying.
    DATABASE is the path where the SQLite database file will be saved. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder.
    '''
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        '''
        overrides the default configuration with values taken from the config.py file in the instance folder if it exists. For example, when deploying, this can be used to set a real SECRET_KEY.
        '''
    else:
        # load an alternative test config, bypassing congig.py
        app.config.from_mapping(test_config)


    # ensure the instance folder exists
    '''
    Flask doesn’t create the instance folder automatically, but it needs to be created because your project will create the SQLite database file there.
    '''
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    return app
