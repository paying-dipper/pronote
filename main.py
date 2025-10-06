import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QTextEdit, QPushButton, QLineEdit, QFileDialog,
                             QAction, QMessageBox, QInputDialog, QToolBar, QLabel, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor

APP_NAME = "pronote"
NOTES_DIR = os.path.expanduser(f"~/.{APP_NAME}_notes")
SETTINGS_FILE = os.path.join(NOTES_DIR, "settings.json")

def ensure_notes_dir():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

def list_notes():
    ensure_notes_dir()
    return [f[:-5] for f in os.listdir(NOTES_DIR) if f.endswith('.json') and f != "settings.json"]

def load_note(note_name):
    with open(os.path.join(NOTES_DIR, note_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_note(note_name, content, tags):
    with open(os.path.join(NOTES_DIR, note_name + '.json'), 'w', encoding='utf-8') as f:
        json.dump({'content': content, 'tags': tags}, f)

def delete_note(note_name):
    os.remove(os.path.join(NOTES_DIR, note_name + '.json'))

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

class ProNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pronote - Pro Note Taking App")
        self.setGeometry(200, 100, 900, 600)
        self.notes = []
        self.current_note = None
        self.settings = load_settings()
        self.init_ui()
        self.refresh_notes()
        self.apply_theme(dark=self.settings.get('dark_mode', False))

    def init_ui(self):
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout()
        central.setLayout(layout)

        # Note List
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.on_note_selected)
        layout.addWidget(self.note_list, 2)

        # Editor and controls
        vbox = QVBoxLayout()
        layout.addLayout(vbox, 8)

        # Title and tags
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Note title")
        vbox.addWidget(self.title_edit)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Tags (comma separated)")
        vbox.addWidget(self.tags_edit)

        # Rich Text Editor
        self.editor = QTextEdit()
        vbox.addWidget(self.editor, 1)

        # Toolbar
        toolbar = QHBoxLayout()
        vbox.addLayout(toolbar)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_current_note)
        toolbar.addWidget(save_btn)

        new_btn = QPushButton("New Note")
        new_btn.clicked.connect(self.new_note)
        toolbar.addWidget(new_btn)

        del_btn = QPushButton("Delete Note")
        del_btn.clicked.connect(self.delete_current_note)
        toolbar.addWidget(del_btn)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_note)
        toolbar.addWidget(export_btn)

        # Search bar
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search notes...")
        self.search_edit.textChanged.connect(self.search_notes)
        toolbar.addWidget(self.search_edit)

        # Menu
        menubar = self.menuBar()
        
        view_menu = menubar.addMenu("View")
        self.dark_mode_action = QAction("Dark Mode", self, checkable=True)
        self.dark_mode_action.setChecked(self.settings.get('dark_mode', False))
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)

        # Status Bar
        self.statusBar().showMessage("Welcome to pronote!")

    def refresh_notes(self):
        self.notes = list_notes()
        self.note_list.clear()
        for note in self.notes:
            self.note_list.addItem(note)

    def on_note_selected(self, item):
        note_name = item.text()
        data = load_note(note_name)
        self.current_note = note_name
        self.title_edit.setText(note_name)
        self.editor.setHtml(data.get('content', ''))
        self.tags_edit.setText(', '.join(data.get('tags', [])))
        self.statusBar().showMessage(f"Loaded note: {note_name}")

    def save_current_note(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "Note title cannot be empty.")
            return
        content = self.editor.toHtml()
        tags = [t.strip() for t in self.tags_edit.text().split(',') if t.strip()]
        save_note(title, content, tags)
        self.refresh_notes()
        self.current_note = title
        self.statusBar().showMessage(f"Saved note: {title}")

    def new_note(self):
        self.current_note = None
        self.title_edit.clear()
        self.editor.clear()
        self.tags_edit.clear()
        self.statusBar().showMessage("New note.")

    def delete_current_note(self):
        if not self.current_note:
            QMessageBox.warning(self, "Error", "No note selected to delete.")
            return
        reply = QMessageBox.question(self, "Delete Note?", f"Delete note '{self.current_note}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_note(self.current_note)
            self.new_note()
            self.refresh_notes()
            self.statusBar().showMessage("Note deleted.")

    def export_note(self):
        if not self.current_note:
            QMessageBox.warning(self, "Error", "No note selected to export.")
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Export Note", f"{self.current_note}.html",
                                                  "HTML files (*.html);;PDF files (*.pdf)")
        if filename:
            content = self.editor.toHtml()
            if filename.endswith('.html'):
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif filename.endswith('.pdf'):
                try:
                    from PyQt5.QtPrintSupport import QPrinter
                    printer = QPrinter()
                    printer.setOutputFormat(QPrinter.PdfFormat)
                    printer.setOutputFileName(filename)
                    self.editor.document().print_(printer)
                except Exception as e:
                    QMessageBox.warning(self, "Export Failed", f"PDF export requires PyQt5.QtPrintSupport: {e}")
                    return
            self.statusBar().showMessage(f"Exported note to {filename}")

    def search_notes(self, text):
        text = text.lower()
        self.note_list.clear()
        for note in self.notes:
            data = load_note(note)
            tags = ', '.join(data.get('tags', []))
            if text in note.lower() or text in data.get('content', '').lower() or text in tags.lower():
                self.note_list.addItem(note)

    def toggle_dark_mode(self):
        dark = self.dark_mode_action.isChecked()
        self.apply_theme(dark)
        self.settings['dark_mode'] = dark
        save_settings(self.settings)

    def apply_theme(self, dark=False):
        if dark:
            self.setStyleSheet("""
                QMainWindow { background: #232629; color: #f0f0f0; }
                QTextEdit, QListWidget, QLineEdit { background: #31363b; color: #f0f0f0; }
                QPushButton { background: #31363b; color: #f0f0f0; }
                QMenuBar, QMenu { background: #232629; color: #f0f0f0; }
            """)
        else:
            self.setStyleSheet("")

def main():
    ensure_notes_dir()
    app = QApplication(sys.argv)
    win = ProNote()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
