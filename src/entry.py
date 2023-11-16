import customtkinter as ctk

class Entry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_text(self, text):
        self.delete(0, ctk.END)
        self.insert(0, text)
    
    def append(self, text):
        self.insert(ctk.END, text)

    def on_key_released(self, function):
        self.bind("<KeyRelease>", lambda event: function())