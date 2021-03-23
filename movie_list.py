import pandas as pd

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

  