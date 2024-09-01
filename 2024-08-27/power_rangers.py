import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

power_rangers_episodes = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-27/power_rangers_episodes.csv',
    null_values= ['NA','','N/A'])
power_rangers_seasons = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-27/power_rangers_seasons.csv',
    null_values= ['NA','','N/A'])

power_rangers_episodes.write_parquet(file = '2024-08-27/power_rangers_episodes.parquet')
power_rangers_seasons.write_parquet(file = '2024-08-27/power_rangers_seasons.parquet')