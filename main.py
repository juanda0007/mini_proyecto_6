# Created by: Juan David Tabares (19/09/2024)
import fondos, bloques
import pygame
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import user_service
pygame.init()

#Configuración de la pantalla y ventana
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 760
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WINDOW_NAME = pygame.display.set_caption('BODY BUILDER APP')
CLOCK = pygame.time.Clock()
font = pygame.font.Font('horizon.otf', 15)
font2 = pygame.font.Font('horizon.otf', 30)
font3 = pygame.font.Font('horizon.otf', 20)

def create_user():
    """
    - Abre una ventana de diálogo para crear un nuevo usuario.
    - Solicita el nombre de usuario, nombre, grado y contraseña a través de ventanas.
    """
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Nombre de usuario", "Ingrese el nombre de usuario:")
    name = simpledialog.askstring("Nombre", "Ingrese el nombre del usuario:")
    degree = simpledialog.askstring("Grado", "Ingrese el grado académico del usuario:")
    password = simpledialog.askstring("Contraseña", "Ingrese la contraseña del usuario:")
    root.destroy()
    try:
        user_service.create_new_user(username, name=name, degree=degree, password=password)
        messagebox.showinfo("Éxito", f"Usuario '{username}' creado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_user_info():
    """
    - Solicita un nombre de usuario para obtener su información.
    - Muestra la información del usuario en un cuadro de diálogo.
    """
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Buscar usuario", "Ingrese el nombre de usuario:")
    root.destroy()
    try:
        user_info = user_service.get_user_by_username(username)
        if user_info:
            info = f"Nombre: {user_info['name']}\nGrado: {user_info['degree']}\nContraseña: {user_info['password']}"
            messagebox.showinfo(f"Información de {username}", info)
        else:
            messagebox.showwarning("No encontrado", f"No se encontró un usuario con el nombre '{username}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_all_users_info():
    """
    - Muestra la información de todos los usuarios registrados.
    """
    root = tk.Tk()
    root.withdraw()
    try:
        users = user_service.get_all_users()  # Esta función debería ser añadida en el servicio para obtener todos los usuarios
        if users:
            info = ""
            for username, details in users.items():
                info += f"Usuario: {username}\nNombre: {details['name']}\nGrado: {details['degree']}\nContraseña: {details['password']}\n\n"
            messagebox.showinfo("Todos los usuarios", info)
        else:
            messagebox.showwarning("Sin usuarios", "No hay usuarios registrados.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_user_info():
    """
    - Solicita el nombre de usuario para modificar su información.
    - Permite cambiar el nombre, grado y contraseña del usuario.
    """
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Actualizar usuario", "Ingrese el nombre de usuario a modificar:")
    if not username:
        messagebox.showerror("Error", "Debe ingresar un nombre de usuario.")
        return
    name = simpledialog.askstring("Nombre", "Ingrese el nuevo nombre (o deje vacío para no cambiar):")
    degree = simpledialog.askstring("Grado", "Ingrese el nuevo grado (o deje vacío para no cambiar):")
    password = simpledialog.askstring("Contraseña", "Ingrese la nueva contraseña (o deje vacío para no cambiar):")
    root.destroy()
    try:
        user_info = user_service.get_user_by_username(username)
        if not user_info:
            messagebox.showwarning("No encontrado", f"No se encontró un usuario con el nombre '{username}'")
            return
        updated_info = {
            "name": name if name else user_info['name'],
            "degree": degree if degree else user_info['degree'],
            "password": password if password else user_info['password']
        }
        user_service.update_existing_user(username, **updated_info)
        messagebox.showinfo("Éxito", f"Información del usuario '{username}' actualizada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_rutine(fondo):
    """
    Ejecuta una rutina de ejercicios visual en la pantalla con 3 series,
    13 repeticiones por serie y pausas entre ellas, permite al usuario pausar
    y reanudar la rutina con la tecla [P], tambien muestra información de repeticiones,
    series, tiempo transcurrido y descanso.

    Parámetros: (fondo) : Imagen de fondo que se renderiza durante la rutina.
    """
    sets = 3
    repetition = 13
    rest = 30
    total_time = 0
    pause = False
    for serie in range(1, sets + 1):
        running = True
        while running:
            for rep in range(1, repetition + 1):
                SCREEN.blit(fondo, (0, 0))
                mess = font.render("Presiona la tecla [P] para pausar", True, (255, 255, 255))
                SCREEN.blit(mess, (55, 735))
                # Repeticiones
                rep_text = font.render(f"- Repetición {rep} de {repetition}", True, (47, 55, 255))
                SCREEN.blit(rep_text, (150, 625))
                # Series
                serie_text = font2.render(f"Serie {serie} de {sets}", True, (255, 255, 255))
                SCREEN.blit(serie_text, (135, 565))
                # Tiempo
                tiempo_text = font.render(f"Tiempo: {total_time} segundos", True, (255, 87, 87))
                SCREEN.blit(tiempo_text, (150, 675))
                pygame.display.update()

                # Control de pausa
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            pause = not pause
                            while pause:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        running = False
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p:
                                            pause = False
                if not pause:
                    total_time += 1
                    CLOCK.tick(0.38)
            running = False

        if serie < sets:
            rest_time = rest
            while rest_time > 0:
                SCREEN.blit(fondo, (0, 0))
                rest_text = font3.render(f"Descanso: {rest_time} segundos", True, (255, 255, 255))
                SCREEN.blit(rest_text, (80, 615))
                pygame.display.update()
                time.sleep(1)
                rest_time -= 1
                total_time += 1

    SCREEN.blit(fondos.fin, (0, 0))
    finish_text = font3.render("¡Rutina Completada!", True, (0, 255, 0))
    SCREEN.blit(finish_text, (105, 370))
    pygame.display.update()
    time.sleep(3)

current_screen = "inicio"
rutine = ""
coins = 0
clicked = False
on = True
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked:
            if bloques.BOX_START.collidepoint(event.pos) and current_screen == "inicio":
                current_screen = "menu"
                clicked = True
            elif bloques.USERS.collidepoint(event.pos) and current_screen == "inicio":
                current_screen = "users"
                clicked = True
            elif current_screen == "users":
                if bloques.RETURN_BUT.collidepoint(event.pos):
                    current_screen = "inicio"
                elif bloques.AGR_USER.collidepoint(event.pos):
                    create_user()
                elif bloques.INFO_USER.collidepoint(event.pos):
                    view_user_info()
                elif bloques.INFO_USERS.collidepoint(event.pos):
                    view_all_users_info()
                elif bloques.MOD_USER.collidepoint(event.pos):
                    update_user_info()


            elif current_screen == "menu":
                if bloques.BRAZOS_BOTTON.collidepoint(event.pos):
                    current_screen = "brazos"
                    clicked = True
                elif bloques.ABDOMEN_BOTTON.collidepoint(event.pos):
                    current_screen = "abdomen"
                    clicked = True
                elif bloques.PECHO_BOTTON.collidepoint(event.pos):
                    current_screen = "pecho"
                    clicked = True
                elif bloques.PIERNAS_BOTTON.collidepoint(event.pos):
                    current_screen = "piernas"
                    clicked = True
            elif current_screen == "brazos":
                if bloques.E1.collidepoint(event.pos):
                    rutine = "rb1"
                    clicked = True
                elif bloques.E2.collidepoint(event.pos):
                    rutine = "rb2"
                    clicked = True
                elif bloques.E3.collidepoint(event.pos):
                    rutine = "rb3"
                    clicked = True
                elif bloques.E4.collidepoint(event.pos):
                    rutine = "rb4"
                    clicked = True

            elif current_screen == "abdomen":
                if bloques.E1.collidepoint(event.pos):
                    rutine = "ra1"
                    clicked = True
                elif bloques.E2.collidepoint(event.pos):
                    rutine = "ra2"
                    clicked = True
                elif bloques.E3.collidepoint(event.pos):
                    rutine = "ra3"
                    clicked = True
                elif bloques.E4.collidepoint(event.pos):
                    rutine = "ra4"
                    clicked = True

            elif current_screen == "pecho":
                if bloques.E1.collidepoint(event.pos):
                    rutine = "rp1"
                    clicked = True
                elif bloques.E2.collidepoint(event.pos):
                    rutine = "rp2"
                    clicked = True
                elif bloques.E3.collidepoint(event.pos):
                    rutine = "rp3"
                    clicked = True
                elif bloques.E4.collidepoint(event.pos):
                    rutine = "rp4"
                    clicked = True

            elif current_screen == "piernas":
                if bloques.E1.collidepoint(event.pos):
                    rutine = "rpi1"
                    clicked = True
                elif bloques.E2.collidepoint(event.pos):
                    rutine = "rpi2"
                    clicked = True
                elif bloques.E3.collidepoint(event.pos):
                    rutine = "rpi3"
                    clicked = True
                elif bloques.E4.collidepoint(event.pos):
                    rutine = "rpi4"
                    clicked = True

            if current_screen in ["brazos", "abdomen", "pecho", "piernas"]:
                if bloques.BACK_BOTTON.collidepoint(event.pos):
                    current_screen = "menu"
                    clicked = True

            if rutine in ["rb1", "rb2", "rb3", "rb4"]:
                if bloques.BACK_2.collidepoint(event.pos):
                    rutine = ""
                    clicked = True
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rb1":
                    run_rutine(fondos.B1R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rb2":
                    run_rutine(fondos.B2R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rb3":
                    run_rutine(fondos.B3R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rb4":
                    run_rutine(fondos.B4R)
                    coins += 100
            elif rutine in ["ra1", "ra2", "ra3", "ra4"]:
                if bloques.BACK_2.collidepoint(event.pos):
                    rutine = ""
                    clicked = True
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "ra1":
                    run_rutine(fondos.A1R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "ra2":
                    run_rutine(fondos.A2R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "ra3":
                    run_rutine(fondos.A3R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "ra4":
                    run_rutine(fondos.A4R)
                    coins += 100
            elif rutine in ["rp1", "rp2", "rp3", "rp4"]:
                if bloques.BACK_2.collidepoint(event.pos):
                    rutine = ""
                    clicked = True
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rp1":
                    run_rutine(fondos.P1R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rp2":
                    run_rutine(fondos.P2R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rp3":
                    run_rutine(fondos.P3R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rp4":
                    run_rutine(fondos.P4R)
                    coins += 100
            elif rutine in ["rpi1", "rpi2", "rpi3", "rpi4"]:
                if bloques.BACK_2.collidepoint(event.pos):
                    rutine = ""
                    clicked = True
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rpi1":
                    run_rutine(fondos.Pp1R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rpi2":
                    run_rutine(fondos.Pp2R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rpi3":
                    run_rutine(fondos.Pp3R)
                    coins += 100
                elif bloques.RUN_RUTINE.collidepoint(event.pos) and rutine == "rpi4":
                    run_rutine(fondos.Pp4R)
                    coins += 100

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = False

    # IMPLEMENTACIÓN DE FONDOS
    if current_screen == "inicio":
        SCREEN.blit(fondos.SURFACE, (0, 0))

    elif current_screen == "users":
        SCREEN.blit(fondos.USUARIOS, (0, 0))
    elif current_screen == "menu" or current_screen == "brazos" or current_screen == "abdomen" or current_screen == "pecho" or current_screen == "piernas":
        SCREEN.blit(fondos.MENU, (0, 0))
        if current_screen == "brazos":
            SCREEN.blit(fondos.BRAZOS, (0, 0))
            if rutine == "rb1":
                SCREEN.blit(fondos.BE1, (0, 0))
            elif rutine == "rb2":
                SCREEN.blit(fondos.BE2, (0, 0))
            elif rutine == "rb3":
                SCREEN.blit(fondos.BE3, (0, 0))
            elif rutine == "rb4":
                SCREEN.blit(fondos.BE4, (0, 0))

        elif current_screen == "abdomen":
            SCREEN.blit(fondos.ABDOMEN, (0, 0))
            if rutine == "ra1":
                SCREEN.blit(fondos.AE1, (0, 0))
            elif rutine == "ra2":
                SCREEN.blit(fondos.AE2, (0, 0))
            elif rutine == "ra3":
                SCREEN.blit(fondos.AE3, (0, 0))
            elif rutine == "ra4":
                SCREEN.blit(fondos.AE4, (0, 0))

        elif current_screen == "pecho":
            SCREEN.blit(fondos.PECHO, (0, 0))
            if rutine == "rp1":
                SCREEN.blit(fondos.PE1, (0, 0))
            elif rutine == "rp2":
                SCREEN.blit(fondos.PE2, (0, 0))
            elif rutine == "rp3":
                SCREEN.blit(fondos.PE3, (0, 0))
            elif rutine == "rp4":
                SCREEN.blit(fondos.PE4, (0, 0))

        elif current_screen == "piernas":
            SCREEN.blit(fondos.PIERNAS, (0, 0))
            if rutine == "rpi1":
                SCREEN.blit(fondos.PIE1, (0, 0))
            elif rutine == "rpi2":
                SCREEN.blit(fondos.PIE2, (0, 0))
            elif rutine == "rpi3":
                SCREEN.blit(fondos.PIE3, (0, 0))
            elif rutine == "rpi4":
                SCREEN.blit(fondos.PIE4, (0, 0))

    #FPS
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()
