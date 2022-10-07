

class Author:
    def __init__(self, dataDict):
        # TODO fill from data, data is a map or named params???
        self.id = dataDict["id"]
        self.name = dataDict["name"]

    def __str__(self):
        return '{} {}'.format(self.id, self.name)


class AuthorName:
    def __init__(self, dataDict):
        self.id = dataDict["id"]
        self.author_id = dataDict["author_id"]
        self.name = dataDict["name"]
        self.lang = dataDict["lang"]
        self.type = dataDict["type"]

class Book:
    def __init__(self, dataDict):
        self.id = dataDict["id"]
        self.title = dataDict["title"]
        self.genre = dataDict["genre"]
        self.note = dataDict["note"]
        self.lang = dataDict["lang"]
        self.publish_date = dataDict["publish_date"]

class BookName:
    def __init__(self, dataDict):
        self.id = dataDict["id"]
        self.book_id = dataDict["book_id"]
        self.name = dataDict["name"]
        self.lang = dataDict["lang"]

class ReadedBook:
    def __init__(self, dataDict):
        self.id = dataDict["id"]
        self.book_id = dataDict["book_id"]
        self.medium = dataDict["medium"]
        self.score = dataDict["score"]
        self.note = dataDict["note"]
        self.lang_read = dataDict["lang_read"]
        self.date_read = dataDict["date_read"]

