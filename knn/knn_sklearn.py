from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

train_data = pd.read_csv('../iris_train.csv')
test_data = pd.read_csv('../iris_test.csv')
knn = KNeighborsClassifier(n_neighbors=1)

X_train = train_data.drop('Species', axis=1)
y_train = train_data['Species']
X_test = test_data.drop('Species', axis=1)
y_test = test_data['Species']

knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print("\n------------------------------------------\n")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred),'------------------------------------------')
print("\n------------------------------------------\n")
