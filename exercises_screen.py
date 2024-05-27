import flet as ft
import sqlite3
import os
from config import image_base_path, bd_path

def show_exercises(page, body_part, history, current_user_id, current_username):
    def load_exercises(e, equipment_filter=None, target_filter=None):
        page.clean()

        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()

        query = "SELECT id, name, gifUrl, instructions FROM ejercicios WHERE bodyPart=?"
        params = [body_part]

        if equipment_filter:
            query += " AND equipment=?"
            params.append(equipment_filter)
        if target_filter:
            query += " AND target=?"
            params.append(target_filter)

        cursor.execute(query, params)
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

        def add_to_training(e, ejercicio_id):
            def save_to_existing_training(e):
                selected_training = training_dropdown.value
                if selected_training:
                    conn = sqlite3.connect(bd_path)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO entrenamiento_ejercicios (entrenamiento_id, ejercicio_id) VALUES (?, ?)", (selected_training, ejercicio_id))
                    conn.commit()
                    conn.close()
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"Ejercicio añadido al entrenamiento {selected_training}"))
                    page.snack_bar.open = True
                    page.dialog.open = False
                    page.update()

            def create_new_training(e):
                training_name = training_name_field.value
                if training_name:
                    conn = sqlite3.connect(bd_path)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO entrenamientos (user_id, nombre) VALUES (?, ?)", (current_user_id, training_name))
                    conn.commit()
                    training_id = cursor.lastrowid
                    cursor.execute("INSERT INTO entrenamiento_ejercicios (entrenamiento_id, ejercicio_id) VALUES (?, ?)", (training_id, ejercicio_id))
                    conn.commit()
                    conn.close()
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"Nuevo entrenamiento {training_name} creado y ejercicio añadido"))
                    page.snack_bar.open = True
                    page.dialog.open = False
                    page.update()

            training_name_field = ft.TextField(label="Nuevo Entrenamiento")
            training_dropdown = ft.Dropdown(
                options=[],
                label="Entrenamiento Existente",
                width=100
            )

            conn = sqlite3.connect(bd_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM entrenamientos WHERE user_id=?", (current_user_id,))
            entrenamientos = cursor.fetchall()
            conn.close()

            for entrenamiento in entrenamientos:
                training_dropdown.options.append(ft.dropdown.Option(entrenamiento[0], entrenamiento[1]))

            page.dialog = ft.AlertDialog(
                title=ft.Text("Añadir a Entrenamiento"),
                content=ft.Column(
                    [
                        ft.Text("Selecciona un entrenamiento existente o crea uno nuevo"),
                        ft.Row(
                            [
                                training_dropdown,
                                ft.ElevatedButton(text="Añadir", on_click=save_to_existing_training)
                            ]
                        ),
                        training_name_field,
                        ft.ElevatedButton(text="Crear y Añadir", on_click=create_new_training)
                    ],
                    spacing=10
                )
            )
            page.dialog.open = True
            page.update()

        for ejercicio in ejercicios:
            ejercicio_id, name, gifUrl, instructions = ejercicio

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
                                        icon=ft.icons.ADD,
                                        icon_size=20,
                                        tooltip="Añadir a entrenamiento",
                                        on_click=lambda e, ejercicio_id=ejercicio_id: add_to_training(e, ejercicio_id)
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

    load_exercises(None)

def body_screen(page, current_user_id, current_username, history):
    page.clean()
    bp = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    page.add(bp)

    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bodyPart FROM ejercicios")
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
            on_click=lambda e, body_part=body_part: show_exercises(page, body_part[0], history, current_user_id, current_username),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        bp.controls.append(button)
    page.update()
