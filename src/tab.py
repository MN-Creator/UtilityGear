import customtkinter as ctk
from entry import Entry
import keyboard
from textbox import Textbox

class Tab():
    def __init__(self, app, tabview, title, visibility_setting=True):
        self.title = title
        self.app = app
        if visibility_setting:
            tab_visible_setting = self._create_visibility_setting()
            if not tab_visible_setting.value:
                return
        self.tab = tabview.add(title)
        self.create_content()
    
    def _create_visibility_setting(self):
        tab_setting_name = self.title + "_Tab_visible"
        return self.app.settings.create(tab_setting_name, True)
