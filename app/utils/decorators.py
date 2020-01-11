from functools import wraps

from flask import flash, render_template, abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            abort(401)

        return f(*args, **kwargs)

    return decorated_function
