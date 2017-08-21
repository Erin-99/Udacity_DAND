#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'total_stock_value', 'expenses', 'exercised_stock_options', 'restricted_stock',  'from_messages','fraction_to_poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
#my_dataset = data_dict.pop('TOTAL')
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK') # Not a name
data_dict.pop('LOCKHART EUGENE E') # All data is NaN
my_dataset = data_dict
def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """


    ### you fill in this code, so that it returns either
    ###     the fraction of all messages to this person that come from POIs
    ###     or
    ###     the fraction of all messages from this person that are sent to POIs
    ### the same code can be used to compute either quantity

    ### beware of "NaN" when there is no known email address (and so
    ### no filled email features), and integer division!
    ### in case of poi_messages or all_messages having "NaN" value, return 0.
    if poi_messages == 'NaN' or all_messages == 'NaN':
        fraction = 0
    else:
        fraction = poi_messages *1.0 / all_messages



    return fraction

for name in my_dataset:
    data_point = my_dataset[name]
    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
    data_point["fraction_from_poi"] = fraction_from_poi
    
    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )

    data_point["fraction_to_poi"] = fraction_to_poi
    

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)

labels, features = targetFeatureSplit(data)

### feature scalling
from sklearn.preprocessing import MinMaxScaler
features = MinMaxScaler().fit_transform(features)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
#from sklearn.naive_bayes import GaussianNB
#from email_preprocess import preprocess
#clf = GaussianNB()
#features_train, features_test, labels_train, labels_test = preprocess()
#clf.fit(features_train,labels_train)
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
features_list = ['poi', 'total_stock_value', 'expenses', 'exercised_stock_options', 'restricted_stock',  'from_messages','fraction_to_poi']
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
features = MinMaxScaler().fit_transform(features)
param_grid = {'max_depth':[2,3,4,5,6,7,8],
          'min_samples_split': [2,5,8,10,12,15,20],
          'min_samples_leaf':[1,2,5,8,10],
          }
cv = StratifiedShuffleSplit(labels, 100, random_state = 42)

clf_grid = GridSearchCV(DecisionTreeClassifier(), param_grid=param_grid,cv=cv,scoring='f1')
clf_grid.fit(features,labels)
clf=clf_grid.best_estimator_

clf.feature_importances_
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)