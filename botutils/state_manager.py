"""wraps all user state management calls"""

def get_user_state(user):
    """
    gets the current state of the user from persistence
    :param user:
    :return:
    """
    return "IDLE"

def save_user_state(user, state):
    """
    saves the current state of the user to persistence
    :param user:
    :param state:
    :return:
    """
    pass