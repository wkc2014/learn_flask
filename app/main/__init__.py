from flask import Blueprint
from app.models import Permission

main = Blueprint('main', __name__)
from . import views

@main.app_context_processor
def inject_permisions():
    return dict(Permission=Permission)