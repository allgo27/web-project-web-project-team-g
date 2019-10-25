DROP TABLE IF EXISTS books;
CREATE TABLE books (
  authors varchar(300),
  original_publication_year int,
  original_title varchar(300),
  title varchar(300),
  average_rating float(3),
  ratings_count int,
  image_url varchar(300),
  small_image_url varchar(300),
  book_id int
);

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  user_id int,
  book_id int,
  rating int
);

DROP TABLE IF EXISTS book_tags;
CREATE TABLE book_tags (
	goodreads_book_id text,
	tag_id text,
	tagcount text
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	tag_id int,
	tag_name varchar(100)
)

