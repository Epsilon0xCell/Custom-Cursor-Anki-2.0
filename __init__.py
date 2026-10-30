import os

from aqt import mw
from aqt.qt import *
from .cursor_dialog import CursorDialog

# The config is read once, here, because Anki imports this package once
# when the add-on loads. Editing config.json inside Anki therefore takes
# effect on the next start, not immediately; nothing below re-reads it.
config = mw.addonManager.getConfig(__name__) or {}

class CustomCursorManager:
    def __init__(self):
        self.dialog = None
        self.current_cursor = None
        self.setup_menu()
        if config.get("auto_apply") and config.get("default_cursor"):
            self.set_cursor(config["default_cursor"])

    def show_cursor_dialog(self):
        if not self.dialog:
            self.dialog = CursorDialog(mw)
        self.dialog.show()

    def setup_menu(self):
        action = QAction("Custom Cursor", mw)
        action.setShortcut(config.get("shortcut") or "Ctrl+Shift+C")
        action.triggered.connect(self.show_cursor_dialog)
        mw.form.menuTools.addAction(action)

    def set_cursor(self, cursor_path):
        if not cursor_path or not os.path.exists(cursor_path):
            return False

        pixmap = QPixmap(cursor_path)
        # A file can exist and still not be a loadable image (the browse
        # filter offers .cur and .ani, which QPixmap cannot decode on
        # every platform). A null pixmap would install an invisible
        # cursor, so refuse it the same way as a missing file.
        if pixmap.isNull():
            return False

        # Qt override cursors are a stack: each setOverrideCursor pushes
        # and each restoreOverrideCursor pops exactly one. reset_cursor
        # pops once, so applying a second cursor without popping the
        # first would leave the older one active after a reset. Keep the
        # stack depth at one by restoring the previous cursor first.
        if self.current_cursor is not None:
            mw.app.restoreOverrideCursor()

        cursor = QCursor(pixmap)
        mw.app.setOverrideCursor(cursor)
        self.current_cursor = cursor
        return True

    def reset_cursor(self):
        if self.current_cursor:
            mw.app.restoreOverrideCursor()
            self.current_cursor = None

custom_cursor = CustomCursorManager()
