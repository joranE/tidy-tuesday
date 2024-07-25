import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# auditions = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/auditions.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True,
#   infer_schema_length=10000)
# eliminations = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/eliminations.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True)
# finalists = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/finalists.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True,
#   infer_schema_length=10000,
#   ignore_errors=True)
# ratings = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/ratings.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True,
#   infer_schema_length=10000)
# seasons = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/seasons.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True)
# songs = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-23/songs.csv',
#   null_values = ['NA',''],
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