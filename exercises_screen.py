import flet as ft
import os
from config import image_base_path
from database import get_connection

def body_screen(page, user_id, username, history):
    page.clean()
    bp = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    page.add(bp)

    conn = get_connection()
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
            on_click=lambda e, body_part=body_part: show_exercises(page, body_part[0], history, user_id),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )
        bp.controls.append(button)
    page.update()

def show_exercises(page, body_part, history, user_id):
    page.clean()
    history.append("body_screen")

    filter_dropdown_equipment = ft.Dropdown(
        options=[],
        on_change=lambda e: load_exercises(page, body_part, filter_dropdown_equipment.value, filter_dropdown_target.value, history, user_id),
        label="Filter by Equipment",
    )

    filter_dropdown_target = ft.Dropdown(
        options=[],
        on_change=lambda e: load_exercises(page, body_part, filter_dropdown_equipment.value, filter_dropdown_target.value, history, user_id),
        label="Filter by Target",
    )

    expandable_filters = ft.Container(
        content=ft.Column([filter_dropdown_equipment, filter_dropdown_target]),
        expand=False,
    )

    page.add(expandable_filters)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT equipment FROM ejercicios WHERE bodyPart=?", (body_part,))
    equipments = cursor.fetchall()
    cursor.execute("SELECT DISTINCT target FROM ejercicios WHERE bodyPart=?", (body_part,))
    targets = cursor.fetchall()
    conn.close()

    filter_dropdown_equipment.options = [ft.dropdown.Option(equip[0]) for equip in equipments]
    filter_dropdown_equipment.options.insert(0, ft.dropdown.Option("Todos"))

    filter_dropdown_target.options = [ft.dropdown.Option(target[0]) for target in targets]
    filter_dropdown_target.options.insert(0, ft.dropdown.Option("Todos"))

    load_exercises(page, body_part, history=history, user_id=user_id)

def load_exercises(page, body_part, equipment_filter=None, target_filter=None, history=None, user_id=None):
    page.clean()

    filter_dropdown_equipment = ft.Dropdown(
        options=[],
        on_change=lambda e: load_exercises(page, body_part, e.control.value, target_filter, history, user_id),
        label="Filter by Equipment",
    )

    filter_dropdown_target = ft.Dropdown(
        options=[],
        on_change=lambda e: load_exercises(page, body_part, equipment_filter, e.control.value, history, user_id),
        label="Filter by Target",
    )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT equipment FROM ejercicios WHERE bodyPart=?", (body_part,))
    equipments = cursor.fetchall()
    cursor.execute("SELECT DISTINCT target FROM ejercicios WHERE bodyPart=?", (body_part,))
    targets = cursor.fetchall()
    conn.close()

    filter_dropdown_equipment.options = [ft.dropdown.Option(equip[0]) for equip in equipments]
    filter_dropdown_equipment.options.insert(0, ft.dropdown.Option("Todos"))
    filter_dropdown_equipment.value = equipment_filter if equipment_filter else "Todos"

    filter_dropdown_target.options = [ft.dropdown.Option(target[0]) for target in targets]
    filter_dropdown_target.options.insert(0, ft.dropdown.Option("Todos"))
    filter_dropdown_target.value = target_filter if target_filter else "Todos"

    expandable_filters = ft.Container(
        content=ft.Column([filter_dropdown_equipment, filter_dropdown_target]),
        expand=False,
    )

    ejercicio_card = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.ALWAYS)

    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, gifUrl, instructions, secondaryMuscles FROM ejercicios WHERE bodyPart=?"
    params = [body_part]
    if equipment_filter and equipment_filter != "Todos":
        query += " AND equipment=?"
        params.append(equipment_filter)
    if target_filter and target_filter != "Todos":
        query += " AND target=?"
        params.append(target_filter)
    cursor.execute(query, params)
    ejercicios = cursor.fetchall()
    conn.close()

    def open_dlg(content, title="Instrucciones"):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dlg(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    def mark_favorite(e, ejercicio_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM favoritos WHERE user_id=? AND ejercicio_id=?", (user_id, ejercicio_id))
        favorito = cursor.fetchone()
        if favorito:
            cursor.execute("DELETE FROM favoritos WHERE user_id=? AND ejercicio_id=?", (user_id, ejercicio_id))
            conn.commit()
            message = f"Ejercicio eliminado de favoritos"
        else:
            cursor.execute("INSERT INTO favoritos (user_id, ejercicio_id) VALUES (?, ?)", (user_id, ejercicio_id))
            conn.commit()
            message = f"Ejercicio añadido a favoritos"
        conn.close()

        page.snack_bar = ft.SnackBar(content=ft.Text(message))
        page.snack_bar.open = True
        page.update()
        load_exercises(page, body_part, equipment_filter, target_filter, history, user_id)

    for ejercicio in ejercicios:
        ejercicio_id, name, gifUrl, instructions, secondaryMuscles = ejercicio

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM favoritos WHERE user_id=? AND ejercicio_id=?", (user_id, ejercicio_id))
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
                                ft.TextButton("Músculos Auxiliares", on_click=lambda e, secMuscles=secondaryMuscles: open_dlg(secMuscles, title="Músculos Auxiliares")),
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

    page.add(expandable_filters)
    page.add(ejercicio_card)
    page.update()
