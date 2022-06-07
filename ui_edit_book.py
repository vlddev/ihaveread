from os import error
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import PopupOKCancel
import sqlite3 as lite
import datetime
import const
import sqlite_utils

def editBook(con, bookId):
    #  populate fields
    book = sqlite_utils.getBook(con, bookId)
    readedBook = sqlite_utils.getReadedBook(con, bookId)
    authors = sqlite_utils.getBookAuthors(con, bookId)
    bookNames = sqlite_utils.getBookNames(con, bookId)

    edit_book_layout = [
        [sg.Text('Author(s)'), sg.In(size=(60, 1), key=const.KEY_BOOK_AUTHORS)],
        [sg.Listbox(
            values=authors, size=(60, 4),
            key="BookAuthorList",
        )],
        [sg.Text('Title', (12, 1)), sg.In(size=(60, 1), default_text=book[1] , key=const.KEY_BOOK_TITLE)],
        [sg.Text('Lang', (12, 1)), sg.In(size=(10, 1), default_text=book[3], key=const.KEY_BOOK_LANG)],
        [sg.Text('Publish date', (12, 1)), sg.In(size=(10, 1), default_text=book[2], key=const.KEY_BOOK_PUBL_DATE)],
        [sg.Text('Genre', (12, 1)), sg.In(size=(60, 1), default_text=book[4], key=const.KEY_BOOK_GENRE)],
        [sg.Text('Note', (12, 1)), sg.In(size=(60, 3), default_text=book[5], key=const.KEY_BOOK_NOTE)],
        [sg.Button("Change book")],
        [],
        [sg.Listbox(
            values=bookNames, size=(60, 4),
            key="BookNamesList",
        )],
        [sg.Button("Add name"), sg.Button("Edit name"), sg.Button("Delete name")],
        [],
        [sg.Text('Read lang', (12, 1)), sg.In(size=(10, 1), default_text=readedBook[2], key=const.KEY_READ_BOOK_LANG)],
        [sg.Text('Read date', (12, 1)), sg.In(size=(10, 1), default_text=readedBook[1], key=const.KEY_BOOK_READ_DATE)],
        [sg.Text('Medium', (12, 1)), sg.In(size=(10, 1), default_text=readedBook[3], key=const.KEY_BOOK_MEDIUM)],
        [sg.Text('Score', (12, 1)), sg.In(size=(10, 1), default_text=readedBook[4], key=const.KEY_BOOK_SCORE)],
        [sg.Listbox(
            values=[], size=(60, 4),
            key="ErrorList",
        )],
        [sg.Button("Change read book")],
        [sg.CloseButton("Close"), sg.Button("Check")],
    ]
    winEditBook = sg.Window('Edit book', edit_book_layout)

    # Run the Event Loop
    while True:
        event, values = winEditBook.read()
        if event == 'Cancel' or event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Change book':
            pass
        if event == 'Change read book':
            pass

    winEditBook.close()
