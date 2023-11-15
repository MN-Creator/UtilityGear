import customtkinter as ctk
import keyboard
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
        self.attributes("-alpha", 0.95)
        self.rescale_window()

    def create_settings(self):
        self.settings = SettingsManager()
        window_width_setting = self.settings.create("window_width", 400, hidden=True, 
                                                            min_value=300, max_value=700)
        window_height_setting = self.settings.create("window_height", 400, hidden=True,
                                                             min_value=300, max_value=700)
        window_width_setting.on_change = self.rescale_window
        window_height_setting.on_change = self.rescale_window
        aot_setting = self.settings.create("always_on_top", default_value=True)
        aot_setting.on_change = self.set_always_on_top
        self.settings.create("show_titlebar", default_value=True)

    def set_always_on_top(self):
        self.wm_attributes("-topmost", self.settings.get("always_on_top").value)

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
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        TextManipulatorTab(self, self.tabview, "Text")
        NoteTab(self, self.tabview, "Notepad")
        ConverterTab(self, self.tabview, "Converter")
        SettingsTab(self, self.tabview, "Settings")

    def on_window_open(self):
        if self.state() == "withdrawn" or self.state() == "iconic":
            self.deiconify()

    def minimize_window(self):
        if self.state() == "normal":
            self.withdraw()
