import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

drob_funs = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-09/drob_funs.csv')

# Column with package::function
drob_funs = drob_funs.with_columns(
    (pl.col('pkgs') + '::' + pl.col('funs')).alias('pkg_fun')
)

# Functions in multiple packages
# Doesn't appear that functions marked with 'in_multiple_pkgs' actually appear in 
# the code from multiple packages, maybe that's just a general thing
drob_funs.filter(
    pl.col('in_multiple_pkgs')
).group_by(
    pl.col('funs')
).agg(
    pl.col('pkgs').unique().str.concat(',').alias('all_pkgs'),
    pl.col('pkgs').n_unique().alias('n')
).sort(by = pl.col('n'),descending=True)

top_funs = drob_funs.group_by(
    pl.col('funs')
).agg(
    pl.col('funs').count().alias('n')
).top_k(
    k = 40,
    by = pl.col('n')
).sort(
    by = pl.col('n'),
    descending=False
).with_columns(
    pl.col('funs').cast(pl.Categorical('physical'))
)

(
    p9.ggplot(
        top_funs,
        p9.aes(x = 'funs',y = 'n')
    ) 
    + p9.geom_col() 
    + p9.coord_flip()
)