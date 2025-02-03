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

        # Cursor file selection
        file_group = QGroupBox("Cursor File")
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_cursor)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Apply/Reset buttons
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
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cursor Image",
            "",
            "Images (*.png *.xpm *.jpg *.cur *.ani)"
        )
        if file_name:
            self.file_path.setText(file_name)

    def apply_cursor(self):
        cursor_path = self.file_path.text()
        if not cursor_path or not os.path.exists(cursor_path):
            showInfo("Please select a valid cursor file")
            return
        from . import custom_cursor
        custom_cursor.set_cursor(cursor_path)

    def reset_cursor(self):
        from . import custom_cursor
        custom_cursor.reset_cursor()
