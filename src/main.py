# Header Comment
# Project: [Garrett's Tracking System] [https://github.com/GreenBeanio/Garrett-s-Tracking-System]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Tracking System] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track a variety of purposes.]
# File Description: [Creates the flask and celery apps.]

# My Imports
from credentials import app_config  # Loads the credentials into an object
from classes.credentials import Config  # The Config object

# My Blueprints
from b_auth.auth import auth_bp

### Package Imports
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from celery import Celery
from celery import Task


# Creating the celery app
def celeryInitApp(flask_app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(flask_app.config["CELERY"])
    celery_app.set_default()
    flask_app.extensions["celery"] = celery_app
    return celery_app


# Creating the flask app (factory no passing name)
def createFlaskApp(config: Config) -> Flask:
    # Load the config
    # Creating the flask app
    flask_app = Flask(__name__)
    flask_app.config.update(Testing=config.testing, SECRET_KEY=config.secret_key)
    # flask_app.config.update(SERVER_NAME="your_domain.com") # Not sure about this yet
    # Add the stuff for celery
    flask_app.config.from_mapping(CELERY=config.celery_dict)
    flask_app.config.from_prefixed_env()
    celeryInitApp(flask_app)
    # Create the dictionary to return
    return flask_app


# Add blueprints to the flask apt
def addBlueprints(app: Flask):
    flask_app.register_blueprint(auth_bp)
    # flask_app.register_blueprint(tracker_bp)
    return app


# Create the apps
flask_app = createFlaskApp(app_config)

# Add the blueprints
flask_app_blue = addBlueprints(flask_app)


# Creating the main index route (Don't know if I want to put this into a blueprint or just leave it here)
@flask_app_blue.get("/")
def index() -> None:
    # # Get information about if the user is logged in
    c_user, auth_status = getUserAuthCookiesStatus(request, app_config)
    # # Returning the welcome page
    return render_template("home.j2", logged_in=auth_status, user=c_user)
    # return jsonify("hi")


# Start the flask app
if __name__ == "__main__":
    # If we're using SSL with Flask (Only use this for testing! On deployment do it through Gunicorn and Nginx)
    if app_config.flask_ssl:
        flask_app_blue.run(
            host=app_config.flask_host,
            port=app_config.flask_port,
            debug=app_config.debug,
            ssl_context=(app_config.flask_cert_file, app_config.flask_key_file),
        )
    # Run Flask without SSL
    else:
        flask_app_blue.run(
            host=app_config.flask_host,
            port=app_config.flask_port,
            debug=app_config.debug,
        )

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
