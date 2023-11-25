from storage import Storage
from setting import Setting
from setting import OptionSetting
from setting import RangeSetting


class SettingsManager:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage
        self.settings = dict()
        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings from storage."""
        settings_dict = self._storage.read_object("settings")
        if settings_dict is not None:
            for key, value in settings_dict.items():
                self.settings[key] = self._load_setting_from_dict(value)

    @staticmethod
    def _load_setting_from_dict(setting_dict: dict) -> Setting:
        """Load a setting from a dictionary."""
        if setting_dict.get("options") is not None:
            return OptionSetting(**setting_dict)
        elif setting_dict.get("min_value") is not None:
            return RangeSetting(**setting_dict)
        return Setting(**setting_dict)

    def _save_settings(self) -> None:
        """Save settings to storage."""
        settings_dict = dict()
        for key, value in self.settings.items():
            settings_dict[key] = value.to_dict()
        self._storage.save_object("settings", settings_dict)

    def clear_settings(self) -> None:
        """Remove all settings."""
        self.settings = {}
        self._save_settings()

    def create(
        self, name: str, default_value, hidden=False, parent="", desc: str = ""
    ) -> Setting:
        """Create a setting with a default value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
            self.settings[name].description = desc
        except KeyError:
            self.settings[name] = Setting(
                name, default_value, default_value, hidden, parent, desc
            )
            self._save_settings()
        return self.settings[name]

    def create_range(
        self,
        name: str,
        default_value,
        min_value,
        max_value,
        hidden=False,
        parent="",
        desc: str = "",
    ) -> RangeSetting:
        """Create a setting that can have a value between min_value and max_value."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].min_value = min_value
            self.settings[name].max_value = max_value
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
            self.settings[name].description = desc
        except KeyError:
            self.settings[name] = RangeSetting(
                name,
                default_value,
                default_value,
                min_value,
                max_value,
                hidden=hidden,
                parent=parent,
                description=desc,
            )
            self._save_settings()
        return self.settings[name]

    def create_option(
        self,
        name: str,
        default_value,
        options: list,
        hidden: bool = False,
        parent: str = "",
        desc: str = "",
    ) -> OptionSetting:
        """Create a setting that can have a value from a list of options."""
        try:
            self.settings[name].default_value = default_value
            self.settings[name].options = options
            self.settings[name].hidden = hidden
            self.settings[name].parent = parent
            self.settings[name].description = desc
        except KeyError:
            self.settings[name] = OptionSetting(
                name,
                default_value,
                default_value,
                options=options,
                hidden=hidden,
                parent=parent,
                description=desc,
            )
        self._save_settings()
        return self.settings[name]

    def get(self, name: str, default_value=None) -> Setting:
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

    def set_value(self, name: str, value: any) -> None:
        """Set the value of a setting by name, create a new setting if not found."""
        try:
            self.settings[name].value = value
        except KeyError:
            self.settings[name] = Setting(name, value)
        finally:
            self._save_settings()
