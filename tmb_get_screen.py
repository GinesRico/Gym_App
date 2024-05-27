import flet as ft

def show_tmb_get_screen(page):
    def calculate_tmb_get(e):
        try:
            weight = float(weight_field.value)
            height = float(height_field.value)
            age = int(age_field.value)
            activity_factor = float(activity_dropdown.value)
            goal_factor = float(goal_dropdown.value)

            # Fórmula de Harris-Benedict para calcular el TMB
            tmb = 10 * weight + 6.25 * height - 5 * age + 5  # Para hombres
            # tmb = 10 * weight + 6.25 * height - 5 * age - 161  # Para mujeres (descomentar si es necesario)

            get = tmb * activity_factor
            daily_calories_with_goal = get + goal_factor
            
            tmb_result.value = f"TMB: {tmb:.2f} kcal/día"
            get_result.value = f"GET: {get:.2f} kcal/día"
            goal_result.value = f"Calorías diarias con objetivo: {daily_calories_with_goal:.2f} kcal/día"
            
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, ingrese valores válidos"))
            page.snack_bar.open = True
            page.update()
    
    def calculate_macros(e):
        try:
            daily_calories_with_goal = float(goal_result.value.split()[4])
            macro_ratio = macro_dropdown.value
            carb_ratio, protein_ratio, fat_ratio = map(float, macro_ratio.split('/'))

            carb_calories = daily_calories_with_goal * (carb_ratio / 100)
            protein_calories = daily_calories_with_goal * (protein_ratio / 100)
            fat_calories = daily_calories_with_goal * (fat_ratio / 100)

            carb_grams = carb_calories / 4
            protein_grams = protein_calories / 4
            fat_grams = fat_calories / 9

            # Crear los contenedores para los resultados
            containers = [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{daily_calories_with_goal:.2f} kcal", style="headline4", color=ft.colors.BLACK),
                            ft.Text("Media de Kcalorías", color=ft.colors.BLACK54)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    margin=10,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_100,
                    expand=True
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{protein_grams:.2f} g", style="headline4", color=ft.colors.BLACK),
                            ft.Text("Media de Proteínas", color=ft.colors.BLACK54)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    margin=10,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_100,
                    expand=True
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{carb_grams:.2f} g", style="headline4", color=ft.colors.BLACK),
                            ft.Text("Media de Carbohidratos", color=ft.colors.BLACK54)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    margin=10,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_100,
                    expand=True
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{fat_grams:.2f} g", style="headline4", color=ft.colors.BLACK),
                            ft.Text("Media de Grasas", color=ft.colors.BLACK54)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    margin=10,
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_100,
                    expand=True
                )
            ]

            # Organizar los contenedores en una tabla de 2x2
            table_result.controls = [
                ft.Row([containers[0], containers[1]], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([containers[2], containers[3]], alignment=ft.MainAxisAlignment.CENTER)
            ]
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, calcule primero el TMB y GET"))
            page.snack_bar.open = True
            page.update()

    page.clean()
    
    weight_field = ft.TextField(label="Peso (kg)", width=200)
    height_field = ft.TextField(label="Altura (cm)", width=200)
    age_field = ft.TextField(label="Edad", width=200)
    
    activity_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("1.2", "Sedentario"),
            ft.dropdown.Option("1.375", "Actividad ligera"),
            ft.dropdown.Option("1.55", "Actividad moderada"),
            ft.dropdown.Option("1.725", "Actividad intensa"),
            ft.dropdown.Option("1.9", "Actividad muy intensa"),
        ],
        label="Nivel de actividad",
        width=300,
    )

    goal_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("0", "Mantener peso"),
            ft.dropdown.Option("-550", "Déficit para perder 0.5 kg/semana"),
            ft.dropdown.Option("-1100", "Déficit para perder 1 kg/semana"),
            ft.dropdown.Option("-1650", "Déficit para perder 1.5 kg/semana"),
            ft.dropdown.Option("-2200", "Déficit para perder 2 kg/semana"),
            ft.dropdown.Option("550", "Superávit para ganar 0.5 kg/semana"),
            ft.dropdown.Option("1100", "Superávit para ganar 1 kg/semana"),
            ft.dropdown.Option("1650", "Superávit para ganar 1.5 kg/semana"),
            ft.dropdown.Option("2200", "Superávit para ganar 2 kg/semana"),
        ],
        label="Objetivo",
        width=300,
    )

    macro_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("60/25/15", "60/25/15 (Alto en carbohidratos)"),
            ft.dropdown.Option("50/30/20", "50/30/20 (Moderado)"),
            ft.dropdown.Option("40/30/30", "40/30/30 (Dieta de la Zona)"),
            ft.dropdown.Option("25/45/30", "25/45/30 (Bajo en carbohidratos)"),
        ],
        label="Proporción de Macronutrientes",
        width=300,
    )
    
    calculate_tmb_button = ft.ElevatedButton(text="Calcular TMB & GET", on_click=calculate_tmb_get)
    calculate_macros_button = ft.ElevatedButton(text="Obtener Macros", on_click=calculate_macros)
    
    tmb_result = ft.Text()
    get_result = ft.Text()
    goal_result = ft.Text()
    table_result = ft.Column()

    scrollable_content = ft.Column(
        controls=[
            ft.Text("Calculadora de TMB & GET", style="headline4"),
            weight_field,
            height_field,
            age_field,
            activity_dropdown,
            goal_dropdown,
            calculate_tmb_button,
            tmb_result,
            get_result,
            goal_result,
            macro_dropdown,
            calculate_macros_button,
            table_result
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,  # Hacer que la columna sea desplazable
    )

    page.add(scrollable_content)
    page.update()
