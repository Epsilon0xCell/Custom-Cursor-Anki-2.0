import os

from aqt import mw
from aqt.qt import *
from .cursor_dialog import CursorDialog

# I read the config once, here at the top, because Anki imports this
# package once when the add-on loads. That makes this dict a snapshot:
# if I edit config.json inside Anki, my change takes effect on the next
# start, not immediately, because nothing below ever re-reads the file.
config = mw.addonManager.getConfig(__name__) or {}

class CustomCursorManager:
    def __init__(self):
        self.dialog = None
        self.current_cursor = None
        self.setup_menu()
        # I gate the start-up apply on both settings together. auto_apply
        # on its own with an empty default_cursor means I have nothing to
        # apply, and calling set_cursor with an empty path would only
        # return False and hide a config that says nothing.
        if config.get("auto_apply") and config.get("default_cursor"):
            self.set_cursor(config["default_cursor"])

    def show_cursor_dialog(self):
        # I keep one dialog and reuse it. Building a fresh dialog on
        # every menu click would stack windows and throw away the path
        # already typed into the one the user was looking at.
        if not self.dialog:
            self.dialog = CursorDialog(mw)
        self.dialog.show()

    def setup_menu(self):
        action = QAction("Custom Cursor", mw)
        # I use "or" for the fallback on purpose, not a default value in
        # the get call. A config that holds an empty shortcut string
        # counts as missing for me, and I still want a working shortcut.
        action.setShortcut(config.get("shortcut") or "Ctrl+Shift+C")
        action.triggered.connect(self.show_cursor_dialog)
        mw.form.menuTools.addAction(action)

    def set_cursor(self, cursor_path):
        if not cursor_path or not os.path.exists(cursor_path):
            return False

        pixmap = QPixmap(cursor_path)
        # I refuse a file that exists but is not a loadable image. The
        # browse filter offers .cur and .ani, and QPixmap cannot decode
        # those on every platform, so existence is not proof. A null
        # pixmap would install an invisible cursor, which is worse than
        # no change, so I treat it the same way as a missing file.
        if pixmap.isNull():
            return False

        # Qt override cursors are a stack, and this is the invariant I
        # have to protect: each setOverrideCursor pushes, and each
        # restoreOverrideCursor pops exactly one. My reset_cursor pops
        # once. If I pushed a second cursor without popping the first,
        # one reset would still leave the older cursor active. So I
        # restore the previous cursor before pushing the new one, and
        # the stack depth stays at one no matter how often I apply.
        if self.current_cursor is not None:
            mw.app.restoreOverrideCursor()

        cursor = QCursor(pixmap)
        mw.app.setOverrideCursor(cursor)
        self.current_cursor = cursor
        return True

    def reset_cursor(self):
        # I only pop when I know I pushed. If I called
        # restoreOverrideCursor with nothing of mine on the stack, I
        # could pop a cursor some other add-on put there, so a reset
        # with nothing applied has to stay a no-op.
        if self.current_cursor:
            mw.app.restoreOverrideCursor()
            self.current_cursor = None

# I create the manager at import time because that is how Anki add-ons
# run: importing this package is the start-up, and there is no later
# entry point where I could do it instead. Everything above has to be
# defined before this line, and the menu and the start-up apply both
# happen as a side effect of Anki loading the add-on.
custom_cursor = CustomCursorManager()
