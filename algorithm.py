import sklearn.ensemble as ske
from sklearn import  tree, linear_model
from sklearn.naive_bayes import GaussianNB
#Algorithm comparison
algorithms = {
    "DecisionTree": tree.DecisionTreeClassifier(max_depth=50),
    #The max_depth parameter denotes maximum depth of the tree.

    "RandomForest": ske.RandomForestClassifier(n_estimators=50),#In case, of random forest, these ensemble classifiers are            the randomly created decision trees. Each decision tree is a single classifier and the target prediction is based on            the majority voting method.
    #n_estimators ==The number of trees in the forest.

    "GradientBoosting": ske.GradientBoostingClassifier(n_estimators=50),
    "AdaBoost": ske.AdaBoostClassifier(n_estimators=100),
    #Ada mean Adaptive
    #Both are boosting algorithms which means that they convert a set of weak learners into a single strong learner. They            both initialize a strong learner (usually a decision tree) and iteratively create a weak learner that is added to the            strong learner. They differ on how they create the weak learners during the iterative process.

    "GNB": GaussianNB()
    #Bayes theorem is based on conditional probability. The conditional probability helps us calculating the probability             that something will happen
}