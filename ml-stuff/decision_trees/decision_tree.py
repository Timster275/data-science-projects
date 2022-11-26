import pandas 
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
df = pandas.read_csv("ml-stuff/data.csv")
d = {'UK': 0, 'USA': 1, 'N': 2}
df['Nationality'] = df['Nationality'].map(d)
d = {'YES': 1, 'NO': 0}
df['Go'] = df['Go'].map(d)


features = ["Age", "Experience", "Rank", "Nationality", "Go"]
X = df[features]
y = df["Go"]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

tree.plot_tree(clf, feature_names=features, class_names=["NO", "YES"], filled=True)
plt.show()
