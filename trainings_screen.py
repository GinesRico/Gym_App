import flet as ft
from database import get_connection

def show_trainings(page, current_user_id, history):
    page.clean()
    page.appbar = None  # Ensure there is no residual AppBar

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM entrenamientos WHERE user_id=%s", (current_user_id,))
    entrenamientos = cursor.fetchall()
    cursor.close()
    conn.close()

    training_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

    def delete_training(e, training_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entrenamiento_ejercicios WHERE entrenamiento_id=%s", (training_id,))
        cursor.execute("DELETE FROM entrenamientos WHERE id=%s", (training_id,))
        conn.commit()
        cursor.close()
        conn.close()
        snack_bar = ft.SnackBar(content=ft.Text("Entrenamiento eliminado"))
        page.overlay.append(snack_bar)  # Add the snack bar to the overlay
        snack_bar.open = True
        show_trainings(page, current_user_id, history)

    for training in entrenamientos:
        training_id, training_name = training

        def show_exercises(e, training_id=training_id, training_name=training_name):
            page.clean()
            page.appbar = ft.AppBar(
                title=ft.Text(training_name),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: back_to_trainings(page, current_user_id, history))
            )
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ejercicios.id, ejercicios.name, ejercicios.gifUrl, ejercicios.instructions, ejercicios.secondaryMuscles
                FROM entrenamiento_ejercicios
                JOIN ejercicios ON entrenamiento_ejercicios.ejercicio_id = ejercicios.id
                WHERE entrenamiento_ejercicios.entrenamiento_id=%s
            """, (training_id,))
            ejercicios = cursor.fetchall()
            cursor.close()
            conn.close()

            exercise_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

            for exercise in ejercicios:
                ejercicio_id, exercise_name, gifUrl, instructions, secondaryMuscles = exercise

                def open_dlg(instructions):
                    dlg = ft.AlertDialog(
                        title=ft.Text("Instrucciones"),
                        content=ft.Text(instructions),
                        actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dlg(dlg))]
                    )
                    page.overlay.append(dlg)  # Add the dialog to the overlay
                    dlg.open = True
                    page.update()

                def open_muscles_dlg(secondaryMuscles):
                    dlg = ft.AlertDialog(
                        title=ft.Text("Músculos Auxiliares"),
                        content=ft.Text(secondaryMuscles),
                        actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dlg(dlg))]
                    )
                    page.overlay.append(dlg)  # Add the dialog to the overlay
                    dlg.open = True
                    page.update()

                def close_dlg(dlg):
                    dlg.open = False
                    page.update()

                def remove_exercise(e, ejercicio_id=ejercicio_id):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM entrenamiento_ejercicios WHERE entrenamiento_id=%s AND ejercicio_id=%s", (training_id, ejercicio_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    snack_bar = ft.SnackBar(content=ft.Text(f"Ejercicio eliminado del entrenamiento"))
                    page.overlay.append(snack_bar)  # Add the snack bar to the overlay
                    snack_bar.open = True
                    show_exercises(e, training_id, training_name)
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
                                        ft.IconButton(icon=ft.icons.INFO, tooltip="Instrucciones", on_click=lambda e, inst=instructions: open_dlg(inst)),
                                        ft.IconButton(icon=ft.icons.FITNESS_CENTER, tooltip="Músculos Auxiliares", on_click=lambda e, muscles=secondaryMuscles: open_muscles_dlg(muscles)),
                                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar Ejercicio", on_click=remove_exercise)
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
                    trailing=ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, training_id=training_id: delete_training(e, training_id)),
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

def back_to_trainings(page, current_user_id, history):
    show_trainings(page, current_user_id, history)
    page.appbar = None
    page.update()
