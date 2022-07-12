SELECT DISTINCT author from ihaveread_w2 order by 1

SELECT book.*
from ihaveread_w2 book, authors_map a
where book.author = a.name


SELECT distinct book.*
from ihaveread_w2 book
where not exists (select name from authors_map a where a.name = book.author)


insert into author(name) 
select distinct norm_name from authors_map

insert into author_names(author_id, name)
select distinct a.id, m.name 
from author a, authors_map m
where a.name = m.norm_name

insert into book (id, titel, publish_date, genre, note)
SELECT id, book_title, publish_date, tags, note
from ihaveread_w2 b

insert into book_names (book_id, titel)
SELECT id, book_title
from ihaveread_w2 b

insert into book_readed (book_id, date_read, medium, score)
SELECT id, read_date, medium, substr(score, 1,1)
from ihaveread_w2 b

-- insert into author_book (book_id, author_id)
SELECT b.id, a.author_id
from ihaveread_w2 b, author_names a
where b.author = a.name

insert into author_book (book_id, author_id)
SELECT b.id, a.author_id
from author_names a, (
WITH split(word, str, id) AS (
    SELECT '', author||',', id FROM ihaveread_w2
    UNION ALL SELECT
    trim(substr(str, 0, instr(str, ','))),
    trim(substr(str, instr(str, ',')+1)),
	id
    FROM split WHERE str!=''
) SELECT word, id FROM split 
WHERE word!='') b
where b.word = a.name;


-------------
-- authors with more than 1 book
select a.id, a.name, count(ab.book_id)
from author_book ab, author a
where a.id = ab.author_id
GROUP by a.id, a.name
HAVING count(ab.book_id) > 1

-- readed books without author
SELECT distinct br.book_id, b.title
from book_readed br, book b
where  
   br.book_id = b.id
   and not exists (select author_id from author_book ab where ab.book_id = b.id)


-- all readed books
select br.book_id, br.date_read, GROUP_CONCAT(a.name, '| ') author, b.title, b.publish_date, br.medium, br.score, b.genre, b.note
from book_readed br, book b
  left join author_book ab on br.book_id = ab.book_id
  left join author a on ab.author_id = a.id
where 
   br.book_id = b.id
group by br.book_id
order by br.date_read


select br.book_id, br.date_read, a.name, b.titel, b.publish_date, br.medium, br.score, b.genre, b.note
from book_readed br, book b, author_book ab, author a 
where 
   br.book_id = b.id
   and br.book_id = ab.book_id
   and ab.author_id = a.id
order by br.date_read


--- set language

select b.*, bn.lang
from book b, book_names bn
where b.id = bn.book_id and b.title = bn.name and bn.lang is not null and b.lang is null

select b.*, a.lang
from book b, author_book ba, author a
where b.id = ba.book_id and ba.author_id = a.id and a.lang is not null and b.lang is null

update book set lang = 
(select a.lang
from book b, author_book ba, author a
where b.id = book.id and b.id = ba.book_id and ba.author_id = a.id and a.lang is not null and b.lang is null 
limit 1)
where lang is null


https://www.postgresql.org/docs/current/queries-with.html

-- split list of authors
WITH split(word, str) AS (
    SELECT '', author||',' FROM ihaveread_w2 where id in (96)
    UNION ALL SELECT
    trim(substr(str, 0, instr(str, ','))),
    trim(substr(str, instr(str, ',')+1))
    FROM split WHERE str!=''
) SELECT word FROM split WHERE word!='';


WITH split(word, str, id) AS (
    SELECT '', author||',', id FROM ihaveread_w2
    UNION ALL SELECT
    trim(substr(str, 0, instr(str, ','))),
    trim(substr(str, instr(str, ',')+1)),
	id
    FROM split WHERE str!=''
) SELECT word, id FROM split 
WHERE word!='' and id = 96
