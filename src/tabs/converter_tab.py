import customtkinter as ctk
from .tab import Tab
from widgets import Entry


class ConverterTab(Tab):
    def create_content(self):
        self._converter = Converter()
        self._create_widgets()
        self._input_box.bind("<KeyRelease>", lambda event: self._on_input_changed())

    def _create_widgets(self) -> None:
        self._input_box = ctk.CTkEntry(self.tab, placeholder_text="5 cm")
        self._input_box.pack(fill="x", pady=8)
        self._output_box = Entry(self.tab, state="readonly")
        self._output_box.pack(fill="x", pady=8)

    def _on_input_changed(self):
        """Get the input text and try to convert it"""
        text = self._input_box.get()
        text = text.strip()
        text_split = text.split(" ")
        # Must be at least three characters (e.g. 5 f) and two words.
        if len(text) < 3 or len(text_split) < 2:
            self._output_box.set_text_in_readonly("")
            return
        value = text_split[0]
        unit = text_split[1]

        if self.is_number(value):
            unit = unit.lower()
            try:
                value, unit = self._converter.convert(float(value), unit)
                self._set_output_text(value, unit)
            except KeyError:
                return

    @staticmethod
    def get_number_unit_from_text(text: str) -> tuple[float, str]:
        text_split = text.split(" ")
        value = text_split[0]
        unit = text_split[1]
        return float(value), unit

    @staticmethod
    def is_number(value: str) -> bool:
        only_numbers = value.replace(".", "", 1)
        only_numbers = only_numbers.replace("-", "", 1)
        return only_numbers.isnumeric()

    def _set_output_text(self, value: float, unit: str) -> None:
        text = str(value) + " " + unit
        self._output_box.set_text_in_readonly(text)


class Converter:
    def __init__(self):
        self._create_converter_dict()

    def _create_converter_dict(self) -> None:
        self._converter_dict = {
            "c": Conversions.convert_celcius_to_farenheit,
            "f": Conversions.convert_farenheit_to_celcius,
            "cm": Conversions.convert_cm_to_inches,
            "inch": Conversions.convert_inches_to_cm,
            "inches": Conversions.convert_inches_to_cm,
        }

    def convert(
        self, value: float, unit: str, decimal_places: int = 2
    ) -> tuple[float, str]:
        output_value, output_unit = self._converter_dict[unit](value)
        output_value = "{:.{}f}".format(output_value, decimal_places)
        return output_value, output_unit


class Conversions:
    @staticmethod
    def convert_celcius_to_farenheit(celcius: float) -> tuple[float, str]:
        farenheit = (celcius * (9 / 5)) + 32
        return farenheit, "F"

    @staticmethod
    def convert_farenheit_to_celcius(farenheit: float) -> tuple[float, str]:
        celsius = (farenheit - 32) * (5 / 9)
        return celsius, "C"

    @staticmethod
    def convert_cm_to_inches(cm: float) -> tuple[float, str]:
        return cm / 2.54, "inch"

    @staticmethod
    def convert_inches_to_cm(inches: float) -> tuple[float, str]:
        return inches * 2.54, "cm"
