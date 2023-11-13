import os
import json

class SettingsManager:
    def __init__(self):
        self.settings_file = "app_settings.json"
        self.settings = dict()
        self.create_settings_file()
        self.load_settings()
        self.on_change_commands = dict()
        self.clamp_commands = dict()
    
    def create_settings_file(self):
        # Create a settings file if it doesn't exist.
        if(not os.path.exists(self.settings_file)):
            with open(self.settings_file, "w") as file:
                file.write("")
    
    def load_settings(self):
        if(os.stat(self.settings_file).st_size == 0):
            return
        with open(self.settings_file, "r") as file:
            output = json.load(file)
        for key, value in output.items():
            self.settings[key] = Setting.from_dict(value)
    
    def save_settings(self):
        # for setting in self.settings.values():
        #     setting.value = setting.clamp(setting.value)
        save_json = dict()
        for key, value in self.settings.items():
            save_json[key] = value.to_dict()
        with open(self.settings_file, "w") as file:
            json.dump(save_json, file, indent=4)
    
    def clear_settings(self):
        self.settings = {}
        self.save_settings()

    def create(self, setting, default_value, hidden=False, options=None, min_value=None, max_value=None):
        try:
            self.settings[setting].default_value = default_value
            self.settings[setting].hidden = hidden
            if options is not None:
                options = Setting.to_str_list(options)
            self.settings[setting].min_value = min_value
            self.settings[setting].max_value = max_value
        except KeyError:
            if options is not None:
                options = Setting.to_str_list(options)
            self.settings[setting] = Setting(setting, default_value, default_value, hidden, options=options, min_value=min_value, max_value=max_value)
            self.save_settings()
        return self.settings[setting]

    def get(self, setting, default_value="0"):
        try:
            return self.settings[setting]
        except KeyError:
            self.settings[setting] = Setting(setting, default_value, default_value)
            self.save_settings()
            return setting

    def get_float(self, setting):
        return float(self.get(setting).value)

    def get_int(self, setting):
        return int(self.get(setting).value)

    def set(self, setting, value):
        try:
            self.settings[setting].set_value(value)
            self.save_settings()
        except KeyError:
            self.settings[setting] = Setting(setting, value)
            self.save_settings()

class Setting:
    def __init__(self, name, value, default_value="0", hidden=False, on_change=None, options=None, min_value=None, max_value=None):
        self.name = name
        self.value = value
        self.value_type = type(value)
        self.default_value = default_value
        self.hidden = hidden
        self.on_change = on_change
        self.options = options
        self.min_value = min_value
        self.max_value = max_value
    
    @staticmethod
    def from_dict(dict):
        setting = Setting(dict["name"], dict["value"])
        if "default_value" in dict:
            setting.default_value = dict["default_value"]
        if "type" in dict:
            setting.value_type = Setting._determine_value_type(dict)
        if "hidden" in dict:
            setting.hidden = dict["hidden"]
        if "options" in dict:
            setting.options = dict["options"]
        return setting
    
    @staticmethod
    def _determine_value_type(dict):
        if "int" in dict["type"]:
            return int
        elif "float" in dict["type"]:
            return float
        elif "bool" in dict["type"]:
            return bool
        return str

    @staticmethod
    def to_str_list(list):
        """Converts a list of items to a list of strings."""
        return [str(item) for item in list]

    def reset_default_value(self):
        self.value = self.default_value
    
    def set_value(self, value):
        value = self.clamp(value)
        if self.value_type is not None:
            value = self.value_type(value)
        self.value = value
        if self.on_change is not None:
            self.on_change()
    
    def clamp(self, value):
        if type(value) is str and (len(value) == 0 or not value.isnumeric()):
            return value
        if self.min_value is not None and float(value) < self.min_value:
            value = self.min_value
        elif self.max_value is not None and float(value) > self.max_value:
            value = self.max_value
        return value

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "default_value": self.default_value,
            "hidden": self.hidden,
            "options": self.options,
            "type": str(self.value_type),
        }