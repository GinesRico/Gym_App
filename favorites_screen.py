import flet as ft
from database import get_connection

def favorites_screen(page, user_id, history):
    page.clean()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ejercicios.name, ejercicios.gifUrl, ejercicios.instructions
        FROM favoritos
        JOIN ejercicios ON favoritos.ejercicio_id = ejercicios.id
        WHERE favoritos.user_id = ?
    """, (user_id,))
    favoritos = cursor.fetchall()
    conn.close()

    favorites_list = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ejercicios WHERE name=?", (name,))
        ejercicio_id = cursor.fetchone()[0]
        cursor.execute("DELETE FROM favoritos WHERE user_id=? AND ejercicio_id=?", (user_id, ejercicio_id))
        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(content=ft.Text(f"{name} eliminado de favoritos"))
        page.snack_bar.open = True
        page.update()
        favorites_screen(page, user_id, history)

    for fav in favoritos:
        name, gifUrl, instructions = fav

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
    page.update()
