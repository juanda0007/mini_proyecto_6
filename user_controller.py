import user_service

def get_user():
    """
    - Prompts the user to input a username and retrieves the user's information.

    Return:
    Prints the user's information if the username is found, otherwise prints a message indicating the user is not registered.
    """
    username = input("Ingrese el nombre del user: ")
    response = user_service.get_user_by_username(username)
    if response:
        print(response)
    else:
        print(f"El usuario {username} no esta registrado")


def create_user_info():
    """
    - Prompts the user to input information for a new user and creates the user.

    Return:
    Prints a success message or raises an exception if the creation fails.
    """
    username = input("Ingrese el nombre del nuevo user: ")
    name = input("Ingrese el nombre: ")
    degree = input("Ingrese el grado: ")
    password = input("Ingrese la contraseña: ")

    try:
        user_service.create_new_user(username, name=name, degree=degree, password=password)
    except Exception as e:
        print(e)

def update_user_info():
    """
    - Prompts the user to input new information for an existing user and updates the user's data.

    Return:
    Prints a success message or raises an exception if the update fails.
    """
    username = input("Ingrese el nombre del user: ")
    name = input("Ingrese el nuevo nombre: ")
    degree = input("Ingrese el nuevo grado: ")
    password = input("Ingrese la nueva contraseña: ")

    try:
        user_service.update_existing_user(username, name=name, degree=degree, password=password)
        print(f"Información del usuario {username} actualizada correctamente.")
    except Exception as e:
        print(e)


def menu():
    message = """\
    Seleccione una opcion:

    1. Obtener informacion de un usuario
    2. Obtener usuarios
    3. Crear usuario
    4. Actualizar informacion del usuario
    5. Salir
    """
    print("-----------------------------")
    print(message)
    print("-----------------------------")

def main():
    """
    """
    flag = True
    user_service.user_repository.load_users()
    while flag:
        menu()
        option = input("Opción: ")

        if option == "1":
            get_user()

        elif option == "2":
            print(user_service.users)

        elif option == "3":
            create_user_info()

        elif option == "4":
            update_user_info()

        elif option == "5":
            flag = False
        else:
            print("Opción no válida")


main()