import pandas as pd
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

train_data = pd.read_csv("../oneR_discretized.csv")
test_data = pd.read_csv("../oneR_discretized.csv")
#preg,plas,pres,skin,insu,mass,pedi,age,class
cols = ['preg', 'plas', 'pres', 'skin', 'insu', 'mass', 'pedi', 'age', 'class']
train_data.columns = cols
test_data.columns = cols
X_train = train_data.drop('class', axis=1)
y_train = train_data['class']
X_test = test_data.drop('class', axis=1)
y_test = test_data['class']
gnb_model = GaussianNB()
gnb_model.fit(X_train, y_train)
y_pred = gnb_model.predict(X_test)
print("GNB MODEL\n------------------------------------------\n")
accuracy = accuracy_score(y_test, y_pred)
print(confusion_matrix(y_test, y_pred))
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred),'------------------------------------------')

mnb_model = MultinomialNB()
mnb_model.fit(X_train, y_train)
y_pred = mnb_model.predict(X_test)
print("MNB MODEL\n------------------------------------------\n")
accuracy = accuracy_score(y_test, y_pred)
print(confusion_matrix(y_test, y_pred))

print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred),'------------------------------------------')

bnb_model = BernoulliNB()
bnb_model.fit(X_train, y_train)
y_pred = bnb_model.predict(X_test)
print("BNB MODEL\n------------------------------------------\n")
accuracy = accuracy_score(y_test, y_pred)
print(confusion_matrix(y_test, y_pred))

print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred),'------------------------------------------')