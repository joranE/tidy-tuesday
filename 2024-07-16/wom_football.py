import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# ewf_appearances = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_appearances.csv')
# ewf_matches = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_matches.csv')
# ewf_standings = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_standings.csv')

# ewf_appearances.write_parquet('2024-07-16/ewf_appearances.parquet')
# ewf_matches.write_parquet('2024-07-16/ewf_matches.parquet')
# ewf_standings.write_parquet('2024-07-16/ewf_standings.parquet')

ewf_appearances = pl.read_parquet('2024-07-16/ewf_appearances.parquet')
ewf_matches = pl.read_parquet('2024-07-16/ewf_matches.parquet')
ewf_standings = pl.read_parquet('2024-07-16/wf_standings.parquet')