try:
    from CTkToolTip import CTkToolTip
except ModuleNotFoundError:

    class CTkToolTip:
        def __init__(self, *args) -> None:
            pass


class ToolTip(CTkToolTip):
    """Tooltip that works with an always on top root window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show over all other windows to display even when the root window is topmost.
        if hasattr(self, "attributes"):
            self.attributes("-topmost", True)
