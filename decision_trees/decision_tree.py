import sys; args = sys.argv[1:]
import csv
import math
import random
import json 
def info(data,classes):
    # [class_values.count(c)/len(data)*math.log(class_values.count(c)/len(data),2) for c in classes]
    class_values = [row[-1] for row in data]
    class_infos = []
    for c in classes:
        if class_values.count(c) == 0:
            class_infos.append(0)
        else:
            class_infos.append(class_values.count(c)/len(data)*math.log(class_values.count(c)/len(data),2))
    return -1*sum(class_infos)
def splitinfo(data,classes,attribute):
    # return -1*sum([len([row for row in data if row[attribute]==a])/len(data)*math.log(len([row for row in data if row[attribute]==a])/len(data),2) for a in set([row[attribute] for row in data])])
    splitinfos = []
    for a in set([row[attribute] for row in data]):
        attribute_count = len([row for row in data if row[attribute]==a])
        if attribute_count == 0:
            splitinfos.append(0)
        else:
            splitinfos.append(attribute_count/len(data)*math.log(attribute_count/len(data),2))
    return -1*sum(splitinfos)
def gain(data,classes,attribute):
    info_one = info(data,classes)
    # print(info_one)
    sub_infos = []
    for a in set([row[attribute] for row in data]):
        sub_data = [row for row in data if row[attribute]==a]
        # print(info(sub_data,classes),a)     
        sub_infos.append(len(sub_data)/len(data)*info(sub_data,classes))
    return info_one - sum(sub_infos)
def build_tree(data,tree,attributes_used,classes):
    if len(data) == 0:
        return None
    if len(attributes_used) == len(data[0])-1:
        return max(set([row[-1] for row in data]),key=[row[-1] for row in data].count)
    if len(set(temp:=[row[-1] for row in data])) == 1:
        return temp[0]
    attributes_not_used = [i for i in range(len(data[0])-1) if i not in attributes_used]
    splitinfos = [splitinfo(data,classes,attribute) for attribute in attributes_not_used]
    if any([sinfo == 0 for sinfo in splitinfos]):
        best_attribute = max([(gain(data,classes,attribute),attribute) for attribute in attributes_not_used])[1]
    else:
         best_attribute = max([(gain(data,classes,attribute)/splitinfo(data,classes,attribute),attribute) for attribute in attributes_not_used])[1]
        #  print([(gain(data,classes,attribute)/splitinfo(data,classes,attribute),attribute) for attribute in attributes_not_used])
        
    # gain_ratios = [(gain(data,classes,attribute)/splitinfo(data,classes,attribute),attribute) for attribute in attributes_not_used]
    # best_attribute = max(gain_ratios)[1]
    # print(best_attribute)
    tree["Attribute "+str(best_attribute)] = {}
    # print(set([row[best_attribute] for row in data]))
    for a in set([row[best_attribute] for row in data]):
        sub_data = [row for row in data if row[best_attribute]==a]
        tree["Attribute "+ str(best_attribute)]["Value "+a] = build_tree(sub_data,{},attributes_used+[best_attribute],classes)
    return tree
def test_row_of_data(row,tree,data):
    # print(row)
    # print(tree)
    temp = tree.copy()
    class_values = list(set([row[-1] for row in data]))
    
    while type(temp) == dict:
        # print(temp)
        if "Attribute" in list(temp.keys())[0]:
            attribute = int(list(temp.keys())[0][-1])
            temp = temp[list(temp.keys())[0]]
            
            # print("Attribute",attribute)
        else:
            value = row[attribute]
            # print("Value",value)
            if "Value "+value in list(temp.keys()):
                temp = temp["Value "+value]
            else:
                # print("No value found")
                return random.choice(class_values)
    # print(temp)
    return temp

            



def main():
    # random.seed(2)
    train_filename = args[0]
    test_filename = args[1]
    with open(train_filename, 'r') as f:
        data = list(csv.reader(f))[1:]
    classes = list(set([row[-1] for row in data]))
    tree = build_tree(data,{},[],classes)
    print(tree)
    print("\n--------------------------------\n")
    with open(test_filename, 'r') as f:
        test_data = list(csv.reader(f))[1:]
    
    correct = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    for row in test_data:
        prediction = test_row_of_data(row,tree,data)
        if prediction == row[-1]:
            correct += 1
            if prediction == '1':
                true_positives += 1
            else:
                true_negatives += 1
        else:
            if prediction == '1':
                false_positives += 1
            else:
                false_negatives += 1
    accuracy = correct/len(test_data)
    print(f"Accuracy: {accuracy}")
    print(f"True positives: {true_positives}")
    print(f"False positives: {false_positives}")
    print(f"True negatives: {true_negatives}")
    print(f"False negatives: {false_negatives}")
    print("\n--------------------------------\n")
    print("Predictions for training data:")
    correct = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    for row in data:
        prediction = test_row_of_data(row,tree,data)
        if prediction == row[-1]:
            correct += 1
            if prediction == '1':
                true_positives += 1
            else:
                true_negatives += 1
        else:
            if prediction == '1':
                false_positives += 1
            else:
                false_negatives += 1
    accuracy = correct/len(data)
    print(f"Accuracy: {accuracy}")
    print(f"True positives: {true_positives}")
    print(f"False positives: {false_positives}")
    print(f"True negatives: {true_negatives}")
    print(f"False negatives: {false_negatives}")
    with open("diabetes_tree.json", 'w') as f:
        json.dump(tree, f,indent=3)


if __name__ == "__main__":
    main()

