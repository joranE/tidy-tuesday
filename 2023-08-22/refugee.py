import pandas as pd
import polars as pl
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt

refugee_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-22/population.csv'
population = pl.read_csv(refugee_url)

population['coo_iso'].n_unique()

population.groupby('year','coo_iso').agg(
    pl.col('refugees').sum().alias('n_refugees'),
    pl.col('returned_refugees').sum().alias('n_returned_refugees')
).sort('year','n_refugees').with_columns(
    (pl.col('n_returned_refugees') / pl.col('n_refugees')).alias('return_rate')
)

refugee_network = population.groupby(['year','coo_iso','coa_iso']).agg(
    pl.col('refugees').sum().alias('n_refugees'),
    pl.col('returned_refugees').sum().alias('n_returned_refugees'),
    pl.col('asylum_seekers').sum().alias('n_asylum_seekers')
)

# To the US
to_us = population.filter(pl.col('coa_iso') == 'USA').groupby(['year','coo_iso']).agg(
    pl.col('refugees').sum().alias('n_refugees')
).sort('year','n_refugees')

sns.lineplot(
    data=to_us.to_pandas(),
    x='year',
    y='n_refugees',
    hue='coo_iso'
)