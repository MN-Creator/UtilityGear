import customtkinter as ctk

class Textbox(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Control-Key-c>", self._copy)
        self.bind("<Control-Key-BackSpace>", self._remove_word)
    
    def on_key_released(self, function):
        self.bind("<KeyRelease>", function)
    
    def on_visible(self, function):
        self.bind("<Visibility>", function)
    
    def _copy(self, _):
        # If text is not selected, copy all text.
        if not self.tag_ranges(ctk.SEL):
            self.clipboard_clear()
            self.clipboard_append(self.get("1.0", "end"))
    
    def _remove_word(self, _):
        self.delete("insert-1c wordstart", "insert")