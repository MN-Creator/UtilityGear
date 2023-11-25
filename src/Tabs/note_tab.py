import customtkinter as ctk
from .tab import Tab
from textbox import Textbox


class NoteTab(Tab):
    def create_content(self) -> None:
        self._notes = dict()
        self._auto_save_after_id = None
        self._font = "TkDefaultFont"
        self._create_settings()
        self._create_textbox()
        self._load_notes()
        self._set_saving_behaviour()
        self.tab.bind("<Destroy>", lambda _: self._save_on_destroy())

    def _create_textbox(self) -> None:
        """Create the notepad."""
        font = (self._font, self.font_size_setting.value)
        self.text = Textbox(self.tab, font=font)
        self.text.pack(fill=ctk.BOTH, expand=True)

    def _create_settings(self) -> None:
        self._create_auto_save_setting()
        self._create_font_size_setting()

    def _create_font_size_setting(self):
        DESC = "Set the font size of the notepad."
        size_options = [12, 14, 16, 18, 20]
        self.font_size_setting = self.app.settings.create_option(
            "notepad_font_size",
            size_options[0],
            options=size_options,
            parent="Notepad",
            desc=DESC,
        )
        self.font_size_setting.on_change = self._set_font_size

    def _set_font_size(self) -> None:
        font_size = self.font_size_setting.value
        self.text.configure(font=(self._font, font_size))

    def _create_auto_save_setting(self) -> None:
        """Create a boolean setting to enable/disable auto save."""
        DESC = "Automatically save when typing. The notepad will not save if option is disabled."
        self.auto_save_setting = self.app.settings.create(
            "notepad_autosave", True, parent="Notepad", desc=DESC
        )
        self.auto_save_setting.on_change = self._set_saving_behaviour

    def _set_saving_behaviour(self) -> None:
        if self.auto_save_setting.value:
            # Save the note when the user stops typing
            self.text.on_key_released(lambda _: self._auto_save())
            self._auto_save()
            return
        self.text.unbind("<KeyRelease>", None)

    def _auto_save(self) -> None:
        """Save the note after a short delay."""
        if self._auto_save_after_id is not None:
            self.app.after_cancel(self._auto_save_after_id)
        self._auto_save_after_id = self.app.after(500, self._save_note)

    def _save_on_destroy(self) -> None:
        """Save note when user exits the app."""
        if self.auto_save_setting.value and self._auto_save_after_id is not None:
            self._save_note()

    def _load_notes(self) -> None:
        notes = self.app.storage.read_object("notepad")
        if notes is not None:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", notes["default"])

    def _save_note(self) -> None:
        self._notes["default"] = self.text.get("1.0", "end-1c")
        self.app.storage.save_object("notepad", self._notes)
