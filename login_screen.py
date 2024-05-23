import flet as ft
from database import get_connection

def show_login(page, history, show_navigation_bar, show_home, set_current_user):
    page.clean()
    page.add(
        ft.Image(src="icon.png", height=400),
        ft.Container(padding=20)
    )

    def login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, ingrese un usuario y una contraseña"))
            page.snack_bar.open = True
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM usuarios WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            page.snack_bar = ft.SnackBar(content=ft.Text("Usuario no registrado"))
        elif user[1] != password:
            page.snack_bar = ft.SnackBar(content=ft.Text("Contraseña incorrecta"))
        else:
            user_id = user[0]
            set_current_user(user_id, username)
            show_navigation_bar()
            show_home(page, username, history, show_navigation_bar, set_current_user)
            return
        
        page.snack_bar.open = True
        page.update()

    def show_register(e=None):
        page.clean()
        page.add(
            ft.Image(src="icon.png", height=400),
            ft.Container(padding=20)
        )

        def register(e):
            username = username_field.value.strip()
            password = password_field.value.strip()

            if not username or not password:
                page.snack_bar = ft.SnackBar(content=ft.Text("El usuario y la contraseña no pueden estar vacíos"))
                page.snack_bar.open = True
                page.update()
                return

            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                page.snack_bar = ft.SnackBar(content=ft.Text("Usuario registrado con éxito"))
                show_login(page, history, show_navigation_bar, show_home, set_current_user)
            except sqlite3.IntegrityError:
                page.snack_bar = ft.SnackBar(content=ft.Text("El nombre de usuario ya existe"))
            conn.close()
            page.snack_bar.open = True
            page.update()

        username_field = ft.TextField(label="Username")
        password_field = ft.TextField(label="Password", password=True)
        register_button = ft.ElevatedButton(text="Register", on_click=register)
        back_to_login_button = ft.TextButton(text="Back to Login", on_click=lambda e: show_login(page, history, show_navigation_bar, show_home, set_current_user))

        page.add(username_field, password_field, register_button, back_to_login_button)
        page.update()

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=login)
    register_button = ft.TextButton(text="Register", on_click=show_register)

    page.add(username_field, password_field, login_button, register_button)
    page.update()
