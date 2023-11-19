import customtkinter as ctk
from tab import Tab

class TestTab(Tab):
    def create_content(self):
        self._create_widgets()
    
    def _create_widgets(self):
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_rowconfigure(0, weight=1)
        frame = ctk.CTkFrame(self.tab)
        frame.grid(row=0, column=0, sticky="nsew")
        self.checkbox1 = ctk.CTkCheckBox(frame, text="Checkbox 1")
        self.checkbox1.pack()
        self.checkbox2 = ctk.CTkCheckBox(frame, text="Checkbox 2")
        self.checkbox2.pack()