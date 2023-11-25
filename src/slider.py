import customtkinter as ctk

try:
    import CTkToolTip
    from tooltip import ToolTip
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
        value = int(self.get())
        self._tooltip = ToolTip(self, message=f"{value}", delay=0.1)

    def _on_slider_change(self, event):
        self._tooltip.configure(message=f"{int(self.get())}")
        if self._user_command is not None:
            self._user_command(self.get())
