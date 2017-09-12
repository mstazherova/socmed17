# Python 3.6
# Author: Maximilian Seidler
# Reads CSV-file and performs various classifications

import csv
import time
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier


def read_data(filepath):
    """Given a filepath to a CSV-file, this function reads in data 'X' and
    labels 'y' and returns them."""
    X = []
    y = []
    debug = True
    counter = 0
    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            y.append(row[0])
            X.append(row[1:][0])
            counter += 1
            if debug and counter == 10000:
                break
    return (X, y)


def print_emotion_frequency(y):
    c = Counter(y)
    print(c.most_common())


def classifiers(X_train, y_train, X_test, y_test, classifiers):
    for classifier in classifiers:
        start_time = time.time()
        clf = classifier
        clf.fit(X_train, y_train)
        print("{} completed in {:.2f} seconds".format(type(clf).__name__, (time.time() - start_time)))
        # print("Cross-validated accuracy: {:.2f}".format(cross_val_score(clf, X_test, y_test, scoring='accuracy').mean()))
        print("Accuracy: {}".format(clf.score(X_test, y_test)))
        print()


if __name__ == "__main__":
    X, y = read_data('../data/corpus.csv')
    # vectorization
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2))
    X_vec_counts = vectorizer.fit_transform(X)
    # from counts to term frequencies
    # (idf is unneccesary as we have only one document class)
    tfidf_transformer = TfidfTransformer(use_idf=False)
    X_vec_freq = tfidf_transformer.fit_transform(X_vec_counts)
    # split into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X_vec_freq, y, test_size=0.2, random_state=42)
    print("Data reading complete!")
    print_emotion_frequency(y)
    # classfication
    clf_list = [MultinomialNB(),
                LinearSVC(),
                DecisionTreeClassifier(criterion='entropy', random_state=42),
                RandomForestClassifier(criterion='entropy', n_estimators=3),
                LogisticRegression(random_state=42)]

    clf_names = []
    for clf in clf_list:
        clf_names.append(type(clf).__name__)
    voting = [VotingClassifier(list(zip(clf_names, clf_list)))]

    classifiers(X_train, y_train, X_test, y_test, clf_list)
    classifiers(X_train, y_train, X_test, y_test, voting)
