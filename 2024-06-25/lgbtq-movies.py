import pandas as pd
import polars as pl
import plotnine as pn
import numpy as np

# lgbtq_movies = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-06-25/lgbtq_movies.csv')
# lgbtq_movies.write_parquet('2024-06-25/lgbtq_movies.parquet')

lgbtq_movies = pl.read_parquet(
    '2024-06-25/lgbtq_movies.parquet'
)

# Top 5 most popular overall
lgbtq_movies.top_k(
    k = 5,
    by = pl.col('popularity')
)

# Top 5 most popular english language
lgbtq_movies.filter(
    pl.col('original_language') == 'en'
).top_k(
    k = 5,
    by = pl.col('popularity')
)

# Plot popularity vs vote average
pn.ggplot(
    lgbtq_movies.with_columns(pl.col('popularity').log().alias('log_pop')),
    pn.aes(x = "log_pop",y = "vote_average")
) + pn.geom_point()
