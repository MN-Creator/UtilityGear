import customtkinter as ctk
from tab import Tab
from entry import Entry


class ConverterTab(Tab):
    def create_content(self):
        self._create_converter_dict()
        self._create_widgets()
        self._input_box.bind("<KeyRelease>", lambda event: self._input_changed())

    def _create_widgets(self):
        self._input_box = ctk.CTkEntry(self.tab, placeholder_text="5 cm")
        self._input_box.pack(fill="x", pady=8)
        self._output_box = Entry(self.tab, state="readonly")
        self._output_box.pack(fill="x", pady=8)

    def _create_converter_dict(self):
        self._converter_dict = {
            "c": self._convert_celcius_to_farenheit,
            "f": self._convert_farenheit_to_celcius,
            "cm": self._convert_cm_to_inches,
            "inch": self._convert_inches_to_cm,
            "inches": self._convert_inches_to_cm,
        }

    def _input_changed(self):
        text = self._input_box.get()
        text_split = text.split(" ")
        if len(text) < 3 or len(text_split) < 2:
            self._output_box.set_text_in_readonly("")
            return
        value = text_split[0]
        unit = text_split[1]
        if value.isnumeric():
            unit = unit.lower()
            try:
                self._converter_dict[unit](float(value))
            except KeyError:
                return

    def _convert_farenheit_to_celcius(self, farenheit: float):
        celsius = (farenheit - 32) * (5 / 9)
        celsius = "{:.2f}".format(celsius)
        self._set_output_text(celsius, "C")

    def _convert_celcius_to_farenheit(self, celcius: float):
        farenheit = (celcius * (9 / 5)) + 32
        farenheit = "{:.2f}".format(farenheit)
        self._set_output_text(farenheit, "F")

    def _convert_cm_to_inches(self, cm: float):
        output = cm / 2.54
        output = "{:.2f}".format(output)
        self._set_output_text(output, "inch")

    def _convert_inches_to_cm(self, inches: float):
        value = inches * 2.54
        value = "{:.2f}".format(value)
        self._set_output_text(value, "cm")

    def _set_output_text(self, value: float, unit: str):
        text = str(value) + " " + unit
        self._output_box.set_text_in_readonly(text)
