import csv
import random
import sys; args = sys.argv[1:]
split = float(args[0])
with open("../oneR_discretized.csv") as f:
    reader = csv.reader(f)
    data = [row for row in reader][1:]
    negative = [row for row in data if row[-1] == "0"]
    positive = [row for row in data if row[-1] == "1"]
    random.shuffle(negative)
    random.shuffle(positive)
    negative_split = int(len(negative)*split)
    positive_split = int(len(positive)*split)
    train = negative[:negative_split] + positive[:positive_split]
    test = negative[negative_split:] + positive[positive_split:]
    random.shuffle(train)
    random.shuffle(test)
with open("../oneR_train.csv", "w",newline='') as f:
    writer = csv.writer(f)
    # writer.writerow([f"Attribute {i}" for i in range(0, len(data[0]))])
    for row in train:
        writer.writerow(row)
with open("../oneR_test.csv", "w",newline='') as f:
    writer = csv.writer(f)
    # writer.writerow([f"Attribute {i}" for i in range(0, len(data[0]))])
    for row in test:
        writer.writerow(row)