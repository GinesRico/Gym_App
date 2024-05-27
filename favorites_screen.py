import flet as ft
import sqlite3
from config import bd_path

def show_trainings(page, current_user_id, history):
    page.clean()

    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT entrenamientos.nombre, ejercicios.name, ejercicios.gifUrl, ejercicios.instructions
        FROM entrenamiento_ejercicios
        JOIN entrenamientos ON entrenamiento_ejercicios.entrenamiento_id = entrenamientos.id
        JOIN ejercicios ON entrenamiento_ejercicios.ejercicio_id = ejercicios.id
        WHERE entrenamientos.user_id = ?
    """, (current_user_id,))
    entrenamientos = cursor.fetchall()
    conn.close()

    training_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

    for training in entrenamientos:
        training_name, exercise_name, gifUrl, instructions = training

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

        card_content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(exercise_name.upper()),
                            subtitle=ft.Text(f"Entrenamiento: {training_name}"),
                            trailing=ft.Image(src=gifUrl),
                        ),
                        ft.Row(
                            [
                                ft.TextButton("Instrucciones", on_click=lambda e, inst=instructions: open_dlg(inst))
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            )
        )
        training_list.controls.append(card_content)

    page.add(training_list)
