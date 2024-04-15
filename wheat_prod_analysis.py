from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import pandas as pd

print("preprocessing")

base_path = "/Users/lincolnbay/Desktop/484_feat"
labeled_data = "/Users/lincolnbay/Desktop/484_feat/to_include/wheat_prod_labeled.csv"
unlabeled_data = "/Users/lincolnbay/Desktop/484_feat/to_include/wheat_prod_unlabeled.csv"

wheat = pd.read_csv(labeled_data)
y = wheat['logwheatprod']
X = wheat.loc[:,[j for j in wheat.columns if j not in ('logwheatprod', 'wheatprod', 'countycode','county27','year5','county')]]
wheat_unlabeled = pd.read_csv(unlabeled_data)
X_unlabeled = wheat_unlabeled.loc[:,[j for j in wheat.columns if j not in ('logwheatprod', 'wheatprod', 'countycode','county27','year5','county')]]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("fitting and validating")

ela = ElasticNet()
parameters = {'alpha':[.01,.05,.1,.5,1,1.5,2,5,10],'l1_ratio':[.01,.05,.1,.2,.3,.5,.7,.9,.99,1],'max_iter':[100000]}
classi = GridSearchCV(ela, parameters)
classi.fit(X_train_scaled, y_train)

X_unlabeled_scaled = scaler.transform(X_unlabeled)
y_pred = classi.predict(X_unlabeled_scaled)
# y_pred_series = pd.Series(y_pred)
unlabeled_finished = X_unlabeled.copy()
unlabeled_finished['logwheatprod'] = y_pred

print(f'training set accuracy: {classi.score(X_train_scaled,y_train)}')
print(f'test set accuracy: {classi.score(X_test_scaled,y_test)}')

best_params = classi.best_params_
scaler_final = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)
ela_final = ElasticNet(alpha=best_params['alpha'],l1_ratio=best_params['l1_ratio'],max_iter=100000)
ela_final.fit(X_scaled, y)
y_final_pred = ela_final.predict(X_unlabeled_scaled)
# y_final_pred_series = pd.Series(y_final_pred)
unlabeled_finished_final = X_unlabeled.copy()
unlabeled_finished_final['logwheatprod'] = y_final_pred

unlabeled_finished.to_csv('/Users/lincolnbay/Desktop/484_feat/to_include/predicted_product_raw.csv')
unlabeled_finished_final.to_csv('/Users/lincolnbay/Desktop/484_feat/to_include/predicted_product_raw_full.csv')
