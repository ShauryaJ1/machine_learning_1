import csv
import sys; args = sys.argv[1:]
with open(args[0]) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
with open(args[1]) as f:
    reader = csv.reader(f)
    test_data = [row for row in reader]
table = dict()
for i in range(0,8):
    sub_table = {0:{0:0,1:0},1:{0:0,1:0},2:{0:0,1:0},3:{0:0,1:0}}
      
    for row in data:
            sub_table[int(row[i])][int(row[-1])] += 1
    table[i] = sub_table
accuracy_table = {k:0 for k in range(0,8)}
for k in table:
    correct = 0
    for row in data:
        if table[k][int(row[k])][0] > table[k][int(row[k])][1]:
            if int(row[-1]) == 0:
                correct += 1
        else:
            if int(row[-1]) == 1:
                correct += 1

    accuracy_table[k] = correct/len(data)
print(accuracy_table)
best_attribute = max(accuracy_table, key=accuracy_table.get)
print(f"Best attribute: {best_attribute}")
rule_table = {k:0 for k in table[best_attribute]}
for k in table[best_attribute]:
    rule_table[k] = max(table[best_attribute][k], key=table[best_attribute][k].get)
print(rule_table)
correct = 0
for row in test_data:
    if int(row[-1]) == rule_table[int(row[best_attribute])]:
        correct += 1
        # print(f"Incorrectly classified {row}")
print(f"Accuracy: {correct/len(test_data)}")