DROP TABLE IF EXISTS books;
CREATE TABLE books (
  authors text,
  original_publication_year text,
  original_title text,
  title text,
  average_rating text,
  ratings_count text,
  image_url text,
  small_image_url text,
  book_id text
);

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  user_id text,
  book_id text,
  rating text
);

DROP TABLE IF EXISTS book_tags;
CREATE TABLE book_tags (
	goodreads_book_id text,
	tag_id text,
	tagcount text
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	tag_id text,
	tag_name text
);

