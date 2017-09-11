# Python 3.6
# Authors: Maximilian Seidler, Mariia Stazherova
# Reads CSV-file and performs various classifications

import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


def read_data(filepath):
    """Given a filepath to a CSV-file, this function reads in data 'X' and
    labels 'y' and returns them."""
    y = []
    X = []
    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            y.append(row[0][0])
            X.append(row[1:][0])
    return (X, y)


def naive_bayes(X_train, y_train, X_test, y_test):
    # Naive Bayes
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    print(clf.score(X_test, y_test))


def svm(X_train, y_train, X_test, y_test):
    # (kernel) SVM
    classifier_rbf = SVC()
    classifier_rbf.fit(X_train, y_train)
    print(classifier_rbf.score(X_test, y_test))


if __name__ == "__main__":
    X, y = read_data('../data/corpus.csv')

    # data transformation
    vectorizer = CountVectorizer()
    X_train_counts = vectorizer.fit_transform(X)

    tfidf_transformer = TfidfTransformer(use_idf=False)
    X_train = tfidf_transformer.fit_transform(X_train_counts)
    y_train = y
    X_test = X_train[:1000]
    y_test = y_train[:1000]

    # classfication
    naive_bayes(X_train, y_train, X_test, y_test)

    # runs forever right now...
    # svm(X_train, y_train, X_test, y_test)
