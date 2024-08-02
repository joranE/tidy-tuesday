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

summer_movie_explode = summer_movies.with_columns(
  pl.col('genres').str.split(',').alias('genres_list')
).explode(columns='genres_list')

genre_runtimes = summer_movie_explode.group_by(
  pl.col('genres_list')
).agg(
  pl.col('tconst').n_unique().alias('n_movies'),
  pl.col('runtime_minutes').median().alias('med_runtime'),
  pl.col('runtime_minutes').quantile(0.75).alias('q75'),
  pl.col('runtime_minutes').quantile(0.25).alias('q25')
).filter(
  pl.col('genres_list') != 'nan'
).sort(
  'med_runtime',
  descending=False
).with_columns(
  pl.col('genres_list').cast(pl.Categorical('physical'))
)

(
  p9.ggplot(
    data = genre_runtimes,
    mapping = p9.aes(y = 'med_runtime',x = 'genres_list')
  ) 
  + p9.geom_pointrange(
    mapping = p9.aes(ymin = 'q25',ymax = 'q75')
  ) 
  + p9.coord_flip()
)

(
  p9.ggplot(
    data = summer_movies,
    mapping = p9.aes(x = 'runtime_minutes',y = 'average_rating')
  ) 
  + p9.geom_point()
)

summer_movie_explode.group_by(
  pl.col(['title_type','genres_list'])
).agg(
  pl.col('tconst').n_unique().alias('n')
).sort('n')