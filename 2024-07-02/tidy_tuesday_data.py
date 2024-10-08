import polars as pl 
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')

#tt_datasets = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-02/tt_datasets.csv')
#tt_summary = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-02/tt_summary.csv')
#tt_urls = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-02/tt_urls.csv')
#tt_variables = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-02/tt_variables.csv',ignore_errors=True)

#tt_datasets.write_parquet('2024-07-02/tt_datasets.parquet')
#tt_summary.write_parquet('2024-07-02/tt_summary.parquet')
#tt_urls.write_parquet('2024-07-02/tt_urls.parquet')
#tt_variables.write_parquet('2024-07-02/tt_variables.parquet')

tt_datasets = pl.read_parquet('2024-07-02/tt_datasets.parquet')
tt_summary = pl.read_parquet('2024-07-02/tt_summary.parquet')
tt_urls = pl.read_parquet('2024-07-02/tt_urls.parquet')
tt_variables = pl.read_parquet('2024-07-02/tt_variables.parquet')

# Scatterplot of variables vs observations
plt.clf()
plt.yscale('log')
plt.xscale('log')
p = sns.scatterplot(
    data = tt_datasets,
    x = 'variables',
    y = 'observations',
    color = 'blue'
)

tt_datasets = tt_datasets.with_columns(
    pl.concat_str('year','week',separator='-').alias('year_week') + '-2'
)

tt_datasets = tt_datasets.with_columns(
    pl.col('year_week').str.strptime(pl.Date,"%Y-%W-%w",strict = False).alias('date')
)

plt.clf()
plt.yscale('log')
plt.xscale('linear')
p = sns.lineplot(
    data = tt_datasets,
    x = 'date',
    y = 'observations',
    color = 'blue'
)
