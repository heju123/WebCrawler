from flask import Blueprint

crawler = Blueprint('crawler', __name__, static_folder="../static",
                 template_folder="../templates")

from . import views