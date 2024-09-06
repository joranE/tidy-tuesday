import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

worlds_fair = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-08-13/worlds_fairs.csv',
    null_values= ['NA','','N/A'])

#worlds_fair.write_parquet(file = '2024-08-06/olympics.parquet')

(
    p9.ggplot(
        data = worlds_fair,
        mapping = p9.aes(x = 'start_year',y = 'visitors')
    ) + 
    p9.geom_line()
)

(
    p9.ggplot(
        data = worlds_fair,
        mapping = p9.aes(x = 'start_year',y = 'attending_countries')
    ) + 
    p9.geom_line()
)

(
    p9.ggplot(
        data = worlds_fair,
        mapping = p9.aes(x = 'start_year',y = 'cost')
    ) + 
    p9.geom_line()
)

(
    p9.ggplot(
        data = worlds_fair,
        mapping = p9.aes(x = 'start_year',y = 'area')
    ) + 
    p9.geom_line()
)