import os
import json

class SettingsManager:
    def __init__(self):
        self.settings_file = "app_settings.json"
        self.settings = dict()
        self._create_settings_file()
        self._load_settings()
    
    def _create_settings_file(self):
        # Create a settings file if it doesn't exist.
        if(not os.path.exists(self.settings_file)):
            with open(self.settings_file, "w") as file:
                file.write("")
    
    def _load_settings(self):
        if(os.stat(self.settings_file).st_size == 0):
            return
        with open(self.settings_file, "r") as file:
            output = json.load(file)
        for key, value in output.items():
            self.settings[key] = Setting.from_dict(value)
    
    def _save_settings(self):
        save_json = dict()
        for key, value in self.settings.items():
            save_json[key] = value.to_dict()
        with open(self.settings_file, "w") as file:
            json.dump(save_json, file, indent=4)
    
    def clear_settings(self):
        """Remove all settings."""
        self.settings = {}
        self._save_settings()

    def create(self, name, default_value, hidden=False, parent=""):
        """Create a setting with a default value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            self.settings[name] = Setting(name, default_value, default_value, hidden, parent)
            self._save_settings()
        return self.settings[name]

    def create_range(self, name, default_value, min_value, max_value, hidden=False, parent=""):
        """Create a setting that can have a value between min_value and max_value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].min_value = min_value
            self.settings[name].max_value = max_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            self.settings[name] = Setting(name, default_value, default_value, 
                                          hidden, parent, min_value=min_value, max_value=max_value)
            self._save_settings()
        return self.settings[name]

    def create_option(self, name, default_value, options, hidden=False, parent=""):
        """Create a setting that can have a value from a list of options."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].options = Setting.to_str_list(options)
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            options_str_list = Setting.to_str_list(options)
            self.settings[name] = Setting(name, default_value, default_value, 
                                          hidden, parent, options=options_str_list)
            self._save_settings()
        return self.settings[name]

    def get(self, name, default_value=None):
        """Get a setting by name, returns a new setting if not found."""
        try:
            return self.settings[name]
        except KeyError:
            self.settings[name] = Setting(name, default_value, default_value)
            self._save_settings()
            return name

    def get_float(self, name):
        """Returns the value of a setting as a float."""
        return float(self.get(name).value)

    def get_int(self, name):
        """Returns the value of a setting as an int."""
        return int(self.get(name).value)

    def set_value(self, name, value):
        """Set the value of a setting by name, creates a new setting if not found."""
        try:
            self.settings[name].set_value(value)
            self._save_settings()
        except KeyError:
            self.settings[name] = Setting(name, value)
            self._save_settings()

class Setting:
    def __init__(self, name, value, default_value=None, hidden=False, parent="",
                 on_change=None, options=None, min_value=None, max_value=None):
        self.name = name
        self.value = value
        self.value_type = type(value)
        self.default_value = default_value
        self.hidden = hidden
        self.parent = parent
        self.on_change = on_change
        self.options = options
        self.min_value = min_value
        self.max_value = max_value
    
    @staticmethod
    def from_dict(dict):
        """"Create a setting from a dictionary."""
        setting = Setting(dict["name"], dict["value"])
        if "default_value" in dict:
            setting.default_value = dict["default_value"]
        if "type" in dict:
            setting.value_type = Setting._determine_value_type(dict)
        if "hidden" in dict:
            setting.hidden = dict["hidden"]
        if "parent" in dict:
            setting.parent = dict["parent"]
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
        value = self._clamp(value)
        if self.value_type is not None:
            value = self.value_type(value)
        self.value = value
        if self.on_change is not None:
            self.on_change()
    
    def _clamp(self, value):
        """Clamp a value between min_value and max_value."""
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
            "parent": self.parent,
            "options": self.options,
            "type": str(self.value_type),
        }