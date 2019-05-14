from flask import Blueprint

# 'main' will be the name of the blueprint
main = Blueprint('main', __name__)

@main.route("/")
def index():
    return "Project 1: TODO"