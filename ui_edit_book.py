from os import error
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import PopupOKCancel
import sqlite3 as lite
import datetime
import const
import sqlite_utils

def editBook(con, bookId):
    edit_book_layout = [
        [sg.Text('Author(s)'), sg.In(size=(60, 1), key=const.KEY_BOOK_AUTHORS)],
        [sg.Listbox(
            values=[], size=(60, 4),
            key="BookAuthorList",
        )],
        [sg.Text('Title', (12, 1)), sg.In(size=(60, 1), key=const.KEY_BOOK_TITLE)],
        [sg.Text('Orig title', (12, 1)), sg.In(size=(60, 1), key=const.KEY_ORIG_BOOK_TITLE)],
        [sg.Text('Orig lang', (12, 1)), sg.In(size=(10, 1), key=const.KEY_ORIG_BOOK_LANG)],
        [sg.Text('Publish date', (12, 1)), sg.In(size=(10, 1), key=const.KEY_BOOK_PUBL_DATE)],
        [sg.Text('Genre', (12, 1)), sg.In(size=(60, 1), key=const.KEY_BOOK_GENRE)],
        [sg.Text('Note', (12, 1)), sg.In(size=(60, 3), key=const.KEY_BOOK_NOTE)],
        [sg.Button("Change book")],
        [],
        [sg.Listbox(
            values=[], size=(60, 4),
            key="BookNamesList",
        )],
        [],
        [sg.Text('Read lang', (12, 1)), sg.In(size=(10, 1), key=const.KEY_BOOK_LANG)],
        [sg.Text('Read date', (12, 1)), sg.In(size=(10, 1), default_text=datetime.datetime.today().strftime('%Y-%m-%d'), key=const.KEY_BOOK_READ_DATE)],
        [sg.Text('Medium', (12, 1)), sg.In(size=(10, 1), key=const.KEY_BOOK_MEDIUM)],
        [sg.Text('Score', (12, 1)), sg.In(size=(10, 1), key=const.KEY_BOOK_SCORE)],
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
        if event == 'Check':
            # check data
            pass
        if event == 'Submit':
            bookTitle = values[const.KEY_BOOK_TITLE].strip()
            bookLang = values[const.KEY_BOOK_LANG].strip()
            bookNames = [[bookTitle, bookLang]]
            origBookTitle = values[const.KEY_ORIG_BOOK_TITLE].strip()
            origBookLang = values[const.KEY_ORIG_BOOK_LANG].strip()
            if len(origBookTitle) == 0:
                origBookTitle = bookTitle
                origBookLang = bookLang
            else:
                bookNames.append([origBookTitle, origBookLang])
            # TODO implement check insert possible
            try:
                bookId = sqlite_utils.insertBook(con, origBookTitle, origBookLang, values[const.KEY_BOOK_PUBL_DATE].strip(),
                            values[const.KEY_BOOK_GENRE].strip(), values[const.KEY_BOOK_NOTE].strip())
                sqlite_utils.insertBookNames(con, bookId, bookNames)
                sqlite_utils.insertBookReaded(con, bookId, bookLang, values[const.KEY_BOOK_READ_DATE].strip(),
                            values[const.KEY_BOOK_MEDIUM].strip(), values[const.KEY_BOOK_SCORE].strip())
                #  get authors
                bookAuthors = values[const.KEY_BOOK_AUTHORS]
                bookAuthorIds = []
                for author in bookAuthors.split(','):
                    data = sqlite_utils.findAuthor(con, author.strip())
                    if data != None and len(data) > 0:
                        for elem in data:
                            bookAuthorIds.append(elem[0])
                # store authors
                sqlite_utils.insertBookAuthors(con, bookId, bookAuthorIds)
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()
            break
    winEditBook.close()
