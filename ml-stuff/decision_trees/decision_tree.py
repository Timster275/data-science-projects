import pandas 
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

def train_split(X, y, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

df = pandas.read_csv("/Users/timrainer/Desktop/Work/streamlit-projects/ml-stuff/decision_trees/data.csv")
d = {'UK': 0, 'USA': 1, 'N': 2}
df['Nationality'] = df['Nationality'].map(d)
d = {'YES': 1, 'NO': 0}
df['Go'] = df['Go'].map(d)


features = ["Age", "Experience", "Rank", "Nationality", "Go"]
X = df[features]
y = df["Go"]

X_train, X_test, y_train, y_test = train_split(X, y)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

print("Accuracy: ", clf.score(X_test, y_test))



tree.plot_tree(clf, feature_names=features, class_names=["NO", "YES"], filled=True)
plt.show()
