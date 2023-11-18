import customtkinter as ctk
from tab import Tab
from entry import Entry

class ConverterTab(Tab):
    def create_content(self):
        self.create_converter_dict()
        self.create_conversions()
        self.create_widgets()
        self.input_box.bind("<KeyRelease>", lambda event: self.input_changed())

    def create_widgets(self):
        self.input_box = ctk.CTkEntry(self.tab, placeholder_text="5 cm")
        self.input_box.pack(fill="x", pady=8)
        self.output_box = Entry(self.tab)
        self.output_box.pack(fill="x", pady=8)

    def create_conversions(self):
        self.conversions = []
        farenheit_celsius_conv = Conversion("F", "C", self.convert_farenheit_to_celcius)
        self.conversions.append(farenheit_celsius_conv)
        celsius_farenheit_conv = Conversion("C", "F", self.convert_celcius_to_farenheit)
        self.conversions.append(celsius_farenheit_conv)
        cm_inches_conv = Conversion("cm", "inch", self.convert_cm_to_inches)
        self.conversions.append(cm_inches_conv)
        inches_cm_conv = Conversion("inch", "cm", self.convert_inches_to_cm)
        self.conversions.append(inches_cm_conv)
    
    def create_converter_dict(self):
        self.converter_dict = {
            "c": self.convert_celcius_to_farenheit,
            "f": self.convert_farenheit_to_celcius,
            "cm": self.convert_cm_to_inches,
            "inch": self.convert_inches_to_cm,
        }

    def input_changed(self):
        text = self.input_box.get()
        text_split = text.split(" ")
        if(len(text) < 3 or len(text_split) < 2):
            return
        value = text_split[0]
        unit = text_split[1]
        if(value.isnumeric()):
            unit = unit.lower()
            try:
                self.converter_dict[unit](float(value))
            except KeyError:
                return

    def convert_farenheit_to_celcius(self, farenheit):
        celsius = (farenheit - 32) * (5/9)
        celsius = "{:.2f}".format(celsius)
        self.set_output_text(celsius, "C")
    
    def convert_celcius_to_farenheit(self, celcius):
        farenheit = (celcius * (9/5)) + 32
        farenheit = "{:.2f}".format(farenheit)
        self.set_output_text(farenheit, "F")

    def convert_cm_to_inches(self, cm):
        output = cm / 2.54
        output = "{:.2f}".format(output)
        self.set_output_text(output, "inch")
    
    def convert_inches_to_cm(self, inches):
        value = inches * 2.54
        value = "{:.2f}".format(value)
        self.set_output_text(value, "cm")
    
    def set_output_text(self, value, unit):
        self.output_box.set_text(str(value) + " " + unit)

class Conversion():
    def __init__(self, from_unit, to_unit, conversion):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.conversion = conversion

    def convert(self, value):
        return self.conversion(value)