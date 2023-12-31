from algorithm import algorithms
import choose_classifier
from choose_classifier import getResult
from choose_classifier import features
import pickle
# from sklearn.externals import joblib
import joblib

results = {}
print("\nNow testing algorithms")
for algo in algorithms:
    clf, score = getResult(algo)
    print("%s : %f %%" % (algo, score*100))
    results[algo] = score

winner = max(results, key=results.get)
print('\nWinner algorithm is %s with a %f %% success' % (winner, results[winner]*100))

# Save the algorithm and the feature list for later predictions
print('Saving algorithm and feature list in classifier directory...')
joblib.dump(algorithms[winner], 'classifier_new/classifier.pkl')#Persist an arbitrary Python object into one file.
open('classifier_new/features.pkl', 'w').write(pickle.dumps(features))
#joblib works especially well with NumPy arrays which are used by sklearn so depending on the classifier type you use you might have performance and size benefits using joblib.Otherwise pickle does work correctly so saving a trained classifier and loading it again will produce the same results no matter which of the serialization libraries you use
print(features)

# # Identify false and true positive rates
# clf = algorithms[winner]
# res = clf.predict(X_test)
# mt = confusion_matrix(y_test, res)
# #A confusion matrix, also known as an error matrix,[4] is a specific table layout that allows visualization of the performance of an algorithm, typically a supervised learning.
# print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
# print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))