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
  source = '2024-07-30/summer_movies.parquet'
).with_columns(
  pl.when(pl.col('tconst') == 'tt9013026')
    .then(2021)
    .otherwise(pl.col('year'))
    .alias('year')
)

summer_movies.group_by(
  pl.col('year')
).agg(
  pl.col('average_rating').mean().alias('avg_rating')
).sort(by = 'year')

genre_ratings = summer_movies.join(
  summer_movie_genres,
  on = 'tconst'
)

(
  p9.ggplot(
    data = genre_ratings,
    mapping = p9.aes(x = 'runtime_minutes',y = 'average_rating')
  ) 
  + p9.facet_wrap('genres')
  + p9.geom_point()
)

genre_ratings.group_by(
  pl.col('genres')
).agg()