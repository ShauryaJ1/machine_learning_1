import csv
import sys; args = sys.argv[1:]
with open(args[0]) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
with open(args[1]) as f:
    reader = csv.reader(f)
    test_data = [row for row in reader]
table = dict()
num_attributes = len(data[0])-1
num_classes = len(set([row[-1] for row in data]))
sub_sub_table ={k:0 for k in range(num_classes)}
attribute_dict = {k:len(set([row[k] for row in data])) for k in range(num_attributes)}
for i in range(0,8):
    sub_table = {k:sub_sub_table.copy() for k in range(attribute_dict[i])}
      
    for row in data:
            sub_table[int(row[i])][int(row[-1])] += 1
    table[i] = sub_table
accuracy_table = {k:0 for k in range(0,num_classes)}
for k in table:
    correct = 0
    for row in data:
        if int(row[-1]) == max(table[k][int(row[k])], key=table[k][int(row[k])].get):
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
print(f"Accuracy: {correct/len(test_data)}")