import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

english_monarchs = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-20/english_monarchs_marriages_df.csv',
    null_values= ['NA','','N/A','\u2013','?'])

english_monarchs.write_parquet(file = '2024-08-20/english_monarchs.parquet')

english_monarchs = english_monarchs.with_columns(
    pl.when(pl.col('year_of_marriage')
        .str.contains('(?)',literal = True))
        .then(pl.lit('uncertain'))
        .alias('unk_flag'),
    pl.col('year_of_marriage')
        .str.extract(r"([0-9]+)")
        .cast(pl.Int16)
        .alias('marriage_year'),
    pl.col('king_age')
        .str.extract(r"([0-9]+)")
        .cast(pl.Int16)
        .alias('age')
)


