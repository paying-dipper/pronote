# pronote

**pronote** is a professional, feature-rich note-taking app built with PyQt5. It offers powerful tools for organizing and editing notes, making it the perfect choice for students, professionals, and anyone who wants to take their note-taking to the next level.

---

## Features

- **Multi-note management**: Create, rename, delete, and organize unlimited notes.
- **Rich text editing**: Use bold, italics, underline, lists, and more (powered by a WYSIWYG editor).
- **Tagging and categorization**: Assign tags to notes for easy searching and grouping.
- **Fast search**: Search notes by title, content, or tags in real-time.
- **Light/Dark mode**: Toggle between beautiful light and dark themes for comfortable reading.
- **Export**: Export notes as HTML or PDF for sharing or backup.
- **Auto-save**: Your notes are saved as you edit.
- **Local privacy**: Notes are stored locally on your computer.
- **Easy to use**: Clean, modern, intuitive interface.

---

## Screenshots

> *You can add your screenshots here!*

---

## Getting Started

### Requirements

- **Python 3.7+**
- **PyQt5**

### Install dependencies

```bash
pip install PyQt5
```

### Run pronote

```bash
python main.py
```

---

## Usage

- **Create a new note:** Click "New Note", enter a title, tags (comma separated), and edit your note.
- **Save a note:** Click "Save". Notes are saved automatically in your home directory under `~/.pronote_notes/`.
- **Search notes:** Use the search bar to filter notes by title, content, or tags.
- **Toggle dark mode:** Use the "View" menu to switch between light and dark themes.
- **Export notes:** Click "Export" to save a note as HTML or PDF.
- **Delete notes:** Select a note and click "Delete Note".

---

## File Storage

All notes and settings are stored locally in `~/.pronote_notes/`. Each note is a separate `.json` file for easy backup and migration.

---

## Roadmap / Pro Features To Come

- Password protection for sensitive notes
- Cloud sync (Google Drive, Dropbox, etc.)
- Attachments (images, files)
- Markdown support
- Note organization (folders, drag-and-drop)
- More export formats
- Mobile/desktop cross-platform support

---

## Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Author

Made with ❤️ using PyQt5.
