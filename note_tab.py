from tab import Tab
from textbox import Textbox

class NoteTab(Tab):
    def create_content(self):
        # Font size setting.
        self._create_settings()
        self.text = Textbox(self.tab)
        self.text.pack(fill="both", expand=True)

    def _create_settings(self):
        options = [12, 14, 16, 18, 20]
        font_size_setting = self.app.settings.create("font_size", 12, options=options, min_value=8, max_value=20)
        font_size_setting.on_change = self._set_font_size
        
    def _set_font_size(self):
        font_size = self.app.settings.get_int("font_size")
        self.text.configure(font=("TkDefaultFont", font_size))