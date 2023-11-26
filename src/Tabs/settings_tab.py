import customtkinter as ctk

from tooltip import ToolTip
from .tab import Tab
from settings_manager import Setting
from tabview import TabView
from slider import Slider
from setting import Setting
from setting import RangeSetting


class SettingsTab(Tab):
    def __init__(self, app, tabview: TabView, title: str) -> None:
        super().__init__(app, tabview, title, visibility_setting=False)

    def create_content(self) -> None:
        self.settings = self.app.settings
        self._pady = 2
        self._create_settings_widgets()

    def _create_settings_widgets(self) -> None:
        self.settings_frame = ctk.CTkScrollableFrame(self.tab)
        self.settings_frame.pack(fill="both", expand=True)
        self.settings_frame.grid_columnconfigure(0, weight=0)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self._create_bottom_btn_frame()
        self._draw_settings(self._get_parents())

    def _create_bottom_btn_frame(self):
        """Create the frame containing the exit and restart buttons."""
        self.button_frame = ctk.CTkFrame(self.tab)
        self.button_frame.pack(fill="x")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        button_font = ("TkDefaultFont", 12, "bold")
        self.restart_btn = ctk.CTkButton(
            self.button_frame,
            text="RESTART",
            command=self.app.restart_app,
            fg_color="orange",
            text_color="white",
            hover_color="darkorange",
            font=button_font,
        ).grid(row=0, column=0, sticky=ctk.EW, padx=5, pady=2)
        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="EXIT",
            command=self.app.destroy,
            fg_color="red",
            hover_color="darkred",
            font=button_font,
        ).grid(row=0, column=1, sticky=ctk.EW, padx=5, pady=2)

    def _draw_settings(self, parents: list) -> None:
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

    def _create_parent_label(self, name: str, grid_row: int) -> None:
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

    def _draw_setting(self, setting: Setting, grid_row: int) -> None:
        if setting.hidden:
            return
        clean_name = self._clean_name(setting.name)
        label = self._create_label(
            self.settings_frame, clean_name, 0, grid_row, self._pady
        )
        self.create_description_tooltip(label, setting.description)
        if hasattr(setting, "options"):
            self._draw_option_setting(setting, grid_row)
            return
        elif setting.value_type is bool:
            self._create_checkbox_widget(setting, grid_row)
            return
        elif hasattr(setting, "min_value") and hasattr(setting, "max_value"):
            self._create_slider_widget(setting, grid_row)
            return
        self._create_entry_widget(setting, grid_row)

    def _create_label(
        self, container, text: str, column: int, row: int, pady=0
    ) -> ctk.CTkLabel:
        label = ctk.CTkLabel(container, text=text)
        label.grid(row=row, column=column, pady=pady, sticky=ctk.W)
        return label

    def _draw_option_setting(self, setting: Setting, grid_row: int) -> None:
        if len(setting.options) <= 5:
            self._create_segmented_widget(setting, grid_row)
            return
        self._create_dropdown_widget(setting, grid_row)

    def _create_dropdown_widget(self, setting: Setting, grid_row: int) -> None:
        on_dropdown_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, setting.value_type(value)
        )
        dropdown = ctk.CTkOptionMenu(
            self.settings_frame, values=setting.options, command=on_dropdown_changed
        )
        dropdown.grid(row=grid_row, column=1, padx=5, pady=self._pady, sticky=ctk.E)
        dropdown.set(str(setting.value))

    def _create_segmented_widget(self, setting: Setting, grid_row: int) -> None:
        on_segmented_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, setting.value_type(value)
        )
        segmented = ctk.CTkSegmentedButton(
            self.settings_frame, values=setting.options, command=on_segmented_changed
        )
        segmented.grid(row=grid_row, column=1, padx=5, pady=self._pady, sticky=ctk.E)
        segmented.set(str(setting.value))

    def _create_slider_widget(self, setting: RangeSetting, grid_row: int) -> None:
        on_slider_changed = lambda value, setting=setting: self.settings.set_value(
            setting.name, value
        )
        slider = Slider(
            self.settings_frame,
            from_=setting.min_value,
            to=setting.max_value,
            command=on_slider_changed,
        )
        slider.grid(row=grid_row, column=1, pady=self._pady, sticky=ctk.E, padx=(50, 0))
        slider.set(setting.value)

    def _create_entry_widget(self, setting: Setting, grid_row: int) -> None:
        entry_setting_value = ctk.CTkEntry(self.settings_frame)
        entry_setting_value.grid(row=grid_row, column=1, padx=5, pady=self._pady)
        if type(entry_setting_value) is ctk.CTkEntry:
            entry_setting_value.insert(ctk.END, setting.value)
            entry_setting_value.bind(
                "<KeyRelease>",
                lambda event, setting=setting: self._entry_changed(event, setting),
            )

    def _create_checkbox_widget(self, setting: Setting, grid_row: int) -> None:
        on_checkbox_changed = lambda: self.settings.set_value(
            setting.name, checkbox.get()
        )
        checkbox = ctk.CTkCheckBox(self.settings_frame, text="")
        checkbox.configure(command=on_checkbox_changed)
        if setting.value:
            checkbox.select()
        checkbox.grid(row=grid_row, column=1, sticky=ctk.E)
        self.create_description_tooltip(checkbox, setting.description)

    @staticmethod
    def create_description_tooltip(widget, description: str) -> None:
        if description:
            ToolTip(widget, description)

    def _clean_name(self, name: str) -> str:
        """Return string without underscores and with title case."""
        return name.replace("_", " ").title()

    def _entry_changed(self, event, setting: Setting) -> None:
        if event.keysym != "Return":
            return
        entry = event.widget
        value = entry.get()
        if len(value) == 0:
            return
        self.settings.set_value(setting.name, value)
        entry.delete("0", ctk.END)
        entry.insert(ctk.END, self.settings.get(setting.name).value)
