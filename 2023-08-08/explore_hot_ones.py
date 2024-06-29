import polars as pl
import matplotlib.pyplot as plt
import plotnine as p9
import seaborn as sns

# Completion rate by season 
episode_count_compl_rate = episodes.groupby('season').agg(
    pl.col('episode_season').count().alias('total_episodes'),
    pl.col('finished').mean().alias('completion_rate')
).sort(by='season',descending=False)

# Bar plot of completion rate by season
(p9.ggplot(
    episode_count_compl_rate,
    p9.aes(x='season',y='completion_rate')) + 
    p9.geom_col() + 
    p9.scale_y_continuous(labels= lambda x: [f'{i:.0%}' for i in x]) +
    p9.labs(
        x = 'Season',
        y = 'Completion Rate',
        title = 'Completion Rate by Season') + 
    p9.theme_minimal()
)

# Avg scoville by season
sauces.groupby('season').agg(
    pl.col('scoville').mean().alias('avg_scoville')
).sort(by='season',descending=False)

# Always 10 sauces per episode
sauces.groupby('season').agg(
    pl.col('sauce_number').count().alias('total_sauces')
).sort(by='season',descending=False)

# Avg scoville by sauce number
sns.lineplot(
    data = sauces.to_pandas(),
    x = 'season',
    y = 'scoville',
    errorbar = 'ci'
)
plt.show()

# Convert season to string
sauces = sauces.with_columns(
    pl.col('season').cast(pl.Utf8).alias('season_grp')
)

# Plot log scoville by sauce number
p = sns.lineplot(
    data = sauces.to_pandas(),
    x = 'sauce_number',
    y = 'scoville',
    hue = 'season_grp',
    legend = False,
    palette = sns.color_palette('colorblind'),
)
p.set(yscale = 'log')
p.set(xticks = [i for i in range(1,11)])
p.set(
    xlabel = 'Sauce Number', 
    ylabel = 'log(Scoville)',
    title = 'Scoville (log) by Sauce Number'
)
plt.show()

# How frequently are sauces used?
(
    sauces.with_columns(
        pl.col('scoville').log().round(decimals = 1).alias('log_scoville')
    ).groupby('sauce_name','log_scoville').agg(
        pl.col('season').count().alias('total_seasons')
    ).sort(by=['total_seasons','log_scoville'],descending=True).to_pandas()
)

# Guests who have been on more than once
repeat_guests = episodes.select(['guest','guest_appearance_number']).filter(
    pl.col('guest_appearance_number') > 1
).unique() 

# Pivot table of repeat guests and whether they finished
episodes.join(
    repeat_guests,
    on = ['guest'],
    how = 'inner'
).select(['guest','guest_appearance_number','finished']).pivot(
    values = 'finished',
    index = 'guest',
    columns = 'guest_appearance_number',
    aggregate_function = None).to_pandas()