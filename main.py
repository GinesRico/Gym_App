import flet as ft
from config import image_base_path
from database import initialize_database, get_connection
from login_screen import show_login
from home_screen import show_home
from exercises_screen import body_screen, show_exercises
from trainings_screen import show_trainings  # Actualizar el nombre de la función para entrenamientos
from tmb_get_screen import show_tmb_get_screen  # Importar la nueva pantalla

initialize_database()

current_user_id = None  # Variable global para el ID del usuario actual
current_username = None  # Variable global para el nombre de usuario actual

def main(page: ft.Page):
    global current_user_id, current_username

    page.title = "Ejercicios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    history = []

    def show_navigation_bar():
        page.navigation_bar = ft.CupertinoNavigationBar(
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.BLACK,
            on_change=nav_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.icons.SPORTS_GYMNASTICS_ROUNDED, label="Ejercicios"),
                ft.NavigationBarDestination(icon=ft.icons.STAR, label="Entrenamientos"),  # Actualizar el nombre del botón
                ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="TMB & GET"),  # Añadir nuevo botón
                ft.NavigationBarDestination(icon=ft.icons.ARROW_BACK, label="Atrás")
            ]
        )
        page.update()

    def go_back(e):
        if history:
            last_action = history.pop()
            last_action()
        else:
            show_home(page, current_username, history, show_navigation_bar, set_current_user)

    def nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.appbar = None
            history.append(lambda: show_home(page, current_username, history, show_navigation_bar, set_current_user))
            show_home(page, current_username, history, show_navigation_bar, set_current_user)
        elif selected_index == 1:
            page.appbar = None
            history.append(lambda: body_screen(page, current_user_id, current_username, history))
            body_screen(page, current_user_id, current_username, history)
        elif selected_index == 2:
            page.appbar = None
            history.append(lambda: show_trainings(page, current_user_id, history))
            show_trainings(page, current_user_id, history)
        elif selected_index == 3:
            page.appbar = None
            history.append(lambda: show_tmb_get_screen(page))
            show_tmb_get_screen(page)
        elif selected_index == 4:
            go_back(None)

    show_login(page, history, show_navigation_bar, show_home, set_current_user)

def set_current_user(user_id, username):
    global current_user_id, current_username
    current_user_id = user_id
    current_username = username

ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)
