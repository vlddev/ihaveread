from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QListWidget, QListWidgetItem,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QTextEdit, QVBoxLayout, QWidget)
import sqlite3 as lite
import const
import sqlite_utils
import sys

def editAuthor(con, author):
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Add author")
    dialog.setMinimumSize(300, 250)
    layout = QtWidgets.QVBoxLayout()

    name_label = QtWidgets.QLabel("Name(s)")
    name_input = QtWidgets.QLineEdit()
    layout.addWidget(name_label)
    layout.addWidget(name_input)

    surname_label = QtWidgets.QLabel("Surname")
    surname_input = QtWidgets.QLineEdit()
    layout.addWidget(surname_label)
    layout.addWidget(surname_input)

    lang_label = QtWidgets.QLabel("Language")
    lang_input = QtWidgets.QLineEdit()
    layout.addWidget(lang_label)
    layout.addWidget(lang_input)

    note_label = QtWidgets.QLabel("Note")
    note_input = QtWidgets.QLineEdit()
    layout.addWidget(note_label)
    layout.addWidget(note_input)

    synonyms_list = QtWidgets.QListWidget()
    synonyms_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    layout.addWidget(synonyms_list)

    submit_button = QtWidgets.QPushButton("Submit")
    submit_button.clicked.connect(dialog.accept)
    cancel_button = QtWidgets.QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.reject)
    button_layout = QtWidgets.QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(submit_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    dialog.setLayout(layout)

    if dialog.exec() == QtWidgets.QDialog.Accepted:
        authNormName = surname_input.text().strip() + ", " + name_input.text().strip()
        authName = name_input.text().strip() + " " + surname_input.text().strip()
        try:
            authorId = sqlite_utils.insertAuthor(con, authNormName, lang_input.text().strip(), note_input.text().strip())
            sqlite_utils.insertAuthorNames(con, authorId, [authNormName, authName])
            con.commit()
        except Exception as e:
            print ("Error %s:" % e.args[0])
            con.rollback()
    dialog.close()


class IHaveRead(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.con = lite.connect(const.LIB_DB)
        self.clipboard = QApplication.clipboard()

        self.initUI()

    def initUI(self):

        self.setWindowTitle('I have read')

        # Search tab
        self.search_tab = QWidget()
        search_layout = QGridLayout()
        search_layout.addWidget(QLabel('Search for:'), 0, 0)
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input, 0, 1)

        search_btns_layout = QHBoxLayout()
        self.search_by_author_btn = QPushButton('Books by author')
        self.search_by_title_btn = QPushButton('By title')
        self.search_by_year_btn = QPushButton('By year')
        search_btns_layout.addWidget(self.search_by_author_btn)
        search_btns_layout.addWidget(self.search_by_title_btn)
        search_btns_layout.addWidget(self.search_by_year_btn)
        search_layout.addLayout(search_btns_layout, 1, 0, 1, 2)

        self.book_list = QTableWidget()
        self.book_list.setColumnCount(10)
        self.book_list.setHorizontalHeaderLabels(['id', 'read on', 'author', 'title', 'lang', 'published', 'medium', 'score', 'genre', 'note'])
        search_layout.addWidget(self.book_list, 2, 0, 1, 2)

        self.book_list_size = QLabel()
        search_layout.addWidget(self.book_list_size, 3, 0, 1, 2)

        search_layout.addWidget(QLabel(), 4, 0, 1, 2)  # spacer
        search_layout.addWidget(QPushButton('Add book'), 5, 0)
        search_layout.addWidget(QPushButton('Backup DB'), 5, 1)

        self.search_tab.setLayout(search_layout)

        # Author tab
        self.author_tab = QWidget()
        author_layout = QHBoxLayout()

        author_search_layout = QVBoxLayout()
        author_search_layout.addWidget(QLabel('Search for:'))
        self.author_search_input = QLineEdit()
        author_search_layout.addWidget(self.author_search_input)

        author_search_btns_layout = QHBoxLayout()
        self.find_author_btn = QPushButton('Find author')
        self.add_author_btn = QPushButton('Add author')
        author_search_btns_layout.addWidget(self.find_author_btn)
        author_search_btns_layout.addWidget(self.add_author_btn)
        author_search_layout.addLayout(author_search_btns_layout)

        self.author_list = QListWidget()
        author_search_layout.addWidget(self.author_list)

        author_layout.addLayout(author_search_layout)

        author_edit_layout = QVBoxLayout()
        author_edit_layout.addWidget(QLabel('Author name:'))
        self.author_name_input = QLineEdit()
        author_edit_layout.addWidget(self.author_name_input)
        author_edit_layout.addWidget(QLabel('Author lang:'))
        self.author_lang_input = QLineEdit()
        author_edit_layout.addWidget(self.author_lang_input)
        author_edit_layout.addWidget(QLabel('Author note:'))
        self.author_note_input = QLineEdit()
        author_edit_layout.addWidget(self.author_note_input)

        author_edit_btns_layout = QHBoxLayout()
        self.save_author_btn = QPushButton('Save author')
        self.delete_author_btn = QPushButton('Delete author')

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.con = lite.connect(const.LIB_DB)

        # Initialize UI elements
        self.search_book_edit = QtWidgets.QLineEdit()
        self.search_book_edit.setPlaceholderText("Search for a book...")
        self.search_book_edit.textChanged.connect(self.search_books)

        self.books_by_author_button = QtWidgets.QPushButton("Books by author")
        self.books_by_author_button.clicked.connect(self.books_by_author)
        self.by_title_button = QtWidgets.QPushButton("by title")
        self.by_title_button.clicked.connect(self.books_by_title)
        self.by_year_button = QtWidgets.QPushButton("by year")
        self.by_year_button.clicked.connect(self.books_by_year)

        self.book_list_table = QtWidgets.QTableWidget()
        self.book_list_table.setColumnCount(10)
        self.book_list_table.setHorizontalHeaderLabels(["id", "read on", "author", "title", "lang", "published", "medium", "score", "genre", "note"])
        self.book_list_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.book_list_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.book_list_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.book_list_table.customContextMenuRequested.connect(self.show_book_menu)

        self.book_list_size_label = QtWidgets.QLabel()

        self.add_book_button = QtWidgets.QPushButton("Add book")
        self.add_book_button.clicked.connect(self.add_book)
        self.backup_db_button = QtWidgets.QPushButton("Backup DB")
        self.backup_db_button.clicked.connect(self.backup_db)

        # Create layout
        search_layout = QtWidgets.QVBoxLayout()
        search_layout.addWidget(self.search_book_edit)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.books_by_author_button)
        button_layout.addWidget(self.by_title_button)
        button_layout.addWidget(self.by_year_button)

        search_layout.addLayout(button_layout)
        search_layout.addWidget(self.book_list_table)
        search_layout.addWidget(self.book_list_size_label)

        search_layout.addWidget(self.add_book_button)
        search_layout.addWidget(self.backup_db_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(search_layout)

        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle("I have read")
        self.resize(800, 600)

    def search_books(self):
        toFind = self.search_book_edit.text().strip()
        list = sqlite_utils.getReadedBooksByTitle(con, toFind)
        self.update_book_list(list)

    def books_by_author(self):
        toFind = self.search_book_edit.text().strip()
        list = sqlite_utils.getReadedBooksByAuthor(con, toFind)
        self.update_book_list(list)

    def books_by_title(self):
        toFind = self.search_book_edit.text().strip()
        list = sqlite_utils.getReadedBooksByTitle(con, toFind)
        self.update_book_list(list)

    def books_by_year(self):
        toFind = self.search_book_edit.text().strip()
        list = sqlite_utils.getReadedBooksByYear(con, toFind)
        self.update_book_list(list)

    def update_book_list(self, book_list):
        self.book_list_table.clearContents()
        self.book_list_table.setRowCount(len(book_list))
        for i, row in enumerate(book_list):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                self.book_list_table.setItem(i, j, item)
        self.book_list_size_label.setText(f"{len(book_list)} books")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()