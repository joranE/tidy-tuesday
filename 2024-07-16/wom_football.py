import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

# ewf_appearances = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_appearances.csv',
#   null_values = ['NA',''],
#   try_parse_dates = True)
# ewf_matches = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_matches.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True)
# ewf_standings = pl.read_csv(
#   source = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-07-16/ewf_standings.csv',
#   null_values = ['NA',''],
#   try_parse_dates=True)

# ewf_appearances.write_parquet('2024-07-16/ewf_appearances.parquet')
# ewf_matches.write_parquet('2024-07-16/ewf_matches.parquet')
# ewf_standings.write_parquet('2024-07-16/ewf_standings.parquet')

ewf_appearances = pl.read_parquet('2024-07-16/ewf_appearances.parquet')
ewf_matches = pl.read_parquet('2024-07-16/ewf_matches.parquet')
ewf_standings = pl.read_parquet('2024-07-16/ewf_standings.parquet')

# unadjusted points versus goal difference
(
  p9.ggplot(
    data = ewf_standings.with_columns(
      (pl.col('points') - pl.col('point_adjustment')).alias('unadj_points')
    ),
    mapping = p9.aes(x = 'goal_difference',y = 'unadj_points')
  ) 
  + p9.geom_point(p9.aes(color = 'position'))
  + p9.geom_smooth(method = 'lm',se = False,color = 'black') 
  + p9.labs(x = 'Goal differential',y = 'Points',color = 'Position') 
  + p9.theme(legend_position = 'bottom',legend_direction = 'horizontal')
)

# attendance over time by tier
(
  p9.ggplot(
    data = ewf_matches,
    mapping = p9.aes(x = 'date',y = 'attendance')
  ) 
  + p9.facet_wrap('tier',nrow = 2,labeller='label_both')
  + p9.geom_point()
  + p9.scale_y_log10()
)

# Attendance by team & season?
team_attendance = ewf_appearances.group_by(
  pl.col('team_id'),pl.col('team_name'),pl.col('season')
).agg(
  (pl.col('attendance').sum() / pl.col('match_id').n_unique()).alias('per_match')
).sort(
  pl.col('per_match'),descending=True
).with_columns(
  pl.col('season').str.slice(0,4).cast(pl.Int32).alias('year_int'),
  pl.when(
    pl.col('per_match') == 0
  ).then(None).otherwise(pl.col('per_match')).alias('per_match')
)

(
  p9.ggplot(
    data = team_attendance,
    mapping = p9.aes(x = 'year_int',y = 'per_match',group = 'team_name')
  ) 
  + p9.geom_line()
  + p9.scale_y_log10()
)