import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sb
import numpy as np
import sklearn.tree as tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

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
               "total_rev_hi_lim", "purpopse", "title", "purpose", "zip_code",
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
read_data = pd.read_csv('data.csv', na_values=['NA'], low_memory=False)
read_data["sub_grade"].replace(grade_dic, inplace=True)
read_data["home_ownership"].replace(home_ownership_dic, inplace=True)
read_data['home_ownership'] = pd.to_numeric(read_data['home_ownership'])
read_data.dropna()
TESTLIMIT = 0
TRAINLIMIT = 2000

# Columns to drop
cnt = 0
for key in read_data.keys():
    if key not in ignoredCols:
        col_list.append(key)
        cnt = cnt + 1

read_data = read_data[:TRAINLIMIT]
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
read_data.dropna()
train_read_data = read_data[0:TESTLIMIT]
test_read_data = read_data[TESTLIMIT:TRAINLIMIT]
train_raw_data = train_read_data[col_list]
test_raw_data = test_read_data[col_list]
train_data = train_raw_data.dropna()
test_data = test_raw_data.dropna()

# Removing Outliers (TODO)


# correlation matrix showing correlation co-effiecients 
'''corr_matrix = read_data.corr()
heatMap=sb.heatmap(corr_matrix, annot=True,  cmap="YlGnBu", annot_kws={'size':12})
heatmap=plt.gcf()
heatmap.set_size_inches(20,15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)'''

# Classification

all_inputs = read_data.drop(columns=["default_ind"])
all_labels = read_data['default_ind'].values

(training_inputs,
 testing_inputs,
 training_classes,
 testing_classes) = train_test_split(all_inputs, all_labels, test_size=0.25)


# Create the classifier
decision_tree_classifier = DecisionTreeClassifier()


#Find the best paramters

parameters = {'criterion': ['gini', 'entropy'],
              'max_depth': [ 2, 3, 4, 5, 10, 20, 30, 40, 50],
              'max_features': [1, 2, 3, 4, 6, 8, 12]
              }


cross_validation = StratifiedKFold(n_splits=10)

grid_search = GridSearchCV(decision_tree_classifier,
                           param_grid=parameters,
                           cv=cross_validation)


grid_search.fit(all_inputs, all_labels)
print('Best score: {}'.format(grid_search.best_score_)) #Score means accuracy
print('Best parameters: {}'.format(grid_search.best_params_))

with open('decision_tree.dot', 'w+') as out_file:
    out_file = tree.export_graphviz(grid_search.best_estimator_, out_file=out_file)


decision_tree_classifier = grid_search.best_estimator_
cv_scores = cross_val_score(decision_tree_classifier, all_inputs, all_labels, cv=cross_validation, scoring="accuracy")
print(cv_scores)
plt.hist(cv_scores)
plt.title('Average score: {}'.format(np.mean(cv_scores)))


print("Finished")
