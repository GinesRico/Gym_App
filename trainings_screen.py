import flet as ft
import sqlite3
from config import bd_path

def show_trainings(page, current_user_id, history):
    page.clean()
    page.appbar = None  # Asegúrate de que no haya un AppBar residual

    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre FROM entrenamientos WHERE user_id = ?
    """, (current_user_id,))
    entrenamientos = cursor.fetchall()
    conn.close()

    training_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

    for training in entrenamientos:
        training_id, training_name = training

        def show_exercises(e, training_id=training_id, training_name=training_name):
            page.clean()
            page.appbar = ft.AppBar(
                title=ft.Text(training_name),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: show_trainings(page, current_user_id, history))
            )
            conn = sqlite3.connect(bd_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ejercicios.name, ejercicios.gifUrl, ejercicios.instructions
                FROM entrenamiento_ejercicios
                JOIN ejercicios ON entrenamiento_ejercicios.ejercicio_id = ejercicios.id
                WHERE entrenamiento_ejercicios.entrenamiento_id = ?
            """, (training_id,))
            ejercicios = cursor.fetchall()
            conn.close()

            exercise_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

            for exercise in ejercicios:
                exercise_name, gifUrl, instructions = exercise

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
                                    subtitle=ft.Image(src=gifUrl),
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
                exercise_list.controls.append(card_content)

            page.add(exercise_list)
            page.update()

        training_card = ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    title=ft.Text(training_name),
                    on_click=show_exercises
                ),
                padding=10,
                margin=10,
                bgcolor=ft.colors.BLUE_100
            )
        )

        training_list.controls.append(training_card)

    page.add(training_list)
    page.update()

