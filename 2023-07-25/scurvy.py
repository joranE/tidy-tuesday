import polars as pl 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

scurvy_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-07-25/scurvy.csv'
scurvy = pl.read_csv(source = scurvy_url)

scurvy.glimpse()

scurvy.select(['treatment','dosing_regimen_for_scurvy']).unique().to_pandas()

scurvy.groupby('treatment').agg(
    pl.count('study_id').alias('n_individuals')
)