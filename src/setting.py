class Setting:
    """A setting that can have any value."""

    def __init__(
        self,
        name: str,
        value: any,
        default_value=None,
        hidden: bool = False,
        parent: str = "",
        value_type: type = None,
        on_change: callable = None,
    ) -> None:
        self.name = name
        self._value = value
        self.default_value = default_value
        self.hidden = hidden
        self.parent = parent
        self.on_change = on_change
        if value_type is None:
            self.value_type = type(value)
        elif isinstance(value_type, str):
            self.value_type = Setting.determine_value_type(value_type)

    @property
    def value(self) -> any:
        return self._value

    @value.setter
    def value(self, value: any) -> None:
        self._set_value(value)
        if self.on_change is not None:
            self.on_change()

    def _set_value(self, value: any) -> None:
        if self.value_type:
            self._value = self.value_type(value)
            return
        self._value = value

    @staticmethod
    def determine_value_type(value_type: str) -> type:
        if "int" in value_type:
            return int
        elif "float" in value_type:
            return float
        elif "bool" in value_type:
            return bool
        return str

    def reset_default_value(self) -> None:
        self.set_value(self.default_value)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "default_value": self.default_value,
            "hidden": self.hidden,
            "parent": self.parent,
            "value_type": str(self.value_type),
        }


class OptionSetting(Setting):
    """A setting that can have a value from a list of options."""

    def __init__(
        self,
        name: str,
        value,
        default_value,
        options: list | list[str],
        hidden: bool = False,
        parent: str = "",
        value_type: type = None,
        on_change: callable = None,
    ) -> None:
        self.options = options
        super().__init__(
            name, value, default_value, hidden, parent, value_type, on_change
        )

    def _set_value(self, value: any) -> None:
        if str(value) in self.options:
            self._value = value
            return
        raise ValueError(
            f"Value '{value}' is not in the list of options: {self.options}"
        )

    @property
    def options(self) -> list[str]:
        return self._options

    @options.setter
    def options(self, options: list) -> None:
        # Ensure every value in the list is a string.
        self._options = OptionSetting.to_str_list(options)

    @staticmethod
    def to_str_list(input: list) -> list:
        """Converts a list of items to a list of strings"""
        return [str(item) for item in input]

    def set_value(self, value: any) -> None:
        if str(value) in self.options:
            self.value = value

    def to_dict(self) -> dict:
        setting_dict = super().to_dict()
        setting_dict["options"] = self.options
        return setting_dict


class RangeSetting(Setting):
    """A setting that can have a value between min and max."""

    def __init__(
        self,
        name: str,
        value: int | float,
        default_value: int | float,
        min_value: int | float,
        max_value: int | float,
        on_change: callable = None,
        hidden: bool = False,
        parent: str = None,
        value_type: type = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(
            name=name,
            value=value,
            default_value=default_value,
            hidden=hidden,
            parent=parent,
            value_type=value_type,
            on_change=on_change,
        )

    def _clamp(self, value) -> int | float:
        if value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        return value

    def _set_value(self, value: any) -> None:
        if self.value_type:
            value = self.value_type(value)
        self._value = self._clamp(value)

    def to_dict(self) -> dict:
        setting_dict = super().to_dict()
        setting_dict["min_value"] = self.min_value
        setting_dict["max_value"] = self.max_value
        return setting_dict
