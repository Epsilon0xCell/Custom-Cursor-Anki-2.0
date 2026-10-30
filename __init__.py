import os

from aqt import mw
from aqt.qt import *
from .cursor_dialog import CursorDialog

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

        cursor = QCursor(QPixmap(cursor_path))
        mw.app.setOverrideCursor(cursor)
        self.current_cursor = cursor
        return True

    def reset_cursor(self):
        if self.current_cursor:
            mw.app.restoreOverrideCursor()
            self.current_cursor = None

custom_cursor = CustomCursorManager()
