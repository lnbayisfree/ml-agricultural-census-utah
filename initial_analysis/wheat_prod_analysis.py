# Import relevant packages
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import pandas as pd

# Store the paths to the data
base_path = "/Users/lincolnbay/Desktop/484_feat"
labeled_data = f"{base_path}/initial_analysis/wheat_prod_labeled.csv"
unlabeled_data = f"{base_path}/initial_analysis/wheat_prod_unlabeled.csv"

# Load the data
wheat = pd.read_csv(labeled_data)
wheat_unlabeled = pd.read_csv(unlabeled_data)

# Establish outcome variable and features
y = wheat['logwheatprod']
X = wheat.loc[:,[j for j in wheat.columns if j not in ('logwheatprod', 'wheatprod', 'countycode','county27','year5','county')]]
X_unlabeled = wheat_unlabeled.loc[:,[j for j in wheat.columns if j not in ('logwheatprod', 'wheatprod', 'countycode','county27','year5','county')]]

# Split the labeled data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Scale test and training data based on training data means and standard deviations
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train and use cross-validation to select parameters for an Elastic Net model
ela = ElasticNet()
parameters = {'alpha':[.01,.05,.1,.5,1,1.5,2,5,10],'l1_ratio':[.01,.05,.1,.2,.3,.5,.7,.9,.99,1],'max_iter':[100000]}
classi = GridSearchCV(ela, parameters)
classi.fit(X_train_scaled, y_train)

# Predict results for missing values
X_unlabeled_scaled = scaler.transform(X_unlabeled)
y_pred = classi.predict(X_unlabeled_scaled)

# Recombine all the data
unlabeled_finished = X_unlabeled.copy()
unlabeled_finished['logwheatprod'] = y_pred
unlabeled_finished['county'] = wheat_unlabeled['county']
labeled_finished = X.copy()
labeled_finished['logwheatprod'] = y
labeled_finished['county'] = wheat['county']
full_data = pd.concat([unlabeled_finished,labeled_finished])

# Report training and test set accuracy
print(f'training set accuracy: {classi.score(X_train_scaled,y_train)}')
print(f'test set accuracy: {classi.score(X_test_scaled,y_test)}')
print(classi.best_params_)

# Fit a new model with the previously selected parameters and identical process on the whole labeled dataset instead of only on the training set
best_params = classi.best_params_
scaler_final = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)
ela_final = ElasticNet(alpha=best_params['alpha'],l1_ratio=best_params['l1_ratio'],max_iter=100000)
ela_final.fit(X_scaled, y)

# Predict the results based on the whole labeled dataset
y_final_pred = ela_final.predict(X_unlabeled_scaled)

# Recombine data
unlabeled_finished_final = X_unlabeled.copy()
unlabeled_finished_final['logwheatprod'] = y_final_pred
unlabeled_finished_final['county'] = wheat_unlabeled['county']
full_data_final = pd.concat([unlabeled_finished_final,labeled_finished])

# Export data: the first are the results based on only the training set; THESE ARE THE RESULTS WE REPORT.
full_data.to_csv(f'{base_path}/to_include/predicted_product_raw.csv')

# This data is EXTRA; it follows an identical process, but to increase accuracy, it includes the entire labeled dataset
full_data_final.to_csv(f'{base_path}/to_include/predicted_product_raw_full.csv'
