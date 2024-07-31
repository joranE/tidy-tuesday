import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# summer_movie_genres = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-30/summer_movie_genres.csv',
#   null_values= ['NA','','N/A']
# )
# summer_movies = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-30/summer_movies.csv',
#   null_values=['NA','','N/A']
# )

# summer_movie_genres.write_parquet(file = '2024-07-30/summer_movie_genres.parquet')
# summer_movies.write_parquet(file = '2024-07-30/summer_movies.parquet')

summer_movie_genres = pl.read_parquet(
  source = '2024-07-30/summer_movie_genres.parquet'
)
summer_movies = pl.read_parquet(
  source = '2024-07-30/summer_moveis.parquet'
)