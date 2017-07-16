daily_data (open/high... index date)

m1_datas = pd.DataFrame(index=daily_data.index)
for w in [5, 10, 20]:
    for c in comm_data.columns:
        m1_datas[c+'_win_'+str(w)] = comm_data[c] /(comm_data[c].rolloing(widnow=w).max() - comm_data[c].rolling(window=w).min())

# get the predicted value
m1_datas = m1_data.join(tech_data)
m1_datas = m1.datas.shift(1)
m1_datas['reg_target'] = daily_data['close']
m1_datas['clf_target'] = ((daily_data['close']) /daily_data['close'].shift(1))-1 > 0

m1_datas = m1_datas.dropna()
features = m1_datas.drop(['reg_target','clf_target','obv'], axis=1)
y = m1_datas['clf_target']

from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(features)
X = scaler.transform(features)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensembles import ExtraTreeClassifier

forest = ExtraTreeClassifier(n_estimator=250, random_state=0)

forest.fit(X,y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
# print feature ranking

for f in range(len(indices)):
    print("%d feature %s (%f)" % (f+1, features.columns[indices[f]], importances[indices[f]])

indices = indices[:20]

plt.figure(figsize = (16,9))
plt.bar(range(len(indices)),importances[indices], color='r', yerr=std[indices], align="center")
plt.xticks(range(len(indices)), indices)

start_test='2015-01-01'
X_train = features[features.index < start_test]
X_test = features[features.index >= start_test]
Y_train = y[y.index < start_test]
Y_test = y[y.index >= start_test]

from sklearn.ensemble import RandomForestClassifier

models = [{'LR', LogisticRegression()},
    {'LDA', LDA()},
    {"QDA", QDA()},
    {"LSVC", LinearSVC()},
    {"RSVM", SVC(C=100000)},
    {"RF", RandomForestClassifier(n_estimator=1000)}]


for m in models:
    m[1].fit(X_train, Y_train)
    pred = m[1].predict(X_test)
    print("%s:%0.3f" % (m[0], m[1].score(X_test,Y_test)))
    print("%s\n" % confusion_matrix(pred, Y_test))

from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor


# Grid Search
from sklearn.grid_search import GridSearchCV

tuned_parameter =[{'alpha':[1.2,1.1,1,0.9,0.8]}]

model = GridSearchCV(Ridge(), tuned_parameters, cv = 10))
model.fit(X_train,Y_train)
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print "R2 score", score

from sklearn.decomposition import PCA
pca = PCA(n_components = 100)
pca = pca.fit(X_train)
pca
X_train = pca.transform(X_train)
X_test = pca.transform(X_test)
