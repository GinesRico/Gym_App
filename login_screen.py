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
            snack_bar = ft.SnackBar(content=ft.Text("Por favor, ingrese un usuario y una contraseña"))
            page.overlay.append(snack_bar)  # Add the snack bar to the overlay
            snack_bar.open = True
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM usuarios WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            snack_bar = ft.SnackBar(content=ft.Text("Usuario no registrado"))
        elif user[1] != password:
            snack_bar = ft.SnackBar(content=ft.Text("Contraseña incorrecta"))
        else:
            set_current_user(user[0], username)  # Establecer usuario actual
            show_navigation_bar()
            show_home(page, username, history, show_navigation_bar, set_current_user)
            return

        page.overlay.append(snack_bar)  # Add the snack bar to the overlay
        snack_bar.open = True
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
                snack_bar = ft.SnackBar(content=ft.Text("El usuario y la contraseña no pueden estar vacíos"))
                page.overlay.append(snack_bar)  # Add the snack bar to the overlay
                snack_bar.open = True
                page.update()
                return

            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                snack_bar = ft.SnackBar(content=ft.Text("Usuario registrado con éxito"))
                page.overlay.append(snack_bar)  # Add the snack bar to the overlay
                show_login(page, history, show_navigation_bar, show_home, set_current_user)
            except mysql.connector.Error as err:
                snack_bar = ft.SnackBar(content=ft.Text("El nombre de usuario ya existe"))
            cursor.close()
            conn.close()
            snack_bar.open = True
            page.update()

        username_field = ft.TextField(label="Username")
        password_field = ft.TextField(label="Password", password=True)
        register_button = ft.ElevatedButton(text="Register", on_click=register)
        back_to_login_button = ft.TextButton(text="Back to Login", on_click=show_login)

        page.add(username_field, password_field, register_button, back_to_login_button)
        page.update()

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=login)
    register_button = ft.TextButton(text="Register", on_click=show_register)

    page.add(username_field, password_field, login_button, register_button)
    page.update()
