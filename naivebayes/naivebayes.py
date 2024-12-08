import csv
import sys; args = sys.argv[1:]
def get_prob(data, attribute, value, class_value):
    count = 0
    class_count = 0
    for row in data:
        if row[attribute] == value and row[-1] == class_value:
            count += 1
        if row[-1] == class_value:
            class_count += 1
    return count/class_count
def get_prob_from_table(attribute_table,class_table, row,class_value):
    prob = class_table[class_value]
    for i, value in enumerate(row[:-1]):
        prob *= attribute_table[str(i)][value]
    return prob
with open(args[0]) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
with open(args[1]) as f:
    reader = csv.reader(f)
    test_data = [row for row in reader]
num_classes = set([row[-1] for row in data])
probability_table = {str(i):dict() for i in range(len(num_classes))}
for attribute in range(0,len(data[0])-1):
    for class_value in num_classes:
        sub_table = dict()
        attribute_values = set([row[attribute] for row in data])
        for value in attribute_values:
            sub_table[value] = get_prob(data, attribute, value, class_value)
        probability_table[class_value][str(attribute)] = sub_table
print(f"probability table: {probability_table}")
class_table = {k:sum([1 for row in data if row[-1]==k])/len(data) for k in num_classes}
correct=0
true_positives = 0
false_positives = 0
false_negatives = 0
true_negatives = 0
for row in test_data:
    class_probabilities = dict()
    for class_value in num_classes:
        class_probabilities[class_value] = get_prob_from_table(probability_table[class_value], class_table, row, class_value)
    if row[-1] == max(class_probabilities, key=class_probabilities.get):
        correct += 1
        if row[-1] == '1':
            true_positives += 1
        else:
            true_negatives += 1
    else:
        if row[-1] == '1':
            false_negatives += 1
        else:
            false_positives += 1
print(correct/len(test_data))

print(f"TP: {true_positives}\tFN: {false_negatives}")
print(f"FP: {false_positives}\tTN: {true_negatives}")
