from flask import Blueprint, g, redirect, url_for
from functools import wraps

auth = Blueprint('auth', __name__)

from . import routes

def login_required(view_func):
    def _decorator(*args, **kwargs):
        if not g.user:
            return  redirect(url_for("auth.index"))
        return view_func(*args, **kwargs)
    return wraps(view_func)(_decorator)