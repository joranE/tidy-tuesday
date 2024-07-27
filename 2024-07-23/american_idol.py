import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# auditions = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/auditions.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True,
#   infer_schema_length=10000)
# eliminations = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/eliminations.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True)
# finalists = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/finalists.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True,
#   infer_schema_length=10000,
#   ignore_errors=True)
# ratings = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/ratings.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True,
#   infer_schema_length=10000)
# seasons = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/seasons.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True)
# songs = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/songs.csv',
#   null_values = ['NA','','N/A'],
#   try_parse_dates=True)

# auditions.write_parquet('2024-07-23/auditions.parquet')
# eliminations.write_parquet('2024-07-23/eliminations.parquet')
# finalists.write_parquet('2024-07-23/finalists.parquet')
# ratings.write_parquet('2024-07-23/ratings.parquet')
# seasons.write_parquet('2024-07-23/seasons.parquet')
# songs.write_parquet('2024-07-23/songs.parquet')

auditions.read_parquet('2024-07-23/auditions.parquet')
eliminations.read_parquet('2024-07-23/eliminations.parquet')
finalists.read_parquet('2024-07-23/finalists.parquet')
ratings.read_parquet('2024-07-23/ratings.parquet')
seasons.read_parquet('2024-07-23/seasons.parquet')
songs.read_parquet('2024-07-23/songs.parquet')

finalists = finalists.with_columns(
  pl.col('Birthday').str.to_date('%d-%b-%y').alias('Birthday')
)

date_pattern = r"\((\d{4}-\d{2}-\d{2})\)"
season_date = seasons.with_columns(
    pl.col("original_release").str.extract(date_pattern, 1).alias("original_release_date")
).with_columns(
  pl.col('original_release_date').str.to_date('%Y-%m-%d').alias('original_release_date')
).select(
  pl.col('season').alias('Season'),
  pl.col('original_release_date')
).unique()

finalists_age = finalists.join(
  season_date,
  how = 'left',
  on = 'Season'
).with_columns(
  (pl.col('original_release_date') - pl.col('Birthday')).cast(pl.Duration).dt.total_days().cast(pl.Int32).alias('age')
).with_columns(
  (pl.col('age') / 365.25).alias('age_years')
)

finalists_age.group_by(
  pl.col('Season')
).agg(
  pl.col('age').mean() / 365.25
)

(
  p9.ggplot(
    data = finalists_age.with_columns(
      pl.col('Season').cast(pl.String).alias('season'),
      (pl.col('age') / 365.25).alias('age_years')
    ),
    mapping = p9.aes(x = 'age_years',color = 'season',group = 'season')
  ) 
  + p9.geom_density()
)

finalists_age_agg = finalists_age.group_by(
  pl.col('Season')
).agg(
  (pl.col('age') / 365.25).mean().alias('avg_age'),
  (pl.col('age') / 365.25).std().alias('sd_age')
)

(
  p9.ggplot(
    data = finalists_age,
    mapping = p9.aes(y = 'age_years',x = 'Season',group = 'Season')
  ) 
  + p9.geom_boxplot() 
  + p9.coord_flip()
)