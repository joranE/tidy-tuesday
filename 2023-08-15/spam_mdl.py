import numpy as np
import pandas as pd 
import polars as pl 
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.metrics import accuracy_score, make_scorer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import PowerTransformer
from sklearn.pipeline import Pipeline

spam_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-15/spam.csv'
spam = pl.read_csv(spam_url)

# Add a column that counts rows
spam = spam.with_columns(
    pl.Series(np.arange(1,spam.shape[0] + 1)).alias('case_id')
)

# Convert to long to aid in plotting
spam_long = spam.melt(
    id_vars = ['yesno','case_id'],
    value_vars= ['crl.tot','dollar','bang','money','n000','make'],
    value_name = 'val',
    variable_name='var'
)

# Normalize
spam_long = spam_long.with_columns(
    ((pl.col('val') - pl.col('val').mean()) / pl.col('val').std()).over('var').alias('val_norm')
)

# Plot
sns.displot(
    data=spam_long.to_pandas(),
    x = 'val_norm',
    hue = 'yesno',
    kind = 'kde',
    col='var',
    col_wrap=2,
    log_scale=True
)

# Train test split
X = spam[['crl.tot','dollar','bang','money','n000','make']]
y = spam['yesno']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Log transformer function
def log_transform(x):
    return np.log(x + 0.01)

# Classifiers
baseline = DummyClassifier(
    strategy='most_frequent', 
    random_state=42
)
logreg_cv = LogisticRegressionCV(
    penalty = 'l2',
    solver = 'liblinear',
    random_state=42
)
rf = RandomForestClassifier(
    n_estimators=1000,
    criterion='entropy',
    max_features=1,
    random_state=42
)
gb = GradientBoostingClassifier(
    learning_rate=0.01,
    max_depth=5,
    n_estimators=500,
    subsample=0.5,
    random_state=42
)

# Pipelines
pipe_bl = Pipeline([
    ('yj_transform', PowerTransformer()),
    ('baseline', baseline)
])

pipe_lr = Pipeline([
    ('yj_transform', PowerTransformer()),
    ('logreg', logreg_cv)
])

pipe_rf = Pipeline([
    #('yj_transform', PowerTransformer()),
    ('rf', rf)
])

pipe_gb = Pipeline([
    ('yj_transform', PowerTransformer()),
    ('gb', gb)
])

# Cross validation
param_rf = {
    'criterion': ['gini', 'entropy'], 
    'max_features': [1,2,3]
}
param_lr = {'penalty': ['l1', 'l2'], 
            'solver': ['liblinear', 'saga']
}
param_gb = {
    'n_estimators': [100, 500, 1000],
    'max_depth': [3, 5, 10],
    'learning_rate': [0.01, 0.1, 1],
    'subsample': [0.5, 0.75, 1]
}

scoring = {"AUC": "roc_auc", "Accuracy": make_scorer(accuracy_score)}

grid_rf = GridSearchCV(rf, param_rf, cv=5, scoring = scoring,refit='AUC')
grid_lr = GridSearchCV(logreg_cv, param_lr, cv=5, scoring = scoring,refit='AUC')
grid_gb = GridSearchCV(gb, param_gb, cv=5, scoring = scoring,refit='AUC')

grid_rf.fit(X_train, y_train)
grid_lr.fit(X_train, y_train)
grid_gb.fit(X_train, y_train)

grid_rf.best_params_
grid_lr.best_params_
grid_gb.best_params_

pd.DataFrame(grid_lr.cv_results_)
pd.DataFrame(grid_rf.cv_results_)
pd.DataFrame(grid_gb.cv_results_)

# Fit
pipe_bl.fit(X_train, y_train)
pipe_lr.fit(X_train, y_train)
pipe_rf.fit(X_train, y_train)
pipe_gb.fit(X_train, y_train)

# Score
pipe_bl.score(X_test, y_test)
pipe_lr.score(X_test, y_test)
pipe_rf.score(X_test, y_test)
pipe_gb.score(X_test, y_test)

# Coefficients
pipe_lr['logreg'].coef_