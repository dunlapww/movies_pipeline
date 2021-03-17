#import relevant columns of csv data
import pandas as pd
col_list = ["id", "genres", "release_date"]
header_list = ['genres', 'movie_id', 'release_date']
df = pd.read_csv('movies_metadata_sample.csv', usecols = col_list)
df.columns = header_list

#method to validate release date field
def check_date(dt_string):
  try:
    return int(pd.to_datetime(dt_string).year)
  except:
   return False

#ensures string contents is a list with contents
def isvalidlist(genres):
  return genres[0] == '[' and genres[-1] == ']' and len(genres) > 2

#to_list method validates that genres is a list of dictionaries
#note: I'm aware that using eval is very risky on an unknown data source
#as it exposes us to injection attacks.  Incorporating the isvalidlist attempts
#to mitigate the risk by ensuring that the contents is a list and not something more malicious
def to_list(genres):
  try:
    if isvalidlist(genres):
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

#export invalid records to csv
bad_data = df.loc[df['error_desc'] != 'no error']
headers = ['movie_id', 'genres', 'release_date', 'error_desc']
bad_data.to_csv('bad_data.csv', columns = headers, index = False)

#create clean table of data
df_clean = df.loc[df['error_desc'] == 'no error']
clean_headers = ['movie_id', 'genre_list', 'release_year']
df_clean = df_clean[clean_headers]

def has_genre(genre):
  try:
    return genre['name']
  except:
    return 'Unassigned'

#blow out movies and genres to list of dictionaries
movies = []
for row in df_clean.itertuples():
  for genre in row[2]:
    movie = {}
    movie['genre'] = has_genre(genre)
    movie['year'] = row[3]
    movie['movie_id'] = row[1]
    movies.append(movie)

#create a dataframe from those dictionaries
df_movies = pd.DataFrame(movies)

#group df_movies by year, genre, count
df_year_genre_count = df_movies.groupby(['year','genre']).count()
df_year_genre_count.rename(columns={"movie_id": "movie_count"}, inplace= True)

#export movies by year, genre, count to csv
df_year_genre_count.to_csv('movie_count_by_year_genre.csv')

print("Invalid data ingestion exported to: 'bad_data.csv'")
print("Genre summary exported to: 'movie_count_by_year_genre.csv'")