from aqt import mw
from aqt.qt import *
from .cursor_dialog import CursorDialog

config = mw.addonManager.getConfig(__name__)

class CustomCursorManager:
    def __init__(self):
        self.dialog = None
        self.current_cursor = None
        self.setup_menu()

    def show_cursor_dialog(self):
        if not self.dialog:
            self.dialog = CursorDialog(mw)
        self.dialog.show()

    def setup_menu(self):
        action = QAction("Custom Cursor", mw)
        action.setShortcut("Ctrl+Shift+C")
        action.triggered.connect(self.show_cursor_dialog)
        mw.form.menuTools.addAction(action)

    def set_cursor(self, cursor_path):
        if not cursor_path:
            return
        
        cursor = QCursor(QPixmap(cursor_path))
        mw.app.setOverrideCursor(cursor)
        self.current_cursor = cursor

    def reset_cursor(self):
        if self.current_cursor:
            mw.app.restoreOverrideCursor()
            self.current_cursor = None

custom_cursor = CustomCursorManager()
