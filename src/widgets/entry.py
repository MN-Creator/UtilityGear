import customtkinter as ctk


class Entry(ctk.CTkEntry):
    def set_text(self, text: str):
        self.delete(0, ctk.END)
        self.insert(0, text)

    def set_text_in_readonly(self, text: str):
        self.configure(state="normal")
        self.set_text(text)
        self.configure(state="readonly")

    def append(self, text: str):
        self.insert(ctk.END, text)

    def on_key_released(self, function: callable):
        self.bind("<KeyRelease>", lambda event: function())
