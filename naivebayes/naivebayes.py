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
    # print(class_table)
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
# print(probability_table['0'])
# print(probability_table.keys())
class_table = {k:sum([1 for row in data if row[-1]==k])/len(data) for k in num_classes}

# print(class_probabilities)
correct=0
for row in test_data:
    class_probabilities = dict()
    for class_value in num_classes:
        class_probabilities[class_value] = get_prob_from_table(probability_table[class_value], class_table, row, class_value)
    if row[-1] == max(class_probabilities, key=class_probabilities.get):
        correct += 1
print(correct/len(test_data))
