import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sb
import numpy as np
import sklearn.tree as tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# This line tells the notebook to show plots inside of the notebook
# %matplotlib inline

### Cleaning Data

# List of columns to be ignored
col_list = []
ignoredCols = ["id", "member_id", "emp_title", "desc", "grade",
               "mths_since_last_delinq", "mths_since_last_record",
               "initial_list_status", "mths_since_last_major_derog",
               "annual_inc_joint", "dti_joint", "verification_status_joint",
               "open_acc_6m", "open_il_6m", "open_il_12m", "open_il_24m",
               "mths_since_rcnt_il", "total_bal_il", "il_util", "open_rv_12m",
               "open_rv_24m", "max_bal_bc", "all_util", "inq_fi", "total_cu_tl",
               "inq_last_12m", "next_pymnt_d", "tot_coll_amt", "tot_cur_bal",
               "total_rev_hi_lim", "purpose", "title", "zip_code",
               "addr_state", "verification_status", "pymnt_plan",
               "last_pymnt_d", "last_credit_pull_d",
               "application_type", "collections_12_mths_ex_med", "acc_now_delinq",
               "policy_code", "funded_amnt", "funded_amnt_inv", "out_prncp_inv",
               "total_pymnt_inv", "total_rec_prncp", "issue_d", "earliest_cr_line"]

grade_dic = {'A1':1, 'A2':2, 'A3':3, 'A4':4, 'A5':5,
             'B1':11, 'B2':12, 'B3':13, 'B4':14, 'B5':15,
             'C1':21, 'C2':22, 'C3':23, 'C4':24, 'C5':25,
             'D1':31, 'D2':32, 'D3':33, 'D4':34, 'D5':35,
             'E1':41, 'E2':42, 'E3':43, 'E4':44, 'E5':45,
             'F1':51, 'F2':52, 'F3':53, 'F4':54, 'F5':55,
             'G1':61, 'G2':62, 'G3':63, 'G4':64, 'G5':65,
             'H1':71, 'H2':72, 'H3':73, 'H4':74, 'H5':75}

home_ownership_dic = {'RENT': 0, 'MORTGAGE': 1, 'OWN': 2, "OTHER": 3, "NONE": 4, "ANY": 5}

# Reading the data
read_data = pd.read_csv('data.csv', na_values=['NA'], low_memory=False, nrows=30000)
read_data["sub_grade"].replace(grade_dic, inplace=True)
read_data["home_ownership"].replace(home_ownership_dic, inplace=True)
read_data['home_ownership'] = pd.to_numeric(read_data['home_ownership'])
read_data.dropna()

# Columns to drop
for key in read_data.keys():
    if key not in ignoredCols:
        col_list.append(key)
        
read_data = read_data[col_list]

### Cleaning data

# Cleaning term
mode=read_data['term'].mode()
read_data['term'].replace('[^0-9]',"",inplace=True,regex=True)
read_data['term']=read_data['term'].fillna(10)
convert_dict = {'term': int} 
read_data= read_data.astype(convert_dict)

# Cleaning emp_length
mode=read_data['emp_length'].mode()
read_data['emp_length'].replace('[^0-9]',"",inplace=True,regex=True)
read_data['emp_length']=read_data['emp_length'].fillna(10)
convert_dict = {'emp_length': int} 
read_data= read_data.astype(convert_dict)

# Diving data into two subsets so we can avoid overfitting
read_data = read_data[read_data["annual_inc"]<=2000000]
read_data.dropna()
read_data.dropna(how='any', inplace=True)

default_data = read_data.loc[read_data['default_ind'] == 1]
default_data.dropna()
LIMIT = len(default_data)
non_default_data = read_data.loc[read_data['default_ind'] == 0]
non_default_data.dropna()
non_default_data = non_default_data[:LIMIT]

read_data = pd.concat([default_data, non_default_data])

# Removing Outliers (TODO)


# correlation matrix showing correlation co-effiecients 
'''corr_matrix = read_data.corr()
heatMap=sb.heatmap(corr_matrix, annot=True,  cmap="YlGnBu", annot_kws={'size':12})
heatmap=plt.gcf()
heatmap.set_size_inches(20,15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

fig = px.scatter_matrix(read_data, dimensions=
['loan_amnt', 'sub_grade', 'annual_inc', 'installment', 'term', 'emp_length'],
labels={col:col.replace('_', ' ') for col in read_data.columns},           
height=900, color="default_ind", color_continuous_scale=px.colors.diverging.Tealrose)
fig.show()

import os

if not os.path.exists("images"):
    os.mkdir("images")

fig.write_image("images/outliers.png")'''

# Classification

all_inputs = read_data.drop(columns=["default_ind"])
all_labels = read_data['default_ind'].values

X_train, X_test, y_train, y_test = train_test_split(all_inputs, all_labels, test_size=0.25)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)


best_scores = {}
classifiers = {}

cross_validation = StratifiedKFold(n_splits=10)

# Decision Trees Algorithm
decision_tree_classifier = DecisionTreeClassifier()

parameter_grid = {'criterion': ['gini', 'entropy'],
              'max_depth': [ 2, 3, 4, 5, 10, 20, 30, 40, 50],
              'max_features': [1, 2, 3, 4, 6, 8, 12]
              }
    
grid_search = GridSearchCV(decision_tree_classifier,
                           parameter_grid,
                           scoring='precision_weighted',
                           cv=cross_validation)

grid_search.fit(X_train, y_train)
print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))


decision_tree_classifier = grid_search.best_estimator_
   
predictions_train = grid_search.predict(X_train)
predictions_test = grid_search.predict(X_test) 

print(classification_report(y_train, predictions_train, target_names=['PAID', 'DEFAULTED']))
print(classification_report(y_test, predictions_test, target_names=['PAID', 'DEFAULTED']))

classifiers['DecisionTrees'] = grid_search.best_estimator_
best_scores['DecisionTrees'] = grid_search.best_score_

cv_scores = cross_val_score(decision_tree_classifier, all_inputs, all_labels, cv=cross_validation, scoring="precision_weighted")
print(cv_scores)
plt.hist(cv_scores)
plt.title('Average score: {}'.format(np.mean(cv_scores)))

'''
knn_classifier = KNeighborsClassifier()

parameter_grid = {
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'n_neighbors' : [2, 4, 6, 8, 10],
    'leaf_size' : [10, 20, 30, 40, 50],
    'p': [1,2]
}

grid_search = GridSearchCV(knn_classifier, 
                    parameter_grid,
                    scoring='precision_weighted',
                    n_jobs=-1,
                    cv=10)


grid_search.fit(X_train, y_train)

print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))

predictions_train = grid_search.predict(X_train)
predictions_test = grid_search.predict(X_test)


print(accuracy_score(y_train, predictions_train))
print(accuracy_score(y_test, predictions_test))

print(confusion_matrix(y_train, predictions_train))
print(confusion_matrix(y_test, predictions_test))

print(classification_report(y_train, predictions_train, target_names=['PAID', 'DEFAULTED']))
print(classification_report(y_test, predictions_test, target_names=['PAID', 'DEFAULTED']))


parameters = [{'kernel': ['rbf', 'linear'], 'gamma': [1e-3, 1e-4], 'C': [0.01, 0.1, 1, 10, 100]}]

grid_search = GridSearchCV(SVC(random_state=1),
                    parameters,
                    n_jobs=4,
                    scoring='precision_weighted',
                    cv=5)

grid_search.fit(X_train, y_train)

print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))

classifiers['SVM'] = grid_search.best_estimator_
best_scores['SVM'] = grid_search.best_score_

predictions_train = grid_search.predict(X_train)
predictions_test = grid_search.predict(X_test)

print(confusion_matrix(y_train, predictions_train))
print(confusion_matrix(y_test, predictions_test))

print(classification_report(y_train, predictions_train, target_names=['PAID', 'DEFAULTED']))
print(classification_report(y_test, predictions_test, target_names=['PAID', 'DEFAULTED']))


mlp_classifier = MLPClassifier(random_state=1, max_iter=2000)


tuned_parameters = {'hidden_layer_sizes': [(32,), (64,)],
                    'activation': ['logistic','tanh'],
                    'solver': ['adam', 'sgd'], #'lbfgs'
                    'alpha': [0.0001, 0.05],
                    'learning_rate': ['constant','adaptive']}

grid_search = GridSearchCV(mlp_classifier, 
                    tuned_parameters,
                    scoring='precision_weighted',
                    n_jobs=-1,
                    cv=10)

grid_search.fit(X_train, y_train)

print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))

predictions_train = grid_search.predict(X_train)
predictions_test = grid_search.predict(X_test)

print(classification_report(y_train, predictions_train, target_names=['PAID', 'DEFAULTED']))
print(classification_report(y_test, predictions_test, target_names=['PAID', 'DEFAULTED']))


score_df = pd.DataFrame()
for name, score in best_scores.items():
    score_df = score_df.append(pd.DataFrame({'Score': [score], 'Classifier': [name]}))

ax = sb.barplot(x='Classifier', y='Score', data=score_df)
ax.set_title('Classifiers Best Accuracy Score')
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, horizontalalignment='right')  

clf_df = pd.DataFrame()
for name, clf in classifiers.items():
    clf_df = clf_df.append(pd.DataFrame({'precision_weighted': cross_val_score(clf, X_train, y_train, cv=StratifiedKFold(n_splits=10)),
                       'classifier': [name] * 10}))

ax = sb.boxplot(x='classifier', y='precision_weighted', data=clf_df)
ax.set_title('Classifiers Accuracy')
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, horizontalalignment='right')'''

print("Finished")