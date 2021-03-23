#import pdb; pdb.set_trace()

import pandas as pd
from movie_list import MovieList

def test_it_exists():
  csv_path = "movies_metadata_sample.csv"
  m1 = MovieList(csv_path)
  assert type(m1) == MovieList

def test_it_can_create_a_dataframe_of_movie_details():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  assert type(m1.movies) == pd.DataFrame
  assert m1.movies.columns[0] == 'genres'
  assert m1.movies.columns[1] == 'movie_id'
  assert m1.movies.columns[2] == 'release_date'

def test_it_can_add_an_error_column():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  m1.add_movies_column('error_desc', 'no error')
  assert m1.movies.columns[3] == 'error_desc'
  assert m1.movies.values[0][3] == 'no error'

def test_it_can_calc_year_from_str():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  assert m1.release_year('3/1/2020') == 2020
  assert m1.release_year('bad date') == False

def test_it_can_add_year_column():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  m1.add_release_year()
  assert m1.movies.columns[3] == 'release_year'
  assert len(str(m1.movies.values[0][3])) == 4
  assert type(m1.movies.values[0][3]) == int
