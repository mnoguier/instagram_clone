"""Insta485 check for malicous logins etc."""
import uuid
import hashlib
import flask
# import db_funcs
# import insta485


def check_login_status(flask_session: flask.session):
    """
    Pydocstyle summary satisfaction.

    This function will check if the user is logged in.
    If not it will redirect the user to the login page.
    If they are logged in, it will return their username.
    """
    # Check if a user is singed if. Redirect to login page if not
    if 'username' not in flask_session:
        return False

    # # Connect to database
    # connection = insta485.model.get_db()

    # # Check if user exists
    # db_funcs.get_username(connection, flask.session['username'])
    # insta485.model.close_db(False)
    return flask_session['username']


def hash_password(password: str, algo: str, salt: str, use_rando_salt: bool):
    """
    Pydocstyle summary satisfaction.

    This function will check if the user is logged in.
    If not it will redirect the user to the login page.
    If they are logged in, it will return their username.
    """
    alo = algo
    alo += 's'
    algorithm = 'sha512'
    # if we are creating a new password, randomize the salt
    if use_rando_salt:
        salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
