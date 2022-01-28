import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


cars =  pd.read_csv("cleaned_data.csv")

X =  cars[['Name', 'style', 'Exterior color', 'interior color', 'Engine',
       'drive type', 'Fuel Type', 'Transmission', 'Mileage', 'mpg city',
       'mpg highway', 'Year', 'Engine V', 'Brand']]


Y = cars["price"].values

onehot = OneHotEncoder(categories="auto", handle_unknown="ignore")
categorical_features = onehot.fit_transform(X.iloc[:, [1,4,5,6,7,13]]).toarray()

X = np.delete(X.values, [0,1,2,3,4,5,6,7,13], 1)
X = np.concatenate((X,categorical_features), axis=1)


x_train, x_test, y_train, y_test = train_test_split(
    X, Y,
    test_size=0.1,
    random_state=82,
    shuffle=True
)


rfr_pip = Pipeline([
    #("standardizer", StandardScaler()),
    ("rfr", RandomForestRegressor())
])

param_range = [i for i in range(50,101)]
grid_params = [{"rfr__n_estimators" : param_range}]

grid = GridSearchCV(
    rfr_pip, 
    grid_params,
    n_jobs=-1, 
    cv=5
)
grid.fit(x_train, y_train)



# obtaining the best estimator from grid
rfr = grid.best_estimator_
rfr.fit(x_train, y_train)

y_pred = rfr.predict(x_test)
print("Test Accuracy : {:.3f}".format(r2_score(y_test, y_pred)))


# By Sina Kazemi
# Github : https://github.com/sina96n/