import flet as ft
import sqlite3
import os

# Ruta de la imagen
image_base_path = "C:/Users/gines/OneDrive/Documentos/Gym_App/Gym_App/assets"
bd_path = "C:/Users/gines/OneDrive/Documentos/Gym_App/Gym_App/assets/datos_ejercicios.db"

# Conectar a la base de datos y crear tablas si no existen
def initialize_database():
    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT
    )
    """)

    # Verificar si la tabla de favoritos tiene las columnas correctas
    cursor.execute("PRAGMA table_info(favoritos)")
    columns = [info[1] for info in cursor.fetchall()]
    if "user_id" not in columns or "ejercicio_id" not in columns:
        cursor.execute("DROP TABLE IF EXISTS favoritos")
        cursor.execute("""
        CREATE TABLE favoritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            ejercicio_id INTEGER, 
            FOREIGN KEY (user_id) REFERENCES usuarios(id), 
            FOREIGN KEY (ejercicio_id) REFERENCES datos(id)
        )
        """)
    conn.close()

initialize_database()

current_user_id = None  # Variable global para el ID del usuario actual
current_username = None  # Variable global para el nombre de usuario actual

def main(page: ft.Page):
    page.title = "Ejercicios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    history = []

    def show_login(e=None):
        page.clean()
        page.add(
            ft.Image(src="icon.png", height=400),
            ft.Container(padding=20)
        )

        def login(e):
            global current_user_id, current_username
            username = username_field.value.strip()
            password = password_field.value.strip()

            if not username or not password:
                page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, ingrese un usuario y una contraseña"))
                page.snack_bar.open = True
                page.update()
                return

            conn = sqlite3.connect(bd_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM usuarios WHERE username=?", (username,))
            user = cursor.fetchone()
            conn.close()

            if not user:
                page.snack_bar = ft.SnackBar(content=ft.Text("Usuario no registrado"))
            elif user[1] != password:
                page.snack_bar = ft.SnackBar(content=ft.Text("Contraseña incorrecta"))
            else:
                current_user_id = user[0]
                current_username = username
                show_navigation_bar()
                show_home()
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

                conn = sqlite3.connect(bd_path)
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    page.snack_bar = ft.SnackBar(content=ft.Text("Usuario registrado con éxito"))
                    show_login()
                except sqlite3.IntegrityError:
                    page.snack_bar = ft.SnackBar(content=ft.Text("El nombre de usuario ya existe"))
                conn.close()
                page.snack_bar.open = True
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

    def show_navigation_bar():
        page.navigation_bar = ft.CupertinoNavigationBar(
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.BLACK,
            on_change=nav_change,
            destinations=[
                ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Inicio"),
                ft.NavigationDestination(icon=ft.icons.SPORTS_GYMNASTICS_ROUNDED, label="Ejercicios"),
                ft.NavigationDestination(icon=ft.icons.STAR, label="Favoritos"),
                ft.NavigationDestination(icon=ft.icons.ARROW_BACK, label="Atrás")
            ]
        )
        page.update()

    def show_home(e=None):
        def logout(e):
            global current_user_id, current_username
            current_user_id = None
            current_username = None
            page.navigation_bar = None
            show_login()

        page.clean()
        logout_button = ft.ElevatedButton(text="Cerrar sesión", on_click=logout)
        page.add(
            ft.Image(src="icon.png", height=400),
            ft.Container(padding=20),
            ft.Text(f"Bienvenido, {current_username.capitalize()}!"),
            ft.Container(padding=20),
            logout_button
        )
        page.update()

    def body_screen(e=None):
        page.clean()
        bp = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
        page.add(bp)

        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT bodyPart FROM datos")
        body_parts = cursor.fetchall()
        conn.close()

        for body_part in body_parts:
            image_path = os.path.join(image_base_path, f"{body_part[0].lower()}.png")
            button = ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(src=image_path, fit=ft.ImageFit.COVER, width=100, height=100),
                            ft.Text(body_part[0].upper())
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                ),
                on_click=lambda e, body_part=body_part: equipment_screen(e, body_part[0]),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            )
            bp.controls.append(button)
        page.update()

    def equipment_screen(e, body_part):
        history.append("body_part")
        page.clean()
        eq = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
        page.add(eq)

        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT equipment FROM datos WHERE bodyPart=?", (body_part,))
        equipments = cursor.fetchall()
        conn.close()

        for equip in equipments:
            image_path = os.path.join(image_base_path, f"{body_part.lower()}.png")
            button = ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(src=image_path, fit=ft.ImageFit.COVER, width=100, height=100),
                            ft.Text(equip[0].upper())
                        ],
                        alignment=ft.alignment.center
                    ),
                    alignment=ft.alignment.center
                ),
                on_click=lambda e: exercise_screen(e, body_part, equip[0]),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            )
            eq.controls.append(button)

        page.update()

    def exercise_screen(e, body_part, equipment):
        history.append("equipment")
        page.clean()

        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gifUrl, instructions FROM datos WHERE bodyPart=? AND equipment=?", (body_part, equipment))
        ejercicios = cursor.fetchall()
        conn.close()

        ejercicio_card = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

        def open_dlg(instructions):
            dlg = ft.AlertDialog(
                title=ft.Text("Instrucciones"),
                content=ft.Text(instructions),
                actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dlg(dlg))]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        def close_dlg(dlg):
            dlg.open = False
            page.update()

        def mark_favorite(e, ejercicio_id):
            conn = sqlite3.connect(bd_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM favoritos WHERE user_id=? AND ejercicio_id=?", (current_user_id, ejercicio_id))
            favorito = cursor.fetchone()
            if favorito:
                cursor.execute("DELETE FROM favoritos WHERE user_id=? AND ejercicio_id=?", (current_user_id, ejercicio_id))
                conn.commit()
                message = f"Ejercicio eliminado de favoritos"
            else:
                cursor.execute("INSERT INTO favoritos (user_id, ejercicio_id) VALUES (?, ?)", (current_user_id, ejercicio_id))
                conn.commit()
                message = f"Ejercicio añadido a favoritos"
            conn.close()

            page.snack_bar = ft.SnackBar(content=ft.Text(message))
            page.snack_bar.open = True
            page.update()
            exercise_screen(e, body_part, equipment)

        for ejercicio in ejercicios:
            ejercicio_id, name, gifUrl, instructions = ejercicio

            conn = sqlite3.connect(bd_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM favoritos WHERE user_id=? AND ejercicio_id=?", (current_user_id, ejercicio_id))
            favorito = cursor.fetchone()
            conn.close()

            favorite_icon = ft.icons.STAR if favorito else ft.icons.STAR_OUTLINE_OUTLINED

            card_content = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(name.upper()),
                                subtitle=ft.Image(src=gifUrl),
                            ),
                            ft.Row(
                                [
                                    ft.TextButton("Instrucciones", on_click=lambda e, inst=instructions: open_dlg(inst)),
                                    ft.IconButton(
                                        icon=favorite_icon,
                                        icon_size=20,
                                        tooltip="Favorito",
                                        on_click=lambda e, ejercicio_id=ejercicio_id: mark_favorite(e, ejercicio_id)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    padding=10,
                )
            )

            ejercicio_card.controls.append(card_content)

        page.add(ejercicio_card)

    def favorites_screen(e=None):
        page.clean()

        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT datos.name, datos.gifUrl, datos.instructions
            FROM favoritos
            JOIN datos ON favoritos.ejercicio_id = datos.id
            WHERE favoritos.user_id = ?
        """, (current_user_id,))
        favoritos = cursor.fetchall()
        conn.close()

        favorites_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

        for fav in favoritos:
            name, gifUrl, instructions = fav

            def open_dlg(instructions):
                dlg = ft.AlertDialog(
                    title=ft.Text("Instrucciones"),
                    content=ft.Text(instructions),
                    actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dlg(dlg))]
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            def close_dlg(dlg):
                dlg.open = False
                page.update()

            def remove_favorite(e, name):
                conn = sqlite3.connect(bd_path)
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM datos WHERE name=?", (name,))
                ejercicio_id = cursor.fetchone()[0]
                cursor.execute("DELETE FROM favoritos WHERE user_id=? AND ejercicio_id=?", (current_user_id, ejercicio_id))
                conn.commit()
                conn.close()

                page.snack_bar = ft.SnackBar(content=ft.Text(f"{name} eliminado de favoritos"))
                page.snack_bar.open = True
                page.update()
                favorites_screen()

            card_content = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(name.upper()),
                                subtitle=ft.Image(src=gifUrl),
                            ),
                            ft.Row(
                                [
                                    ft.TextButton("Instrucciones", on_click=lambda e, inst=instructions: open_dlg(inst)),
                                    ft.IconButton(
                                        icon=ft.icons.STAR,
                                        icon_size=20,
                                        tooltip="Eliminar de favoritos",
                                        on_click=lambda e, name=name: remove_favorite(e, name)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    padding=10,
                )
            )
            favorites_list.controls.append(card_content)

        page.add(favorites_list)

    def go_back(e):
        if history:
            last_action = history.pop()
            if last_action == "equipment":
                body_screen()
            elif last_action == "body_part":
                show_home()

    def nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            show_home()
        elif selected_index == 1:
            body_screen()
        elif selected_index == 2:
            favorites_screen()
        elif selected_index == 3:
            go_back(None)

    show_login()

ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)
