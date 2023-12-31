import customtkinter as ctk


class TabView(ctk.CTkTabview):
    """Tab view with key bindings."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = []
        self._current_tab_index = 0
        self._current_tab = None
        self._command = self._on_tab_changed

    def add(self, name: str) -> ctk.CTkFrame:
        """Add a tab."""
        self._tabs.append(name)
        return super().add(name)

    def bind_keys(self, modifier_key="Control"):
        """Bind keys to change tab."""
        self._current_tab = self.get()
        for i, _ in enumerate(self._tabs):
            self.master.bind(
                f"<{modifier_key}-Key-{i + 1}>",
                lambda event, index=i: self._change_tab(index),
            )

    def _on_tab_changed(self):
        """Called when the tab is changed by the segmented button."""
        self._current_tab = self.get()
        self._current_tab_index = self.index(self._current_tab)

    def _change_tab(self, index: int):
        """Change to tab at index."""
        self.set(self._tabs[index])
        self._current_tab = self.get()
        self._current_tab_index = self.index(self._current_tab)
