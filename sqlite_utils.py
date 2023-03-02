import re
import sqlite3 as lite


def normalizeStr(str):
    norm = str.replace('_', ' ')
    norm = re.sub(r'\W+', ' ', norm)
    norm = " ".join(norm.split())
    return norm.upper()

def getAuthor(con, author):
    ret = None
    cur = con.cursor()
    cur.execute('SELECT a.id FROM author a WHERE a.name = ? COLLATE NOCASE', (author,))
    data = cur.fetchone()
    if data != None and len(data) > 0:
        ret = data[0]
    return ret

def findAuthor(con, author):
    cur = con.cursor()
    cur.execute("""SELECT distinct a.id, a.name, a.lang, a.note
            FROM author a, author_names an
            WHERE an.name like ? and a.id = an.author_id""", ('%{}%'.format(author),))
    data = cur.fetchall()
    return data

def getAuthorNames(con, authorId):
    cur = con.cursor()
    cur.execute("""SELECT name, lang, type
            FROM author_names
            WHERE author_id = ?""", (authorId,))
    data = cur.fetchall()
    return data

def insertAuthor(con, author, lang, note):
    cur = con.cursor()
    cur.execute('INSERT INTO author(name, lang, note) VALUES (?,?,?)', (author ,lang, note))
    ret = cur.lastrowid
    return ret

def updateAuthor(con, authorId, name, lang, note):
    cur = con.cursor()
    cur.execute("""UPDATE author 
        SET name = ?, lang = ?, note = ? 
        WHERE id = ?""", (name, lang, note, authorId))

def insertAuthorNames(con, authorId, names):
    cur = con.cursor()
    for name in names:
        cur.execute('INSERT INTO author_names(author_id, name) VALUES (?,?)', (authorId, name))

def updateAuthorName(con, authorId, name, new_name, lang, type):
    cur = con.cursor()
    cur.execute("""UPDATE author_names 
        SET name = ?, lang = ?, type = ? 
        WHERE author_id = ? and name = ?""", (new_name, lang, type, authorId, name))

def deleteAuthorName(con, authorId, name):
    cur = con.cursor()
    cur.execute("""DELETE FROM author_names 
        WHERE author_id = ? and name = ?""", (authorId, name))

def getReadedBooksByAuthor(con, author):
    cur = con.cursor()
    cur.execute("""SELECT distinct br.book_id, br.date_read, 
            (select group_concat(a.name, '; ') from author a, author_book ab where ab.book_id = b.id and ab.author_id = a.id) authors,
            ifnull((select bn.name from book_names bn where bn.book_id = b.id and bn.lang = br.lang_read), b.title) title,
            br.lang_read, b.publish_date, br.medium, br.score, b.genre, b.note
        FROM book_readed br, book b, author_book ab, author a 
        WHERE 
        br.book_id = b.id
        and br.book_id = ab.book_id
        and ab.author_id = a.id
        and a.name like ?
        order by br.date_read""", ('%{}%'.format(author),))
    return cur.fetchall()

def getReadedBooksByTitle(con, title):
    cur = con.cursor()
    cur.execute("""SELECT distinct br.book_id, br.date_read, 
            (select group_concat(a.name, '; ') from author a, author_book ab where ab.book_id = b.id and ab.author_id = a.id) authors,
            ifnull((select bn.name from book_names bn where bn.book_id = b.id and bn.lang = br.lang_read), b.title) title,
            br.lang_read, b.publish_date, br.medium, br.score, b.genre, b.note
        from book_readed br, book b, author_book ab, author a 
        where 
        br.book_id = b.id
        and br.book_id = ab.book_id
        and ab.author_id = a.id
        and b.id in (select distinct book_id from book_names where name like ?)
        order by br.date_read""", ('%{}%'.format(title),))
    return cur.fetchall()

def getReadedBooksByYear(con, year):
    cur = con.cursor()
    cur.execute("""SELECT distinct br.book_id, br.date_read, 
            (select group_concat(a.name, '; ') from author a, author_book ab where ab.book_id = b.id and ab.author_id = a.id) authors,
            ifnull((select bn.name from book_names bn where bn.book_id = b.id and bn.lang = br.lang_read), b.title) title,
            br.lang_read, b.publish_date, br.medium, br.score, b.genre, b.note
        from book_readed br, book b, author_book ab, author a 
        where 
        br.book_id = b.id
        and br.book_id = ab.book_id
        and ab.author_id = a.id
        and br.date_read like ?
        order by br.date_read""", ('{}%'.format(year),))
    return cur.fetchall()

def getBook(con, bookId):
    ret = None
    cur = con.cursor()
    cur.execute('SELECT b.id, b.title, b.publish_date, b.lang, b.genre, b.note FROM book b WHERE b.id = ?', (bookId,))
    data = cur.fetchone()
    if data != None and len(data) > 0:
        ret = data
    return ret

def getReadedBooks(con, bookId):
    ret = None
    cur = con.cursor()
    cur.execute('SELECT b.book_id, b.date_read, b.lang_read, b.medium, b.score, b.note, b.id FROM book_readed b WHERE b.book_id = ?', (bookId,))
    data = cur.fetchall()
    if data != None and len(data) > 0:
        ret = data
    return ret

def getBookAuthors(con, bookId):
    cur = con.cursor()
    cur.execute("""SELECT a.id, a.name
            FROM author a, author_book ab
            WHERE ab.author_id = a.id and ab.book_id = ?""", (bookId,))
    data = cur.fetchall()
    return data

def insertBook(con, title, lang, publish_date, genre, note):
    cur = con.cursor()
    cur.execute('INSERT INTO book(title, lang, publish_date, genre, note) VALUES (?,?,?,?,?)', (title ,lang, publish_date, genre, note))
    ret = cur.lastrowid
    return ret

def updateBook(con, bookId, title, lang, publish_date, genre, note):
    cur = con.cursor()
    cur.execute('UPDATE book SET title = ?, lang = ?, publish_date = ?, genre = ?, note = ? WHERE id = ?', 
        (title, lang, publish_date, genre, note, bookId))

def insertBook_err(con, title, lang, publish_date, genre, note):
    try:
        cur = con.cursor()
        cur.execute('INSERT INTO book(title, lang, publish_date, genre, note) VALUES (?,?,?,?,?)', (title ,lang, publish_date, genre, note))
        con.commit()
        ret = cur.lastrowid
        return ret
    except lite.Error as e:
        print ("Error %s:" % e.args[0])
        print("For {0}".format(title))
        con.rollback()

def getBookNames(con, authorId):
    cur = con.cursor()
    cur.execute("""SELECT name, lang, id
            FROM book_names
            WHERE book_id = ?""", (authorId,))
    data = cur.fetchall()
    return data

def insertBookNames(con, bookId, names):
    cur = con.cursor()
    for name in names:
        cur.execute('INSERT INTO book_names(book_id, name, lang) VALUES (?,?,?)', (bookId, name[0], name[1]))

def updateBookName(con, id, lang, newName):
    cur = con.cursor()
    cur.execute('UPDATE book_names SET lang = ?, name = ? WHERE id = ?', (lang, newName, id))

def deleteBookName(con, id):
    cur = con.cursor()
    cur.execute('DELETE FROM book_names WHERE id = ?', (id, ))

def insertBookReaded(con, bookId, lang_read, date_read, medium, score):
    cur = con.cursor()
    cur.execute('INSERT INTO book_readed(book_id, lang_read, date_read, medium, score) VALUES (?,?,?,?,?)',
        (bookId, lang_read, date_read, medium, score))

def updateBookReaded(con, id, lang_read, date_read, medium, score, note):
    cur = con.cursor()
    cur.execute('UPDATE book_readed SET lang_read = ?, date_read = ?, medium = ?, score = ?, note = ? WHERE id = ?', 
        (lang_read, date_read, medium, score, note, id))

def deleteBookReaded(con, id):
    cur = con.cursor()
    cur.execute('DELETE FROM book_readed WHERE id = ?', (id, ))

def insertBookAuthors(con, bookId, authorIds):
    cur = con.cursor()
    for authorId in authorIds:
        cur.execute('INSERT INTO author_book(author_id, book_id) VALUES (?,?)', (authorId, bookId))

def deleteBookAuthors(con, bookId):
    cur = con.cursor()
    cur.execute('DELETE FROM author_book WHERE book_id = ?', (bookId, ))
