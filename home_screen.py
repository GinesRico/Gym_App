import flet as ft
from config import image_base_path

def show_home(page, username, history, show_navigation_bar, set_current_user):
    def logout(e):
        global current_user_id, current_username
        current_user_id = None
        current_username = None
        page.navigation_bar = None
        from login_screen import show_login
        show_login(page, history, show_navigation_bar, show_home, set_current_user)

    page.clean()
    logout_button = ft.ElevatedButton(text="Cerrar sesión", on_click=logout)
    page.add(
        ft.Image(src=f"{image_base_path}icon.png", height=400),
        ft.Container(padding=20),
        ft.Text(f"Bienvenido, {username.capitalize()}!"),
        ft.Container(padding=20),
        logout_button
    )
    page.update()

