# Header Comment
# Project: [Garrett's Tracking System] [https://github.com/GreenBeanio/Garrett-s-Tracking-System]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Tracking System] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track a variety of purposes.]
# File Description: [The auth blueprint for flask]

# My imports
from credentials import app_config  # Loads the saved credentials

# Imports
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import make_response
from flask import url_for
from flask import flash
from markupsafe import escape

# Create the blueprint
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/auth",
    url_prefix="/user",
)


# Creating the new user page
@auth_bp.get("/new-user")
def newUser():
    session["User"] = "test"
    print(session)
    session.update()
    print(session)
    return request.cookies


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
