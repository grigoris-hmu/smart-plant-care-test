from flask import Blueprint

crop = Blueprint('crop', __name__, template_folder='templates')

from . import routes