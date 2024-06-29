import polars as pl

episode_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-08/episodes.csv'
sauces_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-08/sauces.csv'
seasons_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-08/seasons.csv'

episodes = pl.read_csv(source = episode_url,use_pyarrow=True)
sauces = pl.read_csv(source = sauces_url,use_pyarrow=True)
seasons = pl.read_csv(source=seasons_url,use_pyarrow=True)
