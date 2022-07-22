from os import error
from telnetlib import NOP
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
    readedBookId = readedBooks[0][6]
    authors = sqlite_utils.getBookAuthors(con, bookId)
    bookNames = sqlite_utils.getBookNames(con, bookId)

    edit_book_layout = [
        [sg.Text('Author(s)'), sg.In(size=(60, 1), key=const.KEY_BOOK_AUTHORS)],
        [sg.Listbox(
            values=authors, size=(60, 4),
            key="BookAuthorList",
            right_click_menu=['unused', ['Delete author']]),
            sg.Button("Add author(s)", key="Add author")],
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
            enable_events=True,
            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE
        )],
        [sg.Text('Title', (8, 1)), sg.In(size=(60, 1), default_text=bookNames[0][0] , key=const.KEY_ALT_BOOK_TITLE)],
        [sg.Text('Lang', (8, 1)), sg.In(size=(3, 1), default_text=bookNames[0][1] , key=const.KEY_ALT_BOOK_LANG)],
        [sg.Button("Add name"), sg.Button("Save name"), sg.Button("Delete name")],
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
        [sg.Text('Note', (12, 1)), sg.In(size=(50, 1), default_text=readedBooks[0][5], key=const.KEY_READ_BOOK_NOTE)],
        [sg.Listbox(
            values=[], size=(60, 4),
            key="ErrorList",
        )],
        [sg.Button("Change read book")],
        [sg.CloseButton("Close")],
    ]
    winEditBook = sg.Window('Edit book', edit_book_layout)

    # Run the Event Loop
    while True:
        event, values = winEditBook.read()
        if event == 'Cancel' or event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Add author':
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
                sqlite_utils.updateBook(con, bookId, values[const.KEY_BOOK_TITLE].strip(), newLang,
                    values[const.KEY_BOOK_PUBL_DATE].strip(), values[const.KEY_BOOK_GENRE].strip(), values[const.KEY_BOOK_NOTE].strip() )
                if len(newLang) > 0:
                    sqlite_utils.updateBookName(con, bookId, newLang, newName)
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
                sqlite_utils.updateBookReaded(con, readedBookId, values[const.KEY_READ_BOOK_LANG].strip(), values[const.KEY_BOOK_READ_DATE].strip(),
                    values[const.KEY_BOOK_MEDIUM].strip(), values[const.KEY_BOOK_SCORE].strip(), values[const.KEY_READ_BOOK_NOTE].strip() )
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()
        if event == "ReadedBooksList":
            # get data of selected book
            winEditBook[const.KEY_BOOK_READ_DATE].update(values["ReadedBooksList"][0][1].strip())
            winEditBook[const.KEY_READ_BOOK_LANG].update(values["ReadedBooksList"][0][2].strip())
            winEditBook[const.KEY_BOOK_MEDIUM].update(const.ifnull(values["ReadedBooksList"][0][3], "").strip())
            winEditBook[const.KEY_BOOK_SCORE].update(values["ReadedBooksList"][0][4])
            winEditBook[const.KEY_READ_BOOK_NOTE].update(values["ReadedBooksList"][0][5])
            readedBookId = values["ReadedBooksList"][0][6]

        if event == "Delete author":
            if len(values["BookAuthorList"]) > 0:
                bookAuthors = winEditBook["BookAuthorList"].get_list_values()
                selAuthors = winEditBook["BookAuthorList"].get_indexes()
                for ind in selAuthors:
                    del bookAuthors[ind]
                winEditBook["BookAuthorList"].update(bookAuthors)

        if event == 'BookNamesList':
            # get data of selected name
            winEditBook[const.KEY_ALT_BOOK_TITLE].update(values["BookNamesList"][0][0].strip())
            winEditBook[const.KEY_ALT_BOOK_LANG].update(values["BookNamesList"][0][1].strip())

        if event == "Add name":
            lang = values[const.KEY_ALT_BOOK_LANG].strip()
            title = values[const.KEY_ALT_BOOK_TITLE].strip()
            if (len(lang) > 0 and len(title) > 0):
                try:
                    sqlite_utils.insertBookNames(con, bookId, [[title, lang], ])
                    bookNames = sqlite_utils.getBookNames(con, bookId)
                    winEditBook["BookNamesList"].update(bookNames)
                    con.commit()
                except Exception as e:
                    print ("Error %s:" % e.args[0])
                    con.rollback()

        if event == "Save name":
            lang = values[const.KEY_ALT_BOOK_LANG].strip()
            title = values[const.KEY_ALT_BOOK_TITLE].strip()
            if (len(lang) > 0 and len(title) > 0):
                try:
                    sqlite_utils.updateBookName(con, bookId, lang, title)
                    bookNames = sqlite_utils.getBookNames(con, bookId)
                    winEditBook["BookNamesList"].update(bookNames)
                    con.commit()
                except Exception as e:
                    print ("Error %s:" % e.args[0])
                    con.rollback()

        if event == "Delete name":
            lang = values[const.KEY_ALT_BOOK_LANG].strip()
            if (len(lang) > 0):
                try:
                    sqlite_utils.deleteBookName(con, bookId, lang)
                    bookNames = sqlite_utils.getBookNames(con, bookId)
                    winEditBook["BookNamesList"].update(bookNames)
                except Exception as e:
                    print ("Error %s:" % e.args[0])
                    con.rollback()


    winEditBook.close()
