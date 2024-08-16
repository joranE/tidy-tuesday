import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# olympics = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-06/olympics.csv',
#     null_values= ['NA','','N/A'])

# olympics.write_parquet(file = '2024-08-06/olympics.parquet')

olympics = pl.read_parquet(
  source = '2024-08-06/olympics.parquet'
).with_columns(
    pl.when(
        pl.col('medal').is_not_null()
    ).then(
        1
    ).otherwise(
        0
    ).alias('medal_flag')
)

olympics.filter(
    (pl.col('medal').is_not_null()) & (pl.col('sport') == 'Cross Country Skiing')
).group_by(
    ['id','name','season','sport']
).agg(
    pl.col('medal').count().alias('n_medals')
).sort('n_medals',descending=True).filter(pl.col('n_medals') >= 5)

olympics.group_by(
    ['season','sport','id','name']
).agg(
    pl.col('medal_flag').sum().alias('n_medals')
).group_by(
    ['season','sport']
).agg(
    pl.col('n_medals').mean().alias('median_medal_count'),
    pl.col('id').n_unique().alias('n')
).sort('median_medal_count',descending=True).filter(pl.col('n') > 1000)

medals_per_ath = olympics.group_by(
    ['season','sport','id','name','sex']
).agg(
    pl.col('medal_flag').sum().alias('n_medals'),
    pl.col('year').min().alias('min_year'),
    pl.col('year').max().alias('max_year'),
    pl.col('year').n_unique().alias('n_olympics')
)

n_per_sport = olympics.group_by(
    ['season','sport']
).agg(
    pl.col('id').n_unique().alias('n_ath'),
    pl.col('year').n_unique().alias('n_years')
).with_columns(
    (pl.col('n_ath') / pl.col('n_years')).alias('ath_per_year')
).sort('ath_per_year',descending=True)

medal_dist = medals_per_ath.group_by(
    ['season','sport','n_medals']
).len(name = 'count').sort(['season','sport','n_medals']).join(
    n_per_sport,
    how = 'left',
    on = ['season','sport']
)

medal_dist_quantiles = medal_dist.group_by(
    ['season','sport']
).agg(
    pl.col('n_medals').quantile(0.25).alias('q25'),
    pl.col('n_medals').quantile(0.5).alias('q50'),
    pl.col('n_medals').quantile(0.75).alias('q75'),
    pl.col('n_medals').mean().alias('avg')
).join(
    n_per_sport,
    how = 'left',
    on = ['season','sport']
)

medals_per_ath = medals_per_ath.join(
    medal_dist_quantiles,
    how = 'left',
    on = ['season','sport']
).join(
    n_per_sport,
    how = 'left',
    on = ['season','sport']
).with_columns(
    (pl.col('n_medals') / (pl.col('q50') + pl.col('n_ath').sqrt())).alias('medals_per_med'),
    (pl.col('n_medals') / (pl.col('avg') + pl.col('n_ath').sqrt())).alias('medals_per_avg')
)

swimming = medal_dist.filter(pl.col('sport') == 'Swimming')

(
    p9.ggplot(
        data = swimming,
        mapping = p9.aes(x = 'n_medals',y = 'count')
    ) 
    + p9.geom_col() 
    + p9.scale_y_sqrt()
)

xc_ski = medal_dist.filter(pl.col('sport') == 'Cross Country Skiing')

(
    p9.ggplot(
        data = xc_ski,
        mapping = p9.aes(x = 'n_medals',y = 'count')
    ) 
    + p9.geom_col() 
    + p9.scale_y_sqrt()
)

tramp = medal_dist.filter(pl.col('sport') == 'Trampolining')

(
    p9.ggplot(
        data = tramp,
        mapping = p9.aes(x = 'n_medals',y = 'count')
    ) 
    + p9.geom_col() 
    + p9.scale_y_sqrt()
)

medals_per_ath.filter(
    (pl.col('max_year') >= 1972) & (pl.col('n_medals') > 2) & (~pl.col('sport').is_in(['Softball','Baseball']) )
).top_k(k = 15,by = 'medals_per_med')

(
    p9.ggplot(
        data = medal_dist_quantiles,
        mapping = p9.aes(x = 'n_ath',y = 'q50')
    ) 
    + p9.geom_jitter()
    + p9.geom_smooth(method = 'lm',se = False)  
    + p9.scale_x_sqrt()
)

p9.geom_abline