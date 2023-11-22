from storage import Storage


class SettingsManager:
    def __init__(self, storage: Storage):
        self._storage = storage
        self.settings = dict()
        self._load_settings()

    def _load_settings(self):
        """Load settings from storage"""
        settings_dict = self._storage.read_object("settings")
        if settings_dict is not None:
            for key, value in settings_dict.items():
                self.settings[key] = Setting.from_dict(value)

    def _save_settings(self):
        """Save settings to storage"""
        settings_dict = dict()
        for key, value in self.settings.items():
            settings_dict[key] = value.to_dict()
        self._storage.save_object("settings", settings_dict)

    def clear_settings(self):
        """Remove all settings."""
        self.settings = {}
        self._save_settings()

    def create(self, name: str, default_value, hidden=False, parent="") -> "Setting":
        """Create a setting with a default value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            self.settings[name] = Setting(
                name, default_value, default_value, hidden, parent
            )
            self._save_settings()
        return self.settings[name]

    def create_range(
        self, name: str, default_value, min_value, max_value, hidden=False, parent=""
    ) -> "Setting":
        """Create a setting that can have a value between min_value and max_value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].min_value = min_value
            self.settings[name].max_value = max_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            self.settings[name] = Setting(
                name,
                default_value,
                default_value,
                hidden,
                parent,
                min_value=min_value,
                max_value=max_value,
            )
            self._save_settings()
        return self.settings[name]

    def create_option(
        self, name: str, default_value, options: list, hidden=False, parent=""
    ) -> "Setting":
        """Create a setting that can have a value from a list of options."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].options = Setting.to_str_list(options)
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
        except KeyError:
            options_str_list = Setting.to_str_list(options)
            self.settings[name] = Setting(
                name,
                default_value,
                default_value,
                hidden,
                parent,
                options=options_str_list,
            )
        self._save_settings()
        return self.settings[name]

    def get(self, name: str, default_value=None):
        """Get a setting by name, returns a new setting if not found."""
        try:
            return self.settings[name]
        except KeyError:
            self.settings[name] = Setting(name, default_value, default_value)
            self._save_settings()
            return name

    def get_float(self, name) -> float:
        """Returns the value of a setting as a float."""
        return float(self.get(name).value)

    def get_int(self, name) -> int:
        """Returns the value of a setting as an int."""
        return int(self.get(name).value)

    def set_value(self, name: str, value):
        """Set the value of a setting by name, create a new setting if not found."""
        try:
            self.settings[name].set_value(value)
            self._save_settings()
        except KeyError:
            self.settings[name] = Setting(name, value)
            self._save_settings()


class Setting:
    def __init__(
        self,
        name: str,
        value,
        default_value=None,
        hidden=False,
        parent="",
        on_change=None,
        options=None,
        min_value=None,
        max_value=None,
    ):
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
    def from_dict(setting_dict: dict) -> "Setting":
        """ "Create a setting from a dictionary."""
        setting = Setting(setting_dict["name"], setting_dict["value"])
        if "default_value" in setting_dict:
            setting.default_value = setting_dict["default_value"]
        if "type" in setting_dict:
            setting.value_type = Setting._determine_value_type(setting_dict)
        if "hidden" in setting_dict:
            setting.hidden = setting_dict["hidden"]
        if "parent" in setting_dict:
            setting.parent = setting_dict["parent"]
        if "options" in setting_dict:
            setting.options = setting_dict["options"]
        return setting

    @staticmethod
    def _determine_value_type(setting_dict: dict) -> type:
        if "int" in setting_dict["type"]:
            return int
        elif "float" in setting_dict["type"]:
            return float
        elif "bool" in setting_dict["type"]:
            return bool
        return str

    @staticmethod
    def to_str_list(list) -> list:
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
        if isinstance(value, str) and (len(value) == 0 or not value.isnumeric()):
            return value
        if self.min_value is not None and float(value) < self.min_value:
            value = self.min_value
        elif self.max_value is not None and float(value) > self.max_value:
            value = self.max_value
        return value

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "default_value": self.default_value,
            "hidden": self.hidden,
            "parent": self.parent,
            "options": self.options,
            "type": str(self.value_type),
        }
