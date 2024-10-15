import os
import json
from users import users

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_PATH, "user.json")

def save_users(new_info):
    """
    - Saves the updated user information to the JSON file.

    Parameters:
    - new_info (dict): A dictionary containing the user information to be saved.
    """
    with open(JSON_PATH, "w") as f:
        json.dump(new_info, f, indent=4)


def load_users():
    """
    - Loads the user information from the JSON file and updates the global 'users' variable.

    Return:
    The updated 'users' dictionary after loading the data from the JSON file.
    """
    global users
    f = open(JSON_PATH, "r")
    users = json.load(f)
    f.close()

    return users


def save_users(new_info):
    """
    - Saves the provided user information to the JSON file.

    Parameters:
    - new_info (dict): A dictionary containing the updated user information.
    """
    f = open(JSON_PATH, "w")
    json.dump(new_info,
              f,
              indent=4)
    f.close()


def get_users(username):
    """
    - Retrieves the user information for the given username.

    Parameters:
    - username (str): The username of the user to retrieve.

    Return:
    The user's information (dictionary) if the user exists, otherwise None.
    """
    return users.get(username)


def create_user(username, user_info):
    """
    What the function does:
    Adds a new user to the 'users' dictionary with the provided information.

    Parameters:
    - username (str): The username of the new user.
    - user_info (dict): The user's information, such as name, degree, and password.

    """
    users[username] = user_info