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