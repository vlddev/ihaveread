from os import error
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import PopupOKCancel
import sqlite3 as lite
import datetime
import const
import sqlite_utils
import ui_add_book


# see : https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Tabs.py
# https://pysimplegui.readthedocs.io/

def ifnull(var, val):
    if var is None:
        return val
    return var

def editAuthor(con, author):
    edit_author_layout = [
        [sg.Text('Name(s)'), sg.In(size=(60, 1), key=const.KEY_AUTHOR_NAME)],
        [sg.Text('Surname'), sg.In(size=(60, 1), key=const.KEY_AUTHOR_SURNAME)],
        [sg.Text('Language'), sg.In(size=(60, 1), key=const.KEY_AUTHOR_LANG)],
        [sg.Listbox(
            values=[], enable_events=True, size=(60, 10),
            key=const.KEY_AUTHOR_SYNONYMS,
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
            right_click_menu=['unused', ['Add', 'Delete', 'Edit']]
        )],
        [sg.Submit(), sg.Cancel()],
    ]
    winAddAuthor = sg.Window('Add author', edit_author_layout)
    event, values = winAddAuthor.read()
    if event == 'Submit':
        authNormName = values[const.KEY_AUTHOR_SURNAME].strip() + ", " + values[const.KEY_AUTHOR_NAME].strip()
        authName = values[const.KEY_AUTHOR_NAME].strip() + " " + values[const.KEY_AUTHOR_SURNAME].strip()
        try:
            authorId = sqlite_utils.insertAuthor(con, authNormName, values[const.KEY_AUTHOR_LANG].strip())
            sqlite_utils.insertAuthorNames(con, authorId, [authNormName, authName])
            con.commit()
        except Exception as e:
            print ("Error %s:" % e.args[0])
            con.rollback()
    winAddAuthor.close()

search_layout = [
    [
        sg.In(size=(60, 1), enable_events=True, key=const.KEY_SEARCH_BOOK),
        sg.Button("Books by author"),
        sg.Button("by title"),
        sg.Button("by year")
    ],
    [sg.Table(
        values=[], headings=["id", "read on", "author", "title", "lang", "published", "medium", "score", "genre", "note"],
        col_widths=[5,10,20,40,3,10,10,3,15,40],
        auto_size_columns=False,
        justification='left',
        num_rows=20,
        # max_col_width=160,
        key=const.KEY_BOOK_LIST
    )],
    [sg.Button("Add book")]
]

author_layout = [
    [
        sg.In(size=(60, 1), enable_events=True, key=const.KEY_SEARCH_AUTHOR),
        sg.Button("Find author"),
        sg.Button("Add author"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(50, 20),
            key=const.KEY_AUTHOR_LIST,
            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE),
        sg.Column(
            [[sg.Listbox(
                values=[], enable_events=True, size=(50, 10),
                key=const.KEY_AUTHOR_SYNONYMS,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
            [sg.Text('Name'), sg.In(size=(50, 1), key=const.KEY_AUTHOR_SYN_NAME)],
            [sg.Text('Lang'), sg.In(size=(50, 1), key=const.KEY_AUTHOR_SYN_LANG)],
            [sg.Text('Type'), sg.In(size=(50, 1), key=const.KEY_AUTHOR_SYN_TYPE)],
            [sg.Button("Save synonym"), sg.Button("Add synonym"), sg.Text('   '), sg.Button("Delete synonym")],
            ], vertical_alignment='top')
    ]
]


book_layout = []

app_layout = [[sg.TabGroup([[sg.Tab('Search', search_layout, key='-mykey-'),
                         sg.Tab('Author', author_layout),
                         sg.Tab('Book', book_layout),
                         ]], key='-group1-',  )
            ]]

window = sg.Window("I have read", app_layout)

con = lite.connect(const.LIB_DB)

# Run the Event Loop
while True:
    event, values = window.read()
    #print(event, values)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    #
    if event == "Books by author":
        toFind = values[const.KEY_SEARCH_BOOK]
        list = sqlite_utils.getReadedBooksByAuthor(con, toFind)
        window[const.KEY_BOOK_LIST].update(list)

    if event == "by title":
        toFind = values[const.KEY_SEARCH_BOOK]
        list = sqlite_utils.getReadedBooksByTitle(con, toFind)
        window[const.KEY_BOOK_LIST].update(list)

    if event == "by year":
        toFind = values[const.KEY_SEARCH_BOOK]
        list = sqlite_utils.getReadedBooksByYear(con, toFind)
        window[const.KEY_BOOK_LIST].update(list)

    if event == "Find author":
        toFind = values[const.KEY_SEARCH_AUTHOR]
        list = sqlite_utils.findAuthor(con, toFind)
        window[const.KEY_AUTHOR_LIST].update(list)

    if event == const.KEY_AUTHOR_LIST:
        authorId = values[const.KEY_AUTHOR_LIST][0][0]
        list = sqlite_utils.getAuthorNames(con, authorId)
        window[const.KEY_AUTHOR_SYNONYMS].update(list)

    if event == const.KEY_AUTHOR_SYNONYMS:
        authorId = values[const.KEY_AUTHOR_LIST][0][0]
        authorName = values[const.KEY_AUTHOR_SYNONYMS][0][0]
        authorLang = values[const.KEY_AUTHOR_SYNONYMS][0][1]
        authorType = values[const.KEY_AUTHOR_SYNONYMS][0][2]
        window[const.KEY_AUTHOR_SYN_NAME].update(authorName)
        window[const.KEY_AUTHOR_SYN_LANG].update(ifnull(authorLang, ''))
        window[const.KEY_AUTHOR_SYN_TYPE].update(ifnull(authorType, ''))
        updateAuthorSynPosible = True
        authorSynName = authorName

    if event == "Add author":
        editAuthor(con, 'author')

    if event == "Add book":
        ui_add_book.editBook(con, 'book')

    if event == "Add synonym":
        # get selected author
        authorId = values[const.KEY_AUTHOR_LIST][0][0]
        authorName = values[const.KEY_AUTHOR_SYN_NAME]
        authorLang = values[const.KEY_AUTHOR_SYN_LANG]
        authorType = values[const.KEY_AUTHOR_SYN_TYPE]
        # TODO store lang, type in DB
        try:
            sqlite_utils.insertAuthorNames(con, authorId, [authorName])
            con.commit()
        except Exception as e:
            print ("Error %s:" % e.args[0])
            con.rollback()
        list = sqlite_utils.getAuthorNames(con, authorId)
        window[const.KEY_AUTHOR_SYNONYMS].update(list)

    if event == "Save synonym":
        if updateAuthorSynPosible:
            try:
                sqlite_utils.updateAuthorName(con, authorId, authorSynName, values[const.KEY_AUTHOR_SYN_NAME].strip(),
                    values[const.KEY_AUTHOR_SYN_LANG].strip(), values[const.KEY_AUTHOR_SYN_TYPE].strip())
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()

    if event == "Delete synonym":
        if updateAuthorSynPosible:
            try:
                sqlite_utils.deleteAuthorName(con, authorId, authorSynName)
                con.commit()
            except Exception as e:
                print ("Error %s:" % e.args[0])
                con.rollback()

window.close()
if con:
    con.close()

