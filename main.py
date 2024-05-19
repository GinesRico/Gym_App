import flet as ft
import sqlite3
import os 

def main(page: ft.Page):
    page.title = "Ejercicios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.alignment = ft.CrossAxisAlignment.CENTER

    # Ruta de la imagen
    image_base_path = "/Users/ginesrico/Desktop/gym_app/assets"


    conn = sqlite3.connect('datos_ejercicios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bodyPart FROM datos")
    body_parts = cursor.fetchall()
    conn.close()

    history = []

    def equipment_screen(e):
        body_part = e.control.data
        history.append("body_part")
        page.clean()
        eq = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
        page.add(eq)

        conn = sqlite3.connect('datos_ejercicios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT equipment FROM datos WHERE bodyPart=?", (body_part,))
        equipments = cursor.fetchall()
        conn.close()

        for equip in equipments:
            image_path = os.path.join(image_base_path, f"{body_part[0].lower()}.png")
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
                on_click=lambda e: exercisce_screen(e, body_part),
                data=equip[0],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5)
                )
            )
            eq.controls.append(button)
        
        page.update()

    def exercisce_screen(e, body_part):
        equipment = e.control.data
        history.append("equipment")
        page.clean()
        conn = sqlite3.connect('datos_ejercicios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, gifUrl, instructions FROM datos WHERE bodyPart=? AND equipment=?", (body_part, equipment))
        ejercicios = cursor.fetchall()
        conn.close()

        ejercicio_card = ft.Column(
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        )

        for ejercicio in ejercicios:
            name, gifUrl, instructions = ejercicio

            # Crear un diálogo único para cada ejercicio
            dlg = ft.AlertDialog(
                title=ft.Text("Instrucciones"),
                content=ft.Text("")
            )

            # Crear contenido de tarjeta para el ejercicio actual
            card_content = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(name),
                                subtitle=ft.Image(src=gifUrl),
                            ),
                            ft.Row(
                                [ft.TextButton("Instrucciones", on_click=lambda e: open_dlg(instructions))],
                                alignment=ft.MainAxisAlignment.END,
                            ),                            
                        ]
                    ),
                    padding=10,
                )
            )

            # Función para abrir el diálogo correspondiente al ejercicio
            def open_dlg(instructions):
                dlg.content = ft.Text(instructions)
                page.dialog = dlg
                dlg.open = True
                page.update()

            ejercicio_card.controls.append(card_content)

        page.add(ejercicio_card)

    def go_back(e):
        if history:
            last_action = history.pop()
            if last_action == "equipment":
                body_screen()
            elif last_action == "body_part":
                home()

    def home():
        page.add(ft.Text("Bienvenido!", expand=True))


    def body_screen():
        
        bp = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
        page.add(bp)

        conn = sqlite3.connect('datos_ejercicios.db')
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
                on_click=equipment_screen,
                data=body_part[0],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5)
                )
            )
            bp.controls.append(button)
        page.update()
        
    def nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.clean()
            home()
        elif selected_index == 1:
            page.clean()
            body_screen()
        elif selected_index == 2:
            page.clean()
            go_back(None)

    page.navigation_bar = ft.CupertinoNavigationBar(
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change=nav_change,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Inicio"),
            ft.NavigationDestination(icon=ft.icons.SPORTS_GYMNASTICS_ROUNDED, label="Ejercicios"),
            ft.NavigationDestination(icon=ft.icons.ARROW_BACK, label="Atrás")
        ]
    )

    page.add(ft.Text("Bienvenido!", expand=True))

ft.app(target=main)
