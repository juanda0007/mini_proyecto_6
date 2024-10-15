import user_repository
from users import users

def get_all_users():
    """
    - Carga y devuelve todos los usuarios registrados.

    Return:
    Un diccionario con todos los usuarios registrados.
    """
    return user_repository.load_users()

def get_user_by_username(username):
    """
    - Retrieves user information from the repository based on the provided username.

    Parameter:
    - username (str): The username of the user to retrieve.

    Return:
    The user's information (dictionary) from the repository, if found.
    """
    return user_repository.get_users(username)

def create_new_user(username, **kwargs):
    """
    - Creates a new user with the given username and other information (name, degree, password).

    Parameters:
    - username (str): The username for the new user.
    - **kwargs: Additional user information, including 'name', 'degree', and 'password'.

    Return:
    Raises an exception if the user already exists or if the information is not in the expected format.
    """
    if username in users:
        raise Exception(f"User {username} already exists")

    if len(kwargs) != 3:
        raise Exception(f"The user information does not have the expected structure")

    cond = all([kwargs.get(key) for key in ["name", "degree", "password"]])

    if not cond:
        raise Exception(f"The user information does not have the expected structure")

    users[username] = kwargs
    user_repository.save_users(users)
    print(f"User {username} created successfully.")


def update_existing_user(username, **kwargs):
    """
    - Updates the information of an existing user with the provided username.

    Parameters:
    - username (str): The username of the user to update.
    - **kwargs: Updated user information, including 'name', 'degree', and 'password'.

    Return:
    Raises an exception if the user is not registered or if the information is not in the expected format.
    """
    if username not in users:
        raise Exception(f"User {username} is not registered")

    cond = all([kwargs.get(key) for key in ["name", "degree", "password"]])

    if not cond:
        raise Exception(f"The user information does not have the expected structure")

    users[username] = kwargs
    user_repository.save_users(users)

    print(kwargs)
