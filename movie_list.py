import pandas as pd
import math
class MovieList:
  def __init__(self,csv_path):
    self.movies = self.import_movies(csv_path)
  
  def import_movies(self, csv_path):
    col_list = ["id", "genres", "release_date"]
    header_list = ['genres', 'movie_id', 'release_date']
    df = pd.read_csv(csv_path, usecols = col_list)
    df.columns = header_list
    return df

  def add_movies_column(self, column_name, column_value):
    self.movies[column_name] = column_value

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
      return []
    
    if type(eval(genres)) == list:
      return eval(genres)
    else:
      return []

  def add_genre_list(self):
    self.movies['genre_list'] = self.movies['genres'].apply(lambda x: self.to_list(x))
