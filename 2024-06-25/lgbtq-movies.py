import pandas as pd
import polars as pl
import polars.selectors as cs
import plotnine as pn
import seaborn as sns

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

# Avg popularity/vote by language
avg_pop_vote = lgbtq_movies.group_by(
    'original_language'
).agg(
    pl.col('popularity').mean().alias('avg_pop'),
    # Weighted avg
    (pl.col('vote_average') * pl.col('vote_count')).sum() / pl.sum('vote_count'),
    pl.col('id').count().alias('n')
).filter(
    pl.col('n') >= 10
).sort('avg_pop')

sns.barplot(
    avg_pop_vote,
    x = 'avg_pop',
    y = 'original_language'
)

pn.ggplot(
    avg_pop_vote,
    # JFC
    pn.aes(x = 'reorder(original_language,avg_pop)',y = 'avg_pop')
) + pn.geom_col() + pn.coord_flip() + pn.labs(x = 'Avg Popularity',y = 'Language')

avg_pop_vote_long = avg_pop_vote.select(
    pl.col('original_language'),
    pl.col('avg_pop'),
    pl.col('vote_average')
).melt(
    id_vars = 'original_language',
    value_vars = cs.numeric()
)

pn.ggplot(
    avg_pop_vote_long,
    pn.aes(x = 'original_language',y = 'value',fill = 'variable')
) + pn.geom_col(stat = 'identity',position = 'dodge') + pn.coord_flip()