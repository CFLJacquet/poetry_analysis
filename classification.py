from sklearn.model_selection import train_test_split
from poetry_analysis.utils.text import get_tfidf, load_json
from poetry_analysis.preprocessing import json_to_tfidf
from poetry_analysis.utils.text import get_json_dataframe
from sklearn import svm, tree
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier


tfidf = json_to_tfidf('./data/poems_text_anais.json')
ids_poems = get_json_dataframe(load_json('./data/poems_extracted.json'))['theme']

X_train, X_test, y_train, y_test = train_test_split(tfidf, ids_poems, shuffle=True, test_size=0.2)

clf_dict = {
    'svm': svm.SVC(),
    'sgd': SGDClassifier(loss='hinge'),
    'multinomial_nb': MultinomialNB(),
    'kneighbours': KNeighborsClassifier(n_neighbors=136),
    'bagging': BaggingClassifier(KNeighborsClassifier(n_neighbors=136), max_samples=0.5, max_features=0.5),
    'decision_tree': tree.DecisionTreeClassifier(),
    'random_forest': RandomForestClassifier(n_estimators=136, max_depth=None, min_samples_split=2, random_state=0),
    'adaboost': AdaBoostClassifier(n_estimators=136),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
}

predictions = []

for clf_name, clf in clf_dict.items():
    clf.fit(X_train, y_train)
    print(clf_name, clf.score(X_test, y_test))


# nearest neighbours classification