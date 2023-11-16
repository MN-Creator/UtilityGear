import customtkinter as ctk
from tab import Tab

class SettingsTab(Tab):
    def __init__(self, app, tabview, title):
        super().__init__(app, tabview, title, visibility_setting=False)

    def create_content(self):
        self.settings = self.app.settings
        self.create_settings_widgets()

    def create_settings_widgets(self):
        self.settings_frame = ctk.CTkScrollableFrame(self.tab)
        self.settings_frame.pack(fill="both", expand=True)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.exit_button = ctk.CTkButton(self.tab, text="Exit", command=self.app.destroy)
        self.exit_button.pack(fill="x", pady=8)
        grid_row = 0
        for setting in self.settings.settings.values():
            self.draw_setting(setting, grid_row)
            grid_row += 1

    def draw_setting(self, setting, grid_row):
        if setting.hidden:
            return
        clean_name = self.clean_name(setting.name)
        label_name = ctk.CTkLabel(self.settings_frame, text=clean_name)
        label_name.grid(row=grid_row, column=0, pady=5, sticky=ctk.W)
        if setting.options is not None:
            if len(setting.options) <= 5:
                self.create_segmented_widget(setting, grid_row)
                return
            self.create_dropdown_widget(setting, grid_row)
            return
        if setting.value_type is bool:
            self.create_checkbox_widget(setting, grid_row)
            return
        elif setting.min_value is not None and setting.max_value is not None:
            on_slider_changed = lambda value, setting=setting: self.settings.set(setting.name, value)
            slider = ctk.CTkSlider(self.settings_frame, from_=setting.min_value, to=setting.max_value, 
                            command=on_slider_changed)
            slider.grid(row=grid_row, column=1, pady=5)
            return
        self.create_entry_widget(setting, grid_row)

    def create_dropdown_widget(self, setting, grid_row):
        on_dropdown_changed = lambda value, setting=setting: self.settings.set(setting.name, setting.value_type(value))
        # Convert each option to a string.
        options_str_list = [str(option) for option in setting.options]
        dropdown = ctk.CTkOptionMenu(self.settings_frame, values=options_str_list, command=on_dropdown_changed)
        dropdown.grid(row=grid_row, column=1, padx=5, pady=5, sticky=ctk.E)
        dropdown.set(str(setting.value))

    def create_segmented_widget(self, setting, grid_row):
        on_segmented_changed = lambda value, setting=setting: self.settings.set(setting.name, setting.value_type(value))
        segmented = ctk.CTkSegmentedButton(self.settings_frame, values=setting.options, command=on_segmented_changed)
        segmented.grid(row=grid_row, column=1, padx=5, pady=5, sticky=ctk.E)
        segmented.set(str(setting.value))

    def create_entry_widget(self, setting, grid_row):
        entry_setting_value = ctk.CTkEntry(self.settings_frame)
        entry_setting_value.grid(row=grid_row, column=1, padx=5, pady=5)
        if type(entry_setting_value) is ctk.CTkEntry:
            entry_setting_value.insert(ctk.END, setting.value)
            entry_setting_value.bind("<KeyRelease>", lambda event, setting=setting: self.entry_changed(event, setting))

    def create_checkbox_widget(self, setting, grid_row):
        on_checkbox_changed = lambda: self.settings.set(setting.name, checkbox.get())
        checkbox = ctk.CTkCheckBox(self.settings_frame, text="")
        checkbox.configure(command=on_checkbox_changed)
        if setting.value:
            checkbox.select()
        checkbox.grid(row=grid_row, column=1, sticky=ctk.E)

    def clean_name(self, name):
        return name.replace("_", " ").title()

    def entry_changed(self, event, setting):
        if event.keysym != "Return":
            return
        entry = event.widget
        value = entry.get()
        if len(value) == 0:
            return
        self.settings.set(setting.name, value)
        entry.delete("0", ctk.END)
        entry.insert(ctk.END, self.settings.get(setting.name).value)