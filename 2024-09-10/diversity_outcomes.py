import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

diversity_outcomes = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-09-10/college_admissions.csv',
    null_values= ['NA','','N/A'])

diversity_outcomes.write_parquet(file = '2024-09-10/diversity_outcomes.parquet')

diversity_outcomes.group_by(
  pl.col('tier')
).agg(
  pl.col('name').n_unique().alias('n')
)

ivy_plus = diversity_outcomes.filter(pl.col('tier') == 'Ivy Plus').select(
  pl.col('tier'),
  pl.col('name')
).unique()

diversity_outcomes.filter(
  pl.col('name').str.contains('Dartmouth')
)