#import relevant columns of csv data
import pandas as pd
col_list = ["id", "genres", "release_date"]
header_list = ['genres', 'movie_id', 'release_date']
df = pd.read_csv('movies_metadata_sample_copy.csv', usecols = col_list)
df.columns = header_list

