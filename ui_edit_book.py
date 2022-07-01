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
    readedBooks = sqlite_utils.getReadedBooks(con, bookId)
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
        [sg.Text('Note', (12, 1)), sg.Multiline(size=(60, 3), default_text=book[5], key=const.KEY_BOOK_NOTE)],
        [sg.Button("Change book")],
        [],
        [sg.Listbox(
            values=bookNames, size=(60, 4),
            key="BookNamesList",
        )],
        [sg.Button("Add name"), sg.Button("Edit name"), sg.Button("Delete name")],
        [],
        [sg.Listbox(
            values=readedBooks, size=(60, 4),
            key="ReadedBooksList",
            enable_events=True,
            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE
        )],
        [sg.Text('Read lang', (12, 1)), sg.In(size=(10, 1), default_text=readedBooks[0][2], key=const.KEY_READ_BOOK_LANG)],
        [sg.Text('Read date', (12, 1)), sg.In(size=(10, 1), default_text=readedBooks[0][1], key=const.KEY_BOOK_READ_DATE)],
        [sg.Text('Medium', (12, 1)), sg.In(size=(10, 1), default_text=readedBooks[0][3], key=const.KEY_BOOK_MEDIUM)],
        [sg.Text('Score', (12, 1)), sg.In(size=(10, 1), default_text=readedBooks[0][4], key=const.KEY_BOOK_SCORE)],
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
            bookAuthorIds = winEditBook["BookAuthorList"].get_list_values()
            bookAuthors = values[const.KEY_BOOK_AUTHORS]
            for author in bookAuthors.split(','):
                data = sqlite_utils.findAuthor(con, author.strip())
                if data != None and len(data) > 0:
                    for elem in data:
                        if elem not in bookAuthorIds:
                            bookAuthorIds.append(elem)
            winEditBook["BookAuthorList"].update(bookAuthorIds)
        if event == 'Change book':
            try:
                bookNameList = list(zip(*bookNames))[0]
                langList = list(zip(*bookNames))[1]
                newName = values[const.KEY_BOOK_TITLE].strip()
                newLang = values[const.KEY_BOOK_LANG].strip()
                if newName not in bookNameList and newLang not in langList:
                    sqlite_utils.insertBookNames(con, bookId, [[newName, newLang],])
                sqlite_utils.updateBook(con, bookId, values[const.KEY_BOOK_TITLE].strip(), values[const.KEY_BOOK_LANG].strip(),
                    values[const.KEY_BOOK_PUBL_DATE].strip(), values[const.KEY_BOOK_GENRE].strip(), values[const.KEY_BOOK_NOTE].strip() )
                bookAuthors = winEditBook["BookAuthorList"].get_list_values()
                bookAuthorIds = []
                for author in bookAuthors:
                    bookAuthorIds.append(author[0])
                sqlite_utils.deleteBookAuthors(con, bookId)
                sqlite_utils.insertBookAuthors(con, bookId, bookAuthorIds)
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()
        if event == 'Change read book':
            try:
                sqlite_utils.updateBookReaded(con, bookId, values[const.KEY_READ_BOOK_LANG].strip(), values[const.KEY_BOOK_READ_DATE].strip(),
                    values[const.KEY_BOOK_MEDIUM].strip(), values[const.KEY_BOOK_SCORE].strip() )
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()
        if event == "ReadedBooksList":
            # get data of selected book
            winEditBook[const.KEY_BOOK_READ_DATE].update(values["ReadedBooksList"][0][1].strip())
            winEditBook[const.KEY_READ_BOOK_LANG].update(values["ReadedBooksList"][0][2].strip())
            winEditBook[const.KEY_BOOK_MEDIUM].update(values["ReadedBooksList"][0][3].strip())
            winEditBook[const.KEY_BOOK_SCORE].update(values["ReadedBooksList"][0][4])


    winEditBook.close()
