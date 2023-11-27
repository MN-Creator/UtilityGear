import customtkinter as ctk

try:
    import CTkToolTip
    from .tooltip import ToolTip
except ModuleNotFoundError:
    ToolTip = None


class Slider(ctk.CTkSlider):
    """Slider with a tooltip to show the current value."""

    def __init__(self, master: any, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        if ToolTip is None:
            return
        self._create_tooltip()
        self._setup_command()

    def _setup_command(self) -> None:
        self._user_command = None
        if self._command is None:
            self._command = self._on_slider_change
        self._user_command = self._command
        self._command = self._on_slider_change

    def _create_tooltip(self) -> None:
        value = f"{int(self.get())}"
        self._tooltip = ToolTip(self, message=value, delay=0.1)

    def _set_tooltip_message(self, value: float) -> None:
        if self._tooltip:
            self._tooltip.configure(message=f"{int(value)}")

    def _on_slider_change(self, event):
        self._set_tooltip_message(self.get())
        if self._user_command:
            self._user_command(self.get())

    def set(self, value: float) -> None:
        super().set(value)
        if hasattr(self, "_tooltip"):
            self._set_tooltip_message(value)
