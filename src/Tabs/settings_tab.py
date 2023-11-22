import customtkinter as ctk
from .tab import Tab
from settings_manager import Setting
from tabview import TabView


class SettingsTab(Tab):
    def __init__(self, app, tabview: TabView, title: str):
        super().__init__(app, tabview, title, visibility_setting=False)

    def create_content(self):
        self.settings = self.app.settings
        self._pady = 2
        self._create_settings_widgets()

    def _create_settings_widgets(self):
        self.settings_frame = ctk.CTkScrollableFrame(self.tab)
        self.settings_frame.pack(fill="both", expand=True)
        self.settings_frame.grid_columnconfigure(0, weight=0)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.exit_button = ctk.CTkButton(
            self.tab, text="Exit", command=self.app.destroy
        )
        self.exit_button.pack(fill="x", pady=8)
        self._draw_settings(self._get_parents())

    def _draw_settings(self, parents: list):
        current_row = 0
        for parent in parents:
            if len(parent) > 0:
                self._create_parent_label(parent, current_row)
                current_row += 1
            current_row = self._draw_settings_for_parent(parent, current_row)

    def _draw_settings_for_parent(self, parent_name: str, grid_row: int) -> int:
        for setting in self.settings.settings.values():
            if setting.parent == parent_name:
                self._draw_setting(setting, grid_row)
                grid_row += 1
        return grid_row

    def _create_parent_label(self, name: str, grid_row: int):
        text = self._clean_name(name)
        text = text.upper()
        font = ("TkDefaultFont", 14, "bold")
        parent_label = ctk.CTkLabel(self.settings_frame, text=text, font=font)
        parent_label.grid(row=grid_row, column=0, sticky=ctk.W, pady=(10, 0))

    def _get_parents(self) -> list:
        parents = []
        for setting in self.settings.settings.values():
            if setting.parent is not None and setting.parent not in parents:
                parents.append(setting.parent)
        return parents

    def _draw_setting(self, setting: Setting, grid_row: int):
        if setting.hidden:
            return
        clean_name = self._clean_name(setting.name)
        self._create_label(self.settings_frame, clean_name, 0, grid_row, self._pady)
        if setting.options is not None:
            self._draw_option_setting(setting, grid_row)
            return
        if setting.value_type is bool:
            self._create_checkbox_widget(setting, grid_row)
            return
        elif setting.min_value is not None and setting.max_value is not None:
            self._create_slider_widget(setting, grid_row)
            return
        self._create_entry_widget(setting, grid_row)

    def _create_label(self, container, text: str, column: int, row: int, pady=0):
        label = ctk.CTkLabel(container, text=text)
        label.grid(row=row, column=column, pady=pady, sticky=ctk.W)

    def _draw_option_setting(self, setting: Setting, grid_row: int):
        if len(setting.options) <= 5:
            self._create_segmented_widget(setting, grid_row)
            return
        self._create_dropdown_widget(setting, grid_row)

    def _create_dropdown_widget(self, setting: Setting, grid_row: int):
        on_dropdown_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, setting.value_type(value)
        )
        dropdown = ctk.CTkOptionMenu(
            self.settings_frame, values=setting.options, command=on_dropdown_changed
        )
        dropdown.grid(row=grid_row, column=1, padx=5, pady=self._pady, sticky=ctk.E)
        dropdown.set(str(setting.value))

    def _create_segmented_widget(self, setting: Setting, grid_row: int):
        on_segmented_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, setting.value_type(value)
        )
        segmented = ctk.CTkSegmentedButton(
            self.settings_frame, values=setting.options, command=on_segmented_changed
        )
        segmented.grid(row=grid_row, column=1, padx=5, pady=self._pady, sticky=ctk.E)
        segmented.set(str(setting.value))

    def _create_slider_widget(self, setting: Setting, grid_row: int):
        on_slider_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, value
        )
        slider = ctk.CTkSlider(
            self.settings_frame,
            from_=setting.min_value,
            to=setting.max_value,
            command=on_slider_changed,
        )
        slider.grid(row=grid_row, column=1, pady=self._pady, sticky=ctk.E, padx=(50, 0))
        slider.set(setting.value)

    def _create_entry_widget(self, setting: Setting, grid_row: int):
        entry_setting_value = ctk.CTkEntry(self.settings_frame)
        entry_setting_value.grid(row=grid_row, column=1, padx=5, pady=self._pady)
        if type(entry_setting_value) is ctk.CTkEntry:
            entry_setting_value.insert(ctk.END, setting.value)
            entry_setting_value.bind(
                "<KeyRelease>",
                lambda event, setting=setting: self._entry_changed(event, setting),
            )

    def _create_checkbox_widget(self, setting: Setting, grid_row: int):
        on_checkbox_changed = lambda: self.settings.set_value(
            setting.name, checkbox.get()
        )
        checkbox = ctk.CTkCheckBox(self.settings_frame, text="")
        checkbox.configure(command=on_checkbox_changed)
        if setting.value:
            checkbox.select()
        checkbox.grid(row=grid_row, column=1, sticky=ctk.E)

    def _clean_name(self, name: str) -> str:
        return name.replace("_", " ").title()

    def _entry_changed(self, event, setting: Setting):
        if event.keysym != "Return":
            return
        entry = event.widget
        value = entry.get()
        if len(value) == 0:
            return
        self.settings.set_value(setting.name, value)
        entry.delete("0", ctk.END)
        entry.insert(ctk.END, self.settings.get(setting.name).value)
