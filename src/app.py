import customtkinter as ctk
import keyboard
from tabview import TabView
from settings_manager import SettingsManager
from settings_tab import SettingsTab
from converter_tab import ConverterTab
from note_tab import NoteTab
from text_manipulator_tab import TextManipulatorTab


class App(ctk.CTk):
    def __init__(self, title):
        super().__init__()
        self.title_name = title
        self.title(title)
        self.create_settings()
        self.setup_window()
        self.setup_bindings()
        self.create_widgets()

    def setup_bindings(self):
        self.bind("<Alt-KeyPress-z>", lambda event: self.destroy())
        keyboard.add_hotkey("alt+q", self.toggle_window)

    def setup_window(self):
        self.wm_attributes("-topmost", self.settings.get("always_on_top").value)
        self.overrideredirect(not self.settings.get("show_titlebar").value)
        self._set_transparency()
        self._set_window_theme()
        self.rescale_window()

    def create_settings(self):
        self.settings = SettingsManager()
        self.create_window_size_settings()
        aot_setting = self.settings.create("always_on_top", default_value=True)
        aot_setting.on_change = self.set_always_on_top
        self.settings.create("show_titlebar", default_value=True)
        self.transparency_setting = self.settings.create_range(
            "transparency", 95, 50, 100
        )
        self.transparency_setting.on_change = self._set_transparency
        theme_options = ["system", "light", "dark"]
        self._window_theme_setting = self.settings.create_option(
            "window_theme", "system", options=theme_options
        )
        self._window_theme_setting.on_change = self._set_window_theme

    def create_window_size_settings(self):
        window_width_setting = self.settings.create_range(
            "window_width", 400, 300, 700, hidden=True
        )
        window_height_setting = self.settings.create_range(
            "window_height", 400, 300, 700, hidden=True
        )
        window_width_setting.on_change = self.rescale_window
        window_height_setting.on_change = self.rescale_window

    def set_always_on_top(self):
        self.wm_attributes("-topmost", self.settings.get("always_on_top").value)

    def _set_transparency(self):
        self.attributes("-alpha", self.transparency_setting.value / 100)

    def _set_window_theme(self):
        ctk.set_appearance_mode(self._window_theme_setting.value)

    def rescale_window(self):
        self.window_width = self.settings.get_int("window_width")
        self.window_height = self.settings.get_int("window_height")
        self.set_window_size(self.window_width, self.window_height)

    def toggle_window(self):
        if self.state() == "normal":
            self.withdraw()
        elif self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def set_window_size(self, width, height):
        self.window_width = width
        self.window_height = height
        screen_width = self.winfo_screenwidth()
        offset_x = 20
        offset_y = 20
        self.window_x = screen_width - (self.window_width + offset_x)
        self.window_y = offset_y
        self.geometry("{}x{}+{}+{}".format(width, height, self.window_x, self.window_y))
        self.minsize(350, 350)

    def create_widgets(self):
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        NoteTab(self, self.tabview, "Notepad")
        ConverterTab(self, self.tabview, "Converter")
        TextManipulatorTab(self, self.tabview, "Text")
        SettingsTab(self, self.tabview, "Settings")
        self.tabview.bind_keys()

    def on_window_open(self):
        if self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def minimize_window(self):
        if self.state() == "normal":
            self.withdraw()
