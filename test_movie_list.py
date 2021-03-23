#import pdb; pdb.set_trace()

import math
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
  m1.add_error_column()
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

def test_it_can_flag_duplicate_records():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  test_data = [{'movie_id': 1}, {'movie_id': 1}]
  m1.movies = pd.DataFrame(test_data)
  m1.add_mark_dupes()
  assert m1.movies.columns[1] == 'dupes'
  assert m1.movies.values[0][1] == False
  assert m1.movies.values[1][1] == True

def test_it_can_check_id_is_digit():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  test_data = [{'movie_id': 1}, {'movie_id': 'a'}]
  m1.movies = pd.DataFrame(test_data)
  m1.add_id_is_digit()
  assert m1.movies.columns[1] == 'id_is_digit'
  assert m1.movies.values[0][1] == True
  assert m1.movies.values[1][1] == False

def test_it_can_validate_a_list():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  test_dict1 = {'name':'adventure'}
  test_dict2 = {'name':'crime'}
  test_list1 = f'[{test_dict1}, {test_dict2}]'
  test_list2 = f'[{test_dict1}, {test_dict2}'
  test_list3 = f'[]'
  test_list4 = ""
  assert m1.list_check(test_list1) == True
  assert m1.list_check(test_list2) == False
  assert m1.list_check(test_list3) == False
  assert m1.list_check(test_list4) == False

def test_it_can_convert_to_list():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  test_dict1 = {'name':'adventure'}
  test_dict2 = {'name':'crime'}
  test_list1 = f'[{test_dict1}, {test_dict2}]'
  test_list2 = f'[{test_dict1}, {test_dict2}'
  test_list3 = f'[]'
  assert len(m1.to_list(test_list1)) == 2
  assert m1.to_list(test_list2) == False
  assert m1.to_list(test_list3) == False

def test_it_can_add_genre_column():
  csv_path = 'movies_metadata_bad_genre.csv'
  m1 = MovieList(csv_path)
  test_dict1 = {'name':'adventure'}
  test_dict2 = {'name':'crime'}
  test_list1 = f'[{test_dict1}, {test_dict2}]'
  m1.add_genre_list()
  assert m1.movies.columns[3] == 'genre_list'
  assert len(m1.movies.values[0][3]) > 0
  assert m1.movies.values[1][3] == False
  assert len(m1.movies.values[2][3]) > 0
  assert m1.movies.values[3][3] == False
  assert len(m1.movies.values[4][3]) > 0
  assert m1.movies.values[5][3] == False
  
def test_it_can_update_error_column():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  m1.add_error_column()
  m1.add_genre_list()
  m1.update_error('genre_list', False, 'genre is not a valid list')

def test_it_can_add_validation_columns():
  csv_path = 'movies_metadata_sample.csv'
  m1 = MovieList(csv_path)
  m1.add_validations()
  columns = m1.movies.columns
  expected = ['genres', 'movie_id', 'release_date', 'error_desc', 'release_year',
       'dupes', 'id_is_digit', 'genre_list']
  for i in range(len(columns)-1):
    assert columns[i] == expected[i]