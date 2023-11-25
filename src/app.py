import customtkinter as ctk
import keyboard

from settings_manager import SettingsManager
from storage import Storage
from tabview import TabView
from Tabs import NoteTab
from Tabs import ConverterTab
from Tabs import TextManipulatorTab
from Tabs import SettingsTab


class App(ctk.CTk):
    """Root application window."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self._title = title
        self.title(title)
        self.storage = Storage(self._title + "_storage.json")
        self._create_settings()
        self._setup_window()
        self._setup_bindings()
        self._create_tabs()

    def _setup_bindings(self) -> None:
        self.bind("<Alt-KeyPress-z>", lambda event: self.destroy())
        keyboard.add_hotkey("alt+q", self.toggle_window)

    def _setup_window(self) -> None:
        self.wm_attributes("-topmost", self._aot_setting.value)
        self.overrideredirect(not self._show_titlebar_setting.value)
        self._set_transparency()
        self._set_window_theme()
        self.rescale_window()

    def _create_settings(self) -> None:
        self.settings = SettingsManager(self.storage)
        self._create_window_size_settings()
        self._create_toolbar_setting()
        self._create_always_on_top_setting()
        self._create_window_transparency_setting()
        self._create_window_theme_setting()

    def _create_toolbar_setting(self) -> None:
        DESC = "Show or hide the window titlebar at the top of the window."
        self._show_titlebar_setting = self.settings.create(
            "show_titlebar", default_value=True, parent="", desc=DESC
        )

    def _create_always_on_top_setting(self) -> None:
        DESC = "Keep the window on top of other windows."
        self._aot_setting = self.settings.create(
            "always_on_top", default_value=True, desc=DESC
        )
        self._aot_setting.on_change = self._set_always_on_top

    def _create_window_transparency_setting(self) -> None:
        DESC = "Set the transparency of the window."
        self.transparency_setting = self.settings.create_range(
            "transparency", default_value=95, min_value=50, max_value=100, desc=DESC
        )
        self.transparency_setting.on_change = self._set_transparency

    def _create_window_theme_setting(self) -> None:
        theme_options = ["system", "light", "dark"]
        self._window_theme_setting = self.settings.create_option(
            "window_theme", "system", options=theme_options
        )
        self._window_theme_setting.on_change = self._set_window_theme

    def _create_window_size_settings(self) -> None:
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

    def _set_always_on_top(self) -> None:
        self.wm_attributes("-topmost", self._aot_setting.value)

    def _set_transparency(self) -> None:
        self.attributes("-alpha", self.transparency_setting.value / 100)

    def _set_window_theme(self) -> None:
        ctk.set_appearance_mode(self._window_theme_setting.value)

    def rescale_window(self) -> None:
        self.window_width = self.settings.get_int("window_width")
        self.window_height = self.settings.get_int("window_height")
        self.set_window_size(self.window_width, self.window_height)
        self.minsize(350, 350)
        self.maxsize(700, 700)

    def toggle_window(self) -> None:
        if self.state() == "normal":
            self.withdraw()
        elif self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def set_window_size(self, width: int, height: int) -> None:
        self.window_width = width
        self.window_height = height
        screen_width = self.winfo_screenwidth()
        offset_x = 20
        offset_y = 20
        self.window_x = screen_width - (self.window_width + offset_x)
        self.window_y = offset_y
        self.geometry("{}x{}+{}+{}".format(width, height, self.window_x, self.window_y))

    def _create_tabs(self) -> None:
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        NoteTab(self, self.tabview, "Notepad")
        ConverterTab(self, self.tabview, "Converter")
        TextManipulatorTab(self, self.tabview, "Text")
        SettingsTab(self, self.tabview, "Settings")
        self.tabview.bind_keys()

    def _on_window_open(self) -> None:
        if self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def minimize_window(self) -> None:
        if self.state() == "normal":
            self.withdraw()
