import json
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_PATH, "user.json")
users = {}


def load_users_from_json():
    """
    - Loads user data from a JSON file and returns it as a dictionary.

    return:
    A dictionary with the user data loaded from the JSON file.
    """
    with open(JSON_PATH, "r") as json_file:
        data = json.load(json_file)
    return data


users = load_users_from_json()
