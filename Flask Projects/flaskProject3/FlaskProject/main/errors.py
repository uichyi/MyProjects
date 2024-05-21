from flask import render_template
from . import main


@main.errorhandler(418)
def teapot_error(e):
    return render_template("errors/418err.html"), 418
