import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

def create_app(test_config=None):

    POSTGRES_URL = get_env_variable("AWS_RDS_POSTGRES_URL_FLASK")
    POSTGRES_USER = get_env_variable("AWS_RDS_POSTGRES_USER")
    POSTGRES_PW = get_env_variable("AWS_RDS_POSTGRES_PASSWORD")
    POSTGRES_DB = get_env_variable("AWS_RDS_POSTGRES_DB")

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER,
        pw=POSTGRES_PW,
        url=POSTGRES_URL,
        db=POSTGRES_DB)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	SQLALCHEMY_DATABASE_URI=DB_URL)

    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import posts
    app.register_blueprint(posts.bp)
    app.add_url_rule('/', endpoint='index')
    return app
