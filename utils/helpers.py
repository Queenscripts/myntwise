from flask import redirect, render_template, request, session
from functools import wraps


def login_auth(u): 
    """ Authentican validation for user login 
        http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(u)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") == None: 
            return redirect("/login")
        return u(*args, **kwargs)
    return decorated_function