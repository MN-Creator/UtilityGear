import customtkinter as ctk
import keyboard
from tabview import TabView
from settings_manager import SettingsManager
from settings_tab import SettingsTab
from converter_tab import ConverterTab
from note_tab import NoteTab
from text_manipulator_tab import TextManipulatorTab


class App(ctk.CTk):
    def __init__(self, title: str):
        super().__init__()
        self._title = title
        self.title(title)
        self._create_settings()
        self._setup_window()
        self._setup_bindings()
        self._create_tabs()

    def _setup_bindings(self):
        self.bind("<Alt-KeyPress-z>", lambda event: self.destroy())
        keyboard.add_hotkey("alt+q", self.toggle_window)

    def _setup_window(self):
        self.wm_attributes("-topmost", self._aot_setting.value)
        self.overrideredirect(not self._show_titlebar_setting.value)
        self._set_transparency()
        self._set_window_theme()
        self.rescale_window()

    def _create_settings(self):
        self.settings = SettingsManager()
        self._create_window_size_settings()
        self._show_titlebar_setting = self.settings.create(
            "show_titlebar", default_value=True
        )
        self._create_always_on_top_setting()
        self._create_window_transparency_setting()
        self._create_window_theme_setting()

    def _create_always_on_top_setting(self):
        self._aot_setting = self.settings.create("always_on_top", default_value=True)
        self._aot_setting.on_change = self._set_always_on_top

    def _create_window_transparency_setting(self):
        self.transparency_setting = self.settings.create_range(
            "transparency", default_value=95, min_value=50, max_value=100
        )
        self.transparency_setting.on_change = self._set_transparency

    def _create_window_theme_setting(self):
        theme_options = ["system", "light", "dark"]
        self._window_theme_setting = self.settings.create_option(
            "window_theme", "system", options=theme_options
        )
        self._window_theme_setting.on_change = self._set_window_theme

    def _create_window_size_settings(self):
        window_width_setting = self.settings.create_range(
            "window_width", default_value=400, min_value=300, max_value=700, hidden=True
        )
        window_height_setting = self.settings.create_range(
            "window_height",
            default_value=400,
            min_value=300,
            max_value=700,
            hidden=True,
        )
        window_width_setting.on_change = self.rescale_window
        window_height_setting.on_change = self.rescale_window

    def _set_always_on_top(self):
        self.wm_attributes("-topmost", self._aot_setting.value)

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

    def set_window_size(self, width: int, height: int):
        self.window_width = width
        self.window_height = height
        screen_width = self.winfo_screenwidth()
        offset_x = 20
        offset_y = 20
        self.window_x = screen_width - (self.window_width + offset_x)
        self.window_y = offset_y
        self.geometry("{}x{}+{}+{}".format(width, height, self.window_x, self.window_y))
        self.minsize(350, 350)

    def _create_tabs(self):
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        NoteTab(self, self.tabview, "Notepad")
        ConverterTab(self, self.tabview, "Converter")
        TextManipulatorTab(self, self.tabview, "Text")
        SettingsTab(self, self.tabview, "Settings")
        self.tabview.bind_keys()

    def _on_window_open(self):
        if self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def minimize_window(self):
        if self.state() == "normal":
            self.withdraw()
