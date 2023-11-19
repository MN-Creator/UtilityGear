import customtkinter as ctk


class Textbox(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Control-Key-c>", lambda _: self._copy)
        self.bind("<Control-Key-BackSpace>", lambda _: self._remove_word)

    def on_key_released(self, function: callable):
        self.bind("<KeyRelease>", function)

    def on_visible(self, function: callable):
        self.bind("<Visibility>", function)

    def _copy(self):
        # If text is not selected, copy all text.
        if not self.tag_ranges(ctk.SEL):
            self.clipboard_clear()
            self.clipboard_append(self.get("1.0", "end"))

    def _remove_word(self):
        self.delete("insert-1c wordstart", "insert")
