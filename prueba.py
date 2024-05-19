import flet as ft
import sqlite3
import os 



def main(page: ft.Page):
    gv = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    page.add(gv)
    image_base_path = "/Users/ginesrico/Desktop/gym_app/assets"

    def body_part_click(e):
        body_part = e.control.data
        history.append("body_part")
        page.clean()
        conn = sqlite3.connect('datos_ejercicios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT equipment FROM datos WHERE bodyPart=?", (body_part,))
        equipments = cursor.fetchall()
        conn.close()

        equipment_buttons = []

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
                ),
                on_click=lambda e: equipment_click(e, body_part),
                data=equip[0],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5)
                )
            )
            equipment_buttons.append(button)

        page.add(ft.Row(controls=equipment_buttons, scroll="always", wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER))





    conn = sqlite3.connect('datos_ejercicios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bodyPart FROM datos")
    body_parts = cursor.fetchall()
    conn.close()

    body_part_buttons = []
    for body_part in body_parts:
        image_path = os.path.join(image_base_path, f"{body_part[0].lower()}.png")
        button = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src=image_path, fit=ft.ImageFit.COVER, width=100, height=100),
                        ft.Text(body_part[0].upper())
                    ],
                    alignment=ft.alignment.center
                ),
            ),
            on_click=(body_part_click),
            data=body_part[0],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
        gv.controls.append(button)
    page.update()

ft.app(target=main)