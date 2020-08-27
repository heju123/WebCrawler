from flask import Blueprint

crawl = Blueprint('crawl', __name__, static_folder="../static",
                 template_folder="../templates")

from . import views