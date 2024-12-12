import sys; args = sys.argv[1:]
import csv
import math
import random
import time
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
        return random.choice(list(set([row[-1] for row in data])))
    if len(set(temp:=[row[-1] for row in data])) == 1:
        return temp[0]
    attributes_not_used = [i for i in range(len(data[0])-1) if i not in attributes_used]
    splitinfos = [splitinfo(data,classes,attribute) for attribute in attributes_not_used]
    if any([sinfo == 0 for sinfo in splitinfos]):
        best_attribute = max([(gain(data,classes,attribute),attribute) for attribute in attributes_not_used])[1]
    else:
         best_attribute = max([(gain(data,classes,attribute)/splitinfo(data,classes,attribute),attribute) for attribute in attributes_not_used])[1]
        
        
    # gain_ratios = [(gain(data,classes,attribute)/splitinfo(data,classes,attribute),attribute) for attribute in attributes_not_used]
    # best_attribute = max(gain_ratios)[1]
    # print(best_attribute)
    tree["Attribute "+str(best_attribute)] = {}
    # print(set([row[best_attribute] for row in data]))
    for a in set([row[best_attribute] for row in data]):
        sub_data = [row for row in data if row[best_attribute]==a]
        tree["Attribute "+ str(best_attribute)]["Value "+a] = build_tree(sub_data,{},attributes_used+[best_attribute],classes)
    return tree

def make_subsets(data, num_subsets):
    subsets = []
    attributes = [i for i in range(len(data[0])-1)]
    features = random.sample(attributes, 3)

    # print(attributes)
    for i in range(num_subsets):
        # print(features)
        features = random.sample(attributes, 3)
        subset = []
        for j in range(len(data)):
            row = random.sample(data, 1)[0]
            # print(row/)
            subset.append([row[feature] for feature in features]+[row[-1]])
        subsets.append((subset,features))
    # print([len(subset) for subset in subsets])
    return subsets
def build_forest(n_trees,data, num_subsets, classes):
    forest = []
    subsets = make_subsets(data, num_subsets)
    start_time = time.time()
    for i in range(n_trees):
        tree = {}
        subset,features = subsets[i]
        tree = build_tree(subset, tree, [], classes)
        forest.append((tree,features))
    print("Time taken to build forest:",time.time()-start_time)
    return forest
def test_tree_row(row,tree,data,features):
    # print(row)
    # print(tree)
    temp = tree.copy()
    class_values = list(set([row[-1] for row in data]))
    # print(features)
    feature_correction_dict = {i:features[i] for i in range(len(features))}
    while type(temp) == dict:
        # print(temp)
        if "Attribute" in list(temp.keys())[0]:
            attribute = feature_correction_dict[int(list(temp.keys())[0][-1])]
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
def test_forest_row(row,forest,data):
    predictions = []
    for tree,features in forest:
        predictions.append(test_tree_row(row,tree,data,features))
    return str(int(sum([int(p) for p in predictions])/len(predictions) > 0.5))
def main():

    # random.seed(42)
    n_trees = int(args[0])
    num_subsets = int(args[0])
    with open(args[1],'r') as file:
        data = [row for row in csv.reader(file)][1:]
    classes = list(set([row[-1] for row in data]))
    forest = build_forest(n_trees,data,num_subsets,classes)
    # print(forest)
    with open(args[2],'r') as file:
        test_data = [row for row in csv.reader(file)][1:]
    correct = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    for row in test_data:
        prediction = test_forest_row(row,forest,data)
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
    print("\n----------------------Test--------------------\n")
    print("Accuracy,",accuracy)
    print("True positives,",true_positives)
    print("False positives,",false_positives)
    print("True negatives,",true_negatives)
    print("False negatives,",false_negatives)
    print("\n------------------------------------------\n")
    print("Predictions for training data:")
    correct = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    for row in data:
        prediction = test_forest_row(row,forest,data)
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
    print("Accuracy,",accuracy)
    print("True positives,",true_positives)
    print("False positives,",false_positives)
    print("True negatives,",true_negatives)
    print("False negatives,",false_negatives)
    print("\n------------------------------------------\n")
    with open("buys_computer_forest.json",'w') as file:
        json.dump(forest,file,indent=4)
    
if __name__ == '__main__':
    main()