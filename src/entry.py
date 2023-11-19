import customtkinter as ctk


class Entry(ctk.CTkEntry):
    def set_text(self, text):
        self.delete(0, ctk.END)
        self.insert(0, text)

    def set_text_in_readonly(self, text):
        self.configure(state="normal")
        self.set_text(text)
        self.configure(state="readonly")

    def append(self, text):
        self.insert(ctk.END, text)

    def on_key_released(self, function):
        self.bind("<KeyRelease>", lambda event: function())
