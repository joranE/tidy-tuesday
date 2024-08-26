import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

english_monarchs = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-20/english_monarchs_marriages_df.csv',
    null_values= ['NA','','N/A'])

english_monarchs.write_parquet(file = '2024-08-20/english_monarchs.parquet')