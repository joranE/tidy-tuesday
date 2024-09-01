import polars as pl 
import polars.selectors as cs
import plotnine as p9

p9.theme_set(p9.theme_bw())

qname_levels_single_response_crosswalk = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-09-03/qname_levels_single_response_crosswalk.csv',
    null_values= ['NA','','N/A'])
so_survey_questions = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-09-03/stackoverflow_survey_questions.csv',
    null_values= ['NA','','N/A'])
so_survey_single_response = pl.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-09-03/stackoverflow_survey_single_response.csv',
    null_values= ['NA','','N/A'],infer_schema_length=10000)

qname_levels_single_response_crosswalk.write_parquet(file = '2024-09-03/qname_levels_single_response_crosswalk.parquet')
so_survey_questions.write_parquet(file = '2024-09-03/so_survey_questions.parquet')
so_survey_single_response.write_parquet(file = '2024-09-03/so_survey_single_response.parquet')