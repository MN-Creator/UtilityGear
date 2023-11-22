import customtkinter as ctk
from .tab import Tab
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
        regex = TextManipulator("Regex", self._regex)
        self.manipulators[regex.name] = regex
        self.regex_inputbox = None

    def refine_text(self, text: str) -> str:
        text = text.strip()
        text = " ".join(text.split())
        return text

    def sort_text_asc(self, text: str) -> str:
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = sorted(text_list)
        return "\n".join(text_list)

    def sort_text_desc(self, text: str) -> str:
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = sorted(text_list, reverse=True)
        return "\n".join(text_list)

    def unique_lines(self, text: str) -> str:
        text_list = text.split("\n")
        text_list = [line for line in text_list if len(line) > 0]
        text_list = list(set(text_list))
        return "\n".join(text_list)

    def create_widgets(self):
        self.configure_main_frame()
        self.input_box = Textbox(self.tab)
        self.input_box.grid(row=0, column=0, padx=2, sticky=ctk.NSEW)
        self.input_box.bind("<KeyRelease>", self.input_changed)
        self.output_box = ctk.CTkTextbox(self.tab, state="disabled")
        self.output_box.grid(row=0, column=1, padx=2, sticky=ctk.NSEW)
        options = list(self.manipulators.keys())
        self.option_dropdown = ctk.CTkOptionMenu(
            self.tab, values=options, command=self.on_option_changed
        )
        self.option_dropdown.grid(row=1, column=0, padx=2, pady=(5, 0), sticky="SEW")
        self.option_dropdown.set(self.current_manipulator.name)

    def configure_main_frame(self):
        self.tab.columnconfigure(0, weight=1)
        self.tab.columnconfigure(1, weight=1)
        self.tab.rowconfigure(0, weight=1, minsize=250)
        self.tab.rowconfigure(1, weight=0)

    def on_option_changed(self, _):
        self.current_manipulator = self.manipulators[self.option_dropdown.get()]
        self._handle_regex_inputbox()
        self.input_changed(_)

    def _handle_regex_inputbox(self):
        if self.current_manipulator.name == "Regex":
            self._create_regex_widget()
        elif self.regex_inputbox is not None:
            self.regex_inputbox.destroy()
            self.regex_inputbox = None

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

    def _create_regex_widget(self):
        self.regex_inputbox = ctk.CTkEntry(
            self.tab, placeholder_text="Press enter to apply regex"
        )
        self.regex_inputbox.grid(row=1, column=1, padx=2, pady=(5, 0), sticky="SEW")
        self.regex_inputbox.bind("<Return>", self.input_changed)

    def _regex(self, text: str) -> str:
        regex_text = self.regex_inputbox.get()
        regex_text = regex_text.strip()
        if len(text) == 0 or len(regex_text) == 0:
            return ""
        regex = self._compile_regex(regex_text)
        if regex is None:
            return "(Invalid regex)"
        matches = regex.findall(text)
        if matches is None:
            return ""
        return matches

    def _compile_regex(self, regex_text: str):
        try:
            regex = re.compile(regex_text)
            return regex
        except re.error:
            return None


class TextManipulator:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def change_text(self, text: str) -> str:
        return self.function(text)
