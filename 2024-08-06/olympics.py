import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# olympics = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-06/olympics.csv',
#     null_values= ['NA','','N/A'])

# olympics.write_parquet(file = '2024-08-06/olympics.parquet')

olympics = pl.read_parquet(
  source = '2024-08-06/olympics.parquet'
)