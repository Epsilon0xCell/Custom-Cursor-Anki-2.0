from aqt.qt import *
from aqt.utils import showInfo
import os

class CursorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Custom Cursor Settings")
        layout = QVBoxLayout()

        file_group = QGroupBox("Cursor File")
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_cursor)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply Cursor")
        apply_btn.clicked.connect(self.apply_cursor)
        reset_btn = QPushButton("Reset Cursor")
        reset_btn.clicked.connect(self.reset_cursor)
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(reset_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def browse_cursor(self):
        # My filter is wider than what QPixmap can always decode: it
        # offers .cur and .ani as well as png, xpm, and jpg. I keep the
        # wide filter because those formats do load on some platforms,
        # and I let apply_cursor report the ones that do not load here
        # instead of hiding the files from the picker entirely.
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cursor Image",
            "",
            "Images (*.png *.xpm *.jpg *.cur *.ani)"
        )
        # I only touch the field when a file was actually picked.
        # Cancelling the picker leaves whatever path was already typed
        # or chosen in place, instead of wiping it to empty.
        if file_name:
            self.file_path.setText(file_name)

    def apply_cursor(self):
        cursor_path = self.file_path.text()
        # I check the path here even though set_cursor checks it again,
        # because from here I can tell the user which problem I found.
        # set_cursor only returns True or False, so without this first
        # check a missing file and a file Qt cannot load would get the
        # same message, and only one of those is fixed by picking again.
        if not cursor_path or not os.path.exists(cursor_path):
            showInfo("Please select a valid cursor file")
            return
        if not self._manager().set_cursor(cursor_path):
            showInfo("That file could not be loaded as a cursor image")

    def reset_cursor(self):
        self._manager().reset_cursor()
        # I clear the field as part of the reset, not as decoration.
        # If the path stayed, the dialog would still show the cursor I
        # just removed as if it were current, and one stray click on
        # Apply would put it straight back.
        self.file_path.setText("")

    @staticmethod
    def _manager():
        # I import here, not at the top of this module, because this
        # module is itself imported by the package __init__ while the
        # manager is still being created. A top-level import of
        # custom_cursor from here would be circular and could bind a
        # half-built package. By the time a button is pressed and this
        # runs, the package has finished loading, so the import is safe.
        from . import custom_cursor
        return custom_cursor
