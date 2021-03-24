import pandas as pd
import math

class MovieList:
  def __init__(self,csv_path):
    self.movies = self.import_movies(csv_path)
    #self.bad_data = self.bad_data()
  
  def import_movies(self, csv_path):
    col_list = ["id", "genres", "release_date"]
    header_list = ['genres', 'movie_id', 'release_date']
    df = pd.read_csv(csv_path, usecols = col_list)
    df.columns = header_list
    return df

  def add_error_column(self):
    self.movies['error_desc'] = 'no error'

  def release_year(self, dt_string):
    try:
      return int(pd.to_datetime(dt_string).year)
    except:
     return False
  
  def add_release_year(self):
    self.movies["release_year"] = self.movies['release_date'].apply(lambda x: self.release_year(x))

  def add_mark_dupes(self):
    self.movies['dupes'] = self.movies.duplicated(subset = 'movie_id', keep = 'first')

  def add_id_is_digit(self):
    self.movies['id_is_digit'] = self.movies['movie_id'].apply(lambda x: str(x).isdigit())

  #this method reduces risk of using 'eval' in the to_list method
  #by ensuring the string contents is generally of list structure
  def list_check(self, data):
    try:
      if math.isnan(data): return False
    except:
      return len(data) > 2 and data[0] == '[' and data[-1] == ']'
  
  def to_list(self, genres):
    if self.list_check(genres) == False: 
      return False
    
    if type(eval(genres)) == list:
      return eval(genres)
    else:
      return False

  def add_genre_list(self):
    self.movies['genre_list'] = self.movies['genres'].apply(lambda x: self.to_list(x))

  def add_validations(self):
    self.add_error_column()
    self.add_release_year()
    self.add_mark_dupes()
    self.add_id_is_digit()
    self.add_genre_list()
  
  def update_error(self, search_column_name, criteria, message):
    self.movies.loc[self.movies[search_column_name] == criteria, 'error_desc'] = message

  def update_all_errors(self):
    self.update_error('release_year', False, 'bad date')
    self.update_error('dupes', True, 'duplicate movie id')
    self.update_error('id_is_digit', False, 'movie_id is not an integer')
    self.update_error('genre_list', False, 'genre is not a valid list')
    
  def bad_data(self):
    self.add_validations()
    self.update_all_errors()
    return self.movies.loc[self.movies['error_desc'] != 'no error']
  
  def export_bad_data(self):
    headers = ['movie_id', 'genres', 'release_date', 'error_desc']
    self.bad_data().to_csv('bad_data.csv', columns = headers, index = False)