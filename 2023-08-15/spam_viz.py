import numpy as np
import pandas as pd 
import polars as pl 
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA

spam_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-08-15/spam.csv'
spam = pl.read_csv(spam_url)

# Add a column that counts rows
spam = spam.with_columns(
    pl.Series(np.arange(1,spam.shape[0] + 1)).alias('case_id')
)

# Select values where all features are zero
spam.filter(
    (pl.col('crl.tot') == 1) & 
    (pl.col('dollar') == 0) &
    (pl.col('bang') == 0) &
    (pl.col('money') == 0) &
    (pl.col('n000') == 0) &
    (pl.col('make') == 0) 
).groupby('yesno').agg(
    pl.col('yesno').count().alias('count')
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

# Scatterplot
sns.scatterplot(
    data=spam.to_pandas(),
    x = 'money',
    y = 'n000',
    hue = 'yesno',
    alpha = 0.25
)

# PCA
pca = PCA()
pipe_pca = Pipeline([
    ('yj_transform', PowerTransformer()),
    ('pca', pca)
])
X_pca = spam[['crl.tot','dollar','bang','money','n000','make']]
X_pca = pipe_pca.fit_transform(X_pca)
X_t = pd.DataFrame(
    X_pca
).rename(
    columns = {0:'PC1',1:'PC2',2:'PC3',3:'PC4',4:'PC5',5:'PC6'}
)
X_t['yesno'] = spam['yesno'].to_pandas()

# Plot
sns.scatterplot(
    data=X_t,
    x = 'PC1',
    y = 'PC2',
    hue = 'yesno',
    alpha = 0.25
)

# Kernel PCA
kpca = KernelPCA(kernel='rbf')
pipe_pca = Pipeline([
    ('yj_transform', PowerTransformer()),
    ('kpca', kpca)
])
X_kpca = spam[['crl.tot','dollar','bang','money','n000','make']]
X_kpca = pipe_pca.fit_transform(X_kpca)
X_kt = pd.DataFrame(
    X_kpca
).rename(
    columns = {0:'kPC1',1:'kPC2',2:'kPC3',3:'kPC4',4:'kPC5',5:'kPC6'}
)
X_kt['yesno'] = spam['yesno'].to_pandas()

# Plot
sns.scatterplot(
    data=X_kt,
    x = 'kPC2',
    y = 'kPC3',
    hue = 'yesno',
    alpha = 0.25
)

# Column bind X_t and X_kt
X_tt = pd.concat([X_t,X_kt[['kPC1','kPC2','kPC3','kPC4','kPC5','kPC6']]],axis=1)
X_tt = pl.DataFrame(X_tt)
X = X_tt.select(
    cs.contains('PC')
)
y = X_tt['yesno']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

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
    ('baseline', baseline)
])

pipe_lr = Pipeline([
    ('logreg', logreg_cv)
])

pipe_rf = Pipeline([
    ('rf', rf)
])

pipe_gb = Pipeline([
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
