from flask import Blueprint
routes = Blueprint('routes', __name__)

from .HelloWorld import *
from .Home import *
from .Category import *
from .Item import *
from .User import *
