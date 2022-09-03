-- postgres tables

CREATE TABLE author (
	id serial NOT NULL,
	"name" text NOT NULL,
	"lang" text NULL,
	"note" text NULL,
	CONSTRAINT artist_pk PRIMARY KEY (id)
);

CREATE TABLE author_book (
	"author_id"	int4 NOT NULL,
	"book_id"	int4 NOT NULL,
	CONSTRAINT author_book_pk PRIMARY KEY (author_id, book_id),
	CONSTRAINT author_book_fk1 FOREIGN KEY (book_id) REFERENCES book(id)
	CONSTRAINT author_book_fk2 FOREIGN KEY (author_id) REFERENCES author(id)
);

CREATE TABLE author_names (
	id serial NOT NULL,
	"author_id"	int4 NOT NULL,
	"name"	TEXT NOT NULL,
	"lang"	TEXT NULL,
	"type"	TEXT NULL,
	CONSTRAINT author_names_pk PRIMARY KEY (id),
	CONSTRAINT author_names_fk FOREIGN KEY (author_id) REFERENCES author(id)
);

CREATE TABLE book (
	id serial NOT NULL,
	"title"	TEXT NOT NULL,
	"publish_date"	TEXT,
	"lang"	TEXT,
	"genre"	TEXT,
	"note"	TEXT,
	CONSTRAINT book_pk PRIMARY KEY (id)
);

CREATE TABLE book_names (
	id serial NOT NULL,
	book_id	int4 NOT NULL,
	"name"	TEXT NOT NULL,
	"lang"	TEXT NOT NULL,
	CONSTRAINT book_names_pk PRIMARY KEY (id),
	CONSTRAINT book_names_fk FOREIGN KEY (book_id) REFERENCES book(id)
);
CREATE UNIQUE INDEX book_names_uk_idx ON book_names (book_id,"name",lang);

CREATE TABLE book_readed (
	id serial NOT NULL,
	book_id	int4 NOT NULL,
	"date_read"	TEXT,
	"lang_read"	TEXT NOT NULL,
	"medium"	TEXT,
	"score"	int4,
	"title_read"	TEXT,
	"note"	TEXT,
	CONSTRAINT book_readed_pk PRIMARY KEY (id),
	CONSTRAINT book_readed_fk FOREIGN KEY (book_id) REFERENCES book(id)
);
