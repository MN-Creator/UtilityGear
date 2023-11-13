import customtkinter as ctk
from tab import Tab
from entry import Entry
from textbox import Textbox
import re

class TextManipulatorTab(Tab):
    def create_content(self):
        self.create_manipulators()
        self.current_manipulator = self.manipulators["Title"]
        self.create_widgets()
    
    def create_manipulators(self):
        self.manipulators = {}
        title = TextManipulator("Title", lambda text: text.title())
        self.manipulators[title.name] = title
        whitespace = TextManipulator("Space", self.refine_text)
        self.manipulators[whitespace.name] = whitespace
        upper = TextManipulator("Uppercase", lambda text: text.upper())
        self.manipulators[upper.name] = upper
        lower = TextManipulator("Lowercase", lambda text: text.lower())
        self.manipulators[lower.name] = lower
        sort_alpha = TextManipulator("Sort Ascending", self.sort_text_asc)
        self.manipulators[sort_alpha.name] = sort_alpha
        sort_desc = TextManipulator("Sort Descending", self.sort_text_desc)
        self.manipulators[sort_desc.name] = sort_desc
        unique_lines = TextManipulator("Unique", self.unique_lines)
        self.manipulators[unique_lines.name] = unique_lines
        
    def refine_text(self, text):
        text = text.strip()
        # Remove extra whitespace.
        text = " ".join(text.split())
        return text

    def sort_text_asc(self, text):
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = sorted(text_list)
        return "\n".join(text_list)

    def sort_text_desc(self, text):
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = sorted(text_list, reverse=True)
        return "\n".join(text_list)

    def unique_lines(self, text):
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = list(set(text_list))
        return "\n".join(text_list)

    def create_widgets(self):
        self.create_main_frame()
        self.input_box = Textbox(self.frame)
        self.input_box.grid(row=0, column=0, padx=2, sticky=ctk.NSEW)
        self.input_box.bind("<KeyRelease>", self.input_changed)
        options = list(self.manipulators.keys())
        self.option_dropdown = ctk.CTkOptionMenu(self.frame, values=options, command=self.on_option_changed)
        self.option_dropdown.grid(row=1, column=0, padx=2, sticky=ctk.EW)
        self.option_dropdown.set(self.current_manipulator.name)
        self.output_box = ctk.CTkTextbox(self.frame, state="disabled")
        self.output_box.grid(row=0, column=1, padx=2, sticky=ctk.NSEW)

    def create_main_frame(self):
        self.frame = ctk.CTkFrame(self.tab)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

    def on_option_changed(self, _):
        self.current_manipulator = self.manipulators[self.option_dropdown.get()]
        self.input_changed(_)

    def input_changed(self, _):
        text = self.input_box.get("1.0", "end")
        changed_text = self.current_manipulator.change_text(text)
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", ctk.END)
        self.output_box.insert("1.0", changed_text)
        self.output_box.configure(state="disabled")

    def copy_output(self):
        self.output_box.clipboard_clear()
        self.output_box.clipboard_append(self.output_box.get("1.0", "end"))

class TextManipulator:
    def __init__(self, name, function):
        self.name = name
        self.function = function
    
    def change_text(self, text):
        return self.function(text)