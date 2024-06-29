import pandas as pd 
import polars as pl 
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt

global_temps = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-07-11/global_temps.csv')
nh_temps = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-07-11/nh_temps.csv')
sh_temps = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-07-11/sh_temps.csv')
zonann_temps = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-07-11/zonann_temps.csv')

global_temps.glimpse()
nh_temps.glimpse()
sh_temps.glimpse()
zonann_temps.glimpse()

# Global temps for meterological seasons
gt_met_seasons = global_temps.select(
    ['Year','DJF','MAM','JJA','SON']
).melt(
    id_vars = ['Year'],
    value_vars = ['DJF','MAM','JJA','SON'],
    variable_name = 'season',
    value_name = 'temp'
).with_columns(
    pl.when(pl.col('season') == 'DJF').then(pl.lit('Winter'))
    .when(pl.col('season') == 'MAM').then(pl.lit('Spring'))
    .when(pl.col('season') == 'JJA').then(pl.lit('Summer'))
    .when(pl.col('season') == 'SON').then(pl.lit('Autumn')).alias('season')
)

sns.lineplot(
    data = gt_met_seasons.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'season'
)
plt.show()

# NH temps for meterological seasons
nht_met_seasons = nh_temps.select(
    ['Year','DJF','MAM','JJA','SON']
).melt(
    id_vars = ['Year'],
    value_vars = ['DJF','MAM','JJA','SON'],
    variable_name = 'season',
    value_name = 'temp'
).with_columns(
    pl.when(pl.col('season') == 'DJF').then(pl.lit('Winter'))
    .when(pl.col('season') == 'MAM').then(pl.lit('Spring'))
    .when(pl.col('season') == 'JJA').then(pl.lit('Summer'))
    .when(pl.col('season') == 'SON').then(pl.lit('Autumn')).alias('season')
)

sns.lineplot(
    data = nht_met_seasons.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'season'
)
plt.show()

# SH temps for meterological seasons
sht_met_seasons = sh_temps.select(
    ['Year','DJF','MAM','JJA','SON']
).melt(
    id_vars = ['Year'],
    value_vars = ['DJF','MAM','JJA','SON'],
    variable_name = 'season',
    value_name = 'temp'
).with_columns(
    pl.when(pl.col('season') == 'DJF').then(pl.lit('Winter'))
    .when(pl.col('season') == 'MAM').then(pl.lit('Spring'))
    .when(pl.col('season') == 'JJA').then(pl.lit('Summer'))
    .when(pl.col('season') == 'SON').then(pl.lit('Autumn')).alias('season')
)

sns.lineplot(
    data = sht_met_seasons.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'season'
)
plt.show()

# Compare July temps for NH and SH
nh_july = nh_temps.select(
    ['Year','Jul']
).with_columns(
    pl.lit('Northern Hemisphere').alias('Hemisphere')
)

sh_july = sh_temps.select(
    ['Year','Jul']
).with_columns(
    pl.lit('Southern Hemisphere').alias('Hemisphere')
)

jul_temps = nh_july.vstack(sh_july)

sns.lineplot(
    data = jul_temps.to_pandas(),
    x = 'Year',
    y = 'Jul',
    hue = 'Hemisphere'
)

# Checking where some missing values were
# Was just a mistake from earlier
jul_temps.pivot(
    index = 'Year',
    values = 'Jul',
    columns = 'Hemisphere'
)

jul_temps = jul_temps.with_columns(
    pl.col('Jul').pct_change().over('Hemisphere').alias('Jul_pct_change')
)

sns.lineplot(
    data = jul_temps.to_pandas(),
    x = 'Year',
    y = 'Jul_pct_change',
    hue = 'Hemisphere'
)

jul_temps.filter(pl.col('Jul_pct_change').abs() >= 10)

jul_temps_cor = jul_temps.select(
    ['Year','Jul','Hemisphere']
).pivot(
    values = 'Jul',
    index = 'Year',
    columns = 'Hemisphere',
    aggregate_function=None
)

# NH & SH July (relative) temps are highly correlated; shocker
sns.regplot(
    data = jul_temps_cor.to_pandas(),
    x = 'Northern Hemisphere',
    y = 'Southern Hemisphere',
    ci = None,
    lowess = True
)

# Are some months more correlated than others?
nh = nh_temps.with_columns(
    pl.lit('Northern Hemisphere').alias('Hemisphere')
)
sh = sh_temps.with_columns(
    pl.lit('Southern Hemisphere').alias('Hemisphere')
)

nh_sh = nh.vstack(sh)

nh_sh_mo_cor = nh_sh.melt(
    id_vars = ['Year','Hemisphere'],
    value_vars = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    variable_name = 'Month',
    value_name = 'temp'
).pivot(
    values = 'temp',
    index = ['Year','Month'],
    columns = 'Hemisphere',
    aggregate_function=None
)

nh_sh_mo_cor.groupby(
    'Month'
).agg(
    pl.corr(a = 'Northern Hemisphere',b = 'Southern Hemisphere').alias('cor')
).sort(pl.col('cor'))

sns.lmplot(
    data = nh_sh_mo_cor.to_pandas(),
    x = 'Northern Hemisphere',
    y = 'Southern Hemisphere',
    col = 'Month',
    col_wrap = 4,
    ci = None,
    lowess=True
)

zone_temps = zonann_temps.select(
    cs.by_name('Year') | cs.contains('-')
).melt(
    id_vars = ['Year'],
    value_vars = zonann_temps.columns[4:],
    variable_name = 'zone',
    value_name = 'temp'
)

sns.lineplot(
    data = zone_temps.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'zone'
)

zone_temps_64_90 = zone_temps.filter(
    pl.col('zone').is_in(['64N-90N','90S-64S'])
)

sns.lineplot(
    data = zone_temps_64_90.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'zone'
)

zone_temps_0_64 = zone_temps.filter(
    ~pl.col('zone').is_in(['64N-90N','90S-64S'])
)

sns.lineplot(
    data = zone_temps_0_64.to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'zone'
)

zone_bands = zonann_temps.select(
    ['Year','44N-64N','24N-44N','EQU-24N','24S-EQU','44S-24S','64S-44S']
).melt(
    id_vars = ['Year'],
    value_vars = ['44N-64N','24N-44N','EQU-24N','24S-EQU','44S-24S','64S-44S'],
    variable_name = 'zone',
    value_name = 'temp'
)

sns.lineplot(
    data = zone_bands.filter(pl.col('Year') >= 1980).to_pandas(),
    x = 'Year',
    y = 'temp',
    hue = 'zone'
)

# Rolling mean by zone
zone_bands_roll = zone_bands.with_columns(
    pl.col('temp').rolling_mean(window_size=15).over('zone').alias('temp_roll')
)

g = sns.lineplot(
    data = zone_bands_roll.to_pandas(),
    x = 'Year',
    y = 'temp_roll',
    hue = 'zone'
)
g.set_ylabel('10 Yr Rolling Avg')
plt.show()
