from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

train_data = pd.read_csv("../oneR_discretized.csv")
test_data = pd.read_csv("../oneR_discretized.csv")
one_level_tree = DecisionTreeClassifier(max_depth=1,random_state=42)
cols = ['preg', 'plas', 'pres', 'skin', 'insu', 'mass', 'pedi', 'age', 'class']

train_data.columns = cols
test_data.columns = cols

X_train = train_data.drop('class', axis=1)
y_train = train_data['class']
X_test = test_data.drop('class', axis=1)
y_test = test_data['class']

one_level_tree.fit(X_train, y_train)
y_pred = one_level_tree.predict(X_test)
print("ONE LEVEL TREE\n------------------------------------------\n")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred),'------------------------------------------')

feature_index = one_level_tree.tree_.feature[0]  
threshold = one_level_tree.tree_.threshold[0]
print(f"Feature index: {feature_index}")
print(f"Threshold: {threshold}")