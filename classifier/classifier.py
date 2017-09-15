# Python 3.6
# Author: Maximilian Seidler
# Reads CSV-file and performs various sentiment classifications

import itertools
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier


# Used classification algorithms for sentiment analysis
clf_list = [MultinomialNB(),
            LinearSVC(),
            LogisticRegression(random_state=42)
            #RandomForestClassifier(criterion='entropy', n_estimators=5)
            ]


def read_data(filepath):
    """Given a filepath to a CSV-file, this function reads in data 'X' and
    labels 'y' and returns them."""
    X = []
    y = []
    debug = True
    counter = 0
    with open(filepath, encoding='UTF-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            y.append(row[0])
            X.append(row[1:][0])
            counter += 1
            # limit data for testing
            if debug and counter == 100000:
                print(counter)
                break
    return (X, y)


def vectorize_data(X):
    """Given a list of sentences, this function returns a matrix of vectorized
    term frequencies."""
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2))
    X_vec_counts = vectorizer.fit_transform(X)
    # from counts to term frequencies
    # (idf is unneccesary as we have only one document class)
    tfidf_transformer = TfidfTransformer(use_idf=False)
    return tfidf_transformer.fit_transform(X_vec_counts)


def print_emotion_ratio(y):
    """This funciton prints the frequency and ratio of each of the labels
    (emotions) in the data."""
    c = Counter(y)
    print("Label distribution in the data:")
    for emotion, frequency in c.most_common():
        print("\t{}: {} ({:.2f}%)".format(emotion, frequency, frequency / len(y) * 100))
    print()


def essemble_classifier():
    """This function collects the names of the classifiers and passes them to
    the Voting Classifier. For consistency reasons, it returns a list with a
    single element (the VotingClassifier)."""
    clf_names = []
    for clf in clf_list:
        clf_names.append(type(clf).__name__)
    # the VotingClassifier expects a list of tuples in the format of
    # (name_of_classifier, classifier)
    return [VotingClassifier(list(zip(clf_names, clf_list)))]


def train_and_evaluate(X_train, y_train, X_test, y_test, classifiers):
    """Given a list of classifiers, this function trains each classifier with a
    training set and evaluates it with a test set."""

    for clf in classifiers:
        start_time = time.time()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        print("Training of {} completed in {:.2f} seconds".format(type(clf).__name__, time.time() - start_time))
        #print("AUC score: {}".format(roc_auc_score(y_test, clf.decision_function(X_test))))
        print("F1-score: {:.2f}".format(f1_score(y_test, y_pred, average='weighted')))
        # print("Accuracy: {:.2f}".format(clf.score(X_test, y_test)))
        print(classification_report(y_test, y_pred, target_names=list(set(y))))

        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_pred)
        # Print and plot confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes= set(y),
                              title='Confusion matrix '+str(type(clf).__name__))


def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.Greens):
    """
    This function prints and plots the confusion matrix
    without normalization and with some fancy stuff
    """
    print('Confusion matrix')
    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    # fancy coloring part, the higher the number - the saturated the color
    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.20)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# def cross_validated_scores(X, y, classifiers):
#     for clf in classifiers:
#         start_time = time.time()
#         print("{}".format(type(clf).__name__))
#
#         print("Cross-validated f1_weighted: {:.2f} (finished in {:.2f} seconds)"
#               .format(cross_val_score(clf, X, y, cv=5, scoring='f1_weighted').mean(),
#                       time.time() - start_time))
#         print()


if __name__ == "__main__":
    print("Processing data...")
    # read from corpus
    X, y = read_data('../data/corpus.csv')
    # vectorize data
    X_vec = vectorize_data(X)
    # split into train and test set (by enabling stratification we ensure that
    # the train and test sets have the same ratio of emotions)
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.1,
                                                        random_state=42, stratify=y)

    print("Data processing completed.")
    print_emotion_ratio(y)
    print("Training and evaluating classifiers:")
    # train and evaluate each of the classifiers
    train_and_evaluate(X_train, y_train, X_test, y_test, clf_list)
    # train and evaluate with an essemble method (using all of the classifiers)
    train_and_evaluate(X_train, y_train, X_test, y_test, essemble_classifier())

    # cross_validated_scores(X, y, clf_list)
    # cross_validated_scores(X, y, essemble_classifier())

    # actually show all the figures
    plt.show()

