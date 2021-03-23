from movie_list import MovieList

def test_it_exists():
  csv_path = "Will"
  m1 = MovieList(csv_path)
  assert type(m1) == MovieList

def test_it_can_create_a_dataframe():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  assert m1.csv == 'movies_metadata_sample.csv'