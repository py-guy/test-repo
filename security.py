from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function tht gets called when a user calls the auth endpoint with their username and password.
    :param username:
    :param password:
    :return: A UserModel if authentication was successful, None otherwise.
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identify(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT verified that their authentication
    header is correct.
    :param payload:
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)