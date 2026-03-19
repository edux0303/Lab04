import flet as ft


class View(object):
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "TdP 2024 - Lab 04 - SpellChecker ++"
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # Controller
        self.__controller = None
        # UI elements
        self.__title = None
        self.__theme_switch = None
        self.__dd_language = None
        self.__dd_modality = None
        self.__txt_input = None
        self.__btn_spell = None
        self.__lv_output = None
        self.__txt_status = None

    def add_content(self):
        """Function that creates and adds the visual elements to the page."""

        # --- Title + theme switch (già fornito) ---
        self.__title = ft.Text(
            "TdP 2026 - Lab 04 - SpellChecker ++",
            size=24,
            color="blue"
        )
        self.__theme_switch = ft.Switch(
            label="Light theme",
            on_change=self.theme_changed
        )
        self.page.controls.append(
            ft.Row(
                spacing=30,
                controls=[self.__theme_switch, self.__title],
                alignment=ft.MainAxisAlignment.START
            )
        )


        self.__dd_language = ft.Dropdown(
            label="Select language",
            width=300,
            options=[
                ft.dropdown.Option("italian"),
                ft.dropdown.Option("english"),
                ft.dropdown.Option("spanish"),
            ],
            on_change=self.__handle_language_change
        )
        self.__txt_status = ft.Text("", color="green", size=13)

        self.page.controls.append(
            ft.Row(
                controls=[self.__dd_language, self.__txt_status],
                alignment=ft.MainAxisAlignment.START
            )
        )


        self.__dd_modality = ft.Dropdown(
            label="Search Modality",
            width=200,
            options=[
                ft.dropdown.Option("Default"),
                ft.dropdown.Option("Linear"),
                ft.dropdown.Option("Dichotomic"),
            ],
            on_change=self.__handle_modality_change
        )

        self.__txt_input = ft.TextField(
            label="Add your sentence here",
            expand=True,
        )

        self.__btn_spell = ft.ElevatedButton(
            text="Spell Check",
            on_click=self.__handle_spell_check
        )

        self.page.controls.append(
            ft.Row(
                controls=[
                    self.__dd_modality,
                    self.__txt_input,
                    self.__btn_spell
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )


        self.__lv_output = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True,
            height=300
        )
        self.page.controls.append(self.__lv_output)

        self.page.update()


    def __handle_language_change(self, e):
        if self.__dd_language.value:
            self.__txt_status.value = (
                f"✓ Lingua selezionata: {self.__dd_language.value}"
            )
            self.__txt_status.color = "green"
        else:
            self.__txt_status.value = "✗ Nessuna lingua selezionata"
            self.__txt_status.color = "red"
        self.page.update()


    def __handle_modality_change(self, e):
        if self.__dd_modality.value:
            self.__lv_output.controls.append(
                ft.Text(
                    f"✓ Modalità selezionata: {self.__dd_modality.value}",
                    color="green",
                    size=13
                )
            )
        else:
            self.__lv_output.controls.append(
                ft.Text("✗ Nessuna modalità selezionata", color="red", size=13)
            )
        self.page.update()


    def __handle_spell_check(self, e):
        language = self.__dd_language.value
        modality = self.__dd_modality.value
        sentence = self.__txt_input.value

        if not language:
            self.__lv_output.controls.append(
                ft.Text("⚠ Seleziona una lingua prima di procedere.", color="red")
            )
            self.page.update()
            return

        if not modality:
            self.__lv_output.controls.append(
                ft.Text("⚠ Seleziona una modalità di ricerca.", color="red")
            )
            self.page.update()
            return

        if not sentence or sentence.strip() == "":
            self.__lv_output.controls.append(
                ft.Text("⚠ Inserisci una frase da controllare.", color="red")
            )
            self.page.update()
            return


        result = self.__controller.handleSentence(sentence, language, modality)

        if result is None:
            self.__lv_output.controls.append(
                ft.Text("⚠ Modalità non riconosciuta.", color="red")
            )
        else:
            parole_errate, tempo = result
            self.__lv_output.controls.append(
                ft.Text(f"Frase inserita: {sentence}", weight=ft.FontWeight.BOLD)
            )
            self.__lv_output.controls.append(
                ft.Text(f"Parole errate: {parole_errate}", color="red")
            )
            self.__lv_output.controls.append(
                ft.Text(f"Tempo richiesto dalla ricerca: {tempo:.6f} s", color="blue")
            )
            self.__lv_output.controls.append(ft.Divider())

        # Svuota il TextField
        self.__txt_input.value = ""
        self.page.update()


    def theme_changed(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.__theme_switch.label = (
            "Light theme"
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else "Dark theme"
        )
        self.page.update()


    def update(self):
        self.page.update()

    def setController(self, controller):
        self.__controller = controller