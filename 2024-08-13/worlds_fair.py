import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

worlds_fair = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-13/worlds_fairs.csv',
    null_values= ['NA','','N/A'])

worlds_fair.write_parquet(file = '2024-08-06/olympics.parquet')