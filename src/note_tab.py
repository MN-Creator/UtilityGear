import customtkinter as ctk
from tab import Tab
from textbox import Textbox

class NoteTab(Tab):
    def create_content(self):
        self._create_settings()
        self.font = "TkDefaultFont"
        self.text = Textbox(self.tab, font=(self.font, self.font_size_setting.value))
        self.text.pack(fill=ctk.BOTH, expand=True)

    def _create_settings(self):
        options = [12, 14, 16, 18, 20]
        self.font_size_setting = self.app.settings.create_option("notepad_font_size", options[0], options=options, parent="Notepad")
        self.font_size_setting.on_change = self._set_font_size
        
    def _set_font_size(self):
        font_size = self.font_size_setting.value
        self.text.configure(font=(self.font, font_size))