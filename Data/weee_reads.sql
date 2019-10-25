DROP TABLE IF EXISTS books;
CREATE TABLE books (
  authors varchar(300),
  original_publication_year int(4),
  original_title varchar(300),
  title varchar(300),
  average_rating float(3, 2),
  ratings_count int (10)
  image_url varchar(300),
  small_image_url varchar(300),
  book_id int (5)
);

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  user_id int(4),
  book_id int(5),
  rating int(1)
);

DROP TABLE IF EXISTS book_tags;
CREATE TABLE book_tags (
	goodreads_book_id int(4),
	tag_id int(6),
	tagcount int(10)
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	tag_id int(6),
	tag_name varchar(100)
)

