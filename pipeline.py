#import relevant columns of csv data
import pandas as pd
col_list = ["id", "genres", "release_date"]
header_list = ['genres', 'movie_id', 'release_date']
df = pd.read_csv('movies_metadata_sample_copy.csv', usecols = col_list)
df.columns = header_list

#method to validate release date field
def check_date(dt_string):
  try:
    return int(pd.to_datetime(dt_string).year)
  except:
   return False

#method to validate that genres is a list of dictionaries
def to_list(genres):
  try:
    data = eval(genres)
    if type(data) == list and data != []:
      return eval(genres)
    else:
      return False
  except:
    return False

#create columns validating data accuracy
df['error_desc'] = 'no error'
df["release_year"] = df['release_date'].apply(lambda x: check_date(x))
df['dupes'] = df.duplicated(subset = 'movie_id', keep = 'first')
df['id_is_digit'] = df['movie_id'].apply(lambda x: str(x).isdigit())
df['genre_list'] = df['genres'].apply(lambda x: to_list(x))

#update invalid records with correct error description
df.loc[df['release_year'] == False, 'error_desc'] = 'bad date'
df.loc[df['dupes'] == True, 'error_desc'] = 'duplicate movie id'
df.loc[df['id_is_digit'] == False, 'error_desc'] = 'movie_id is not an integer'
df.loc[df['genre_list'] == False, 'error_desc'] = 'genre is not a valid list'