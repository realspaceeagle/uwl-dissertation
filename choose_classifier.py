import pandas as pd
import numpy as np
import pickle
import sklearn.ensemble as ske
from algorithm import algorithms
from sklearn import  tree, linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
data = pd.read_csv('./data/data.csv', sep='|')
X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values #now droping some coloumns as axis 1(mean coloumn) and will show the values in the rows
y = data['legitimate'].values #values of legitimate data

print('Researching important feature based on %i total features\n' % X.shape[1])# shape() is use in pandas to give number of row/column
newX = []
newY = []
for i in X:
    a1 = []
    flag = 1
    for j in i:
        try:
            k = (j)
            a1.append(k)
        except:
            flag = 0
            break
    if flag == 1:
        newX.append(a1)
for i in y:
    try:
        k = (i)
        newY.append(k)
    except:
        print('')
print(X)
# Feature selection using Trees Classifier
fsel = ske.ExtraTreesClassifier().fit(X, y)
# X = newX
# y = newY
model = SelectFromModel(fsel, prefit=True)
X_new = model.transform(X)#now features are only 9 :)
nb_features = X_new.shape[1]#will save value 13 as shape is (138047, 13) :}



X_train, X_test, y_train, y_test = train_test_split(X_new, y ,test_size=0.2)#now converting in training and testing data in 20% range
features = []

print('%i features identified as important:' % nb_features) #as mentioned above


#important features sored
indices = np.argsort(fsel.feature_importances_)[::-1][:nb_features]
for f in range(nb_features):
    print("%d. feature %s (%f)" % (f + 1, data.columns[2+indices[f]], fsel.feature_importances_[indices[f]]))

# mean adding to the empty 'features' array the 'important features'
for f in sorted(np.argsort(fsel.feature_importances_)[::-1][:nb_features]):#[::-1] mean start with last towards first
    features.append(data.columns[2+f])

def getResult(algo):
    print(algo)
    clf = algorithms[algo]
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    res = clf.predict(X_test)
    mt = confusion_matrix(y_test, res)
    print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
    print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))
    return clf,score
