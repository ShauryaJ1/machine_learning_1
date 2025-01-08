import csv
import random
import sys; args = sys.argv[1:]

def make_train_test_split(data_file, train_file, test_file, train_percent):
    with open(data_file, 'r') as file:
        data = [row for row in csv.reader(file)]
        header= data[0]
        data = data[1:]
    random.shuffle(data)
    d = dict()
    for row in data:
        if row[-1] not in d:
            d[row[-1]] = []
        d[row[-1]].append(row)
    train_data = [header] + []
    test_data = [header] + []
    for key in d:
        random.shuffle(d[key])
        split = int(len(d[key]) * train_percent)
        train_data += d[key][:split]
        test_data += d[key][split:]
    with open(train_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])
        writer.writerows(train_data)
    with open(test_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])
        writer.writerows(test_data)
def main():
    make_train_test_split(args[0], args[1], args[2], float(args[3]))

if __name__ == '__main__': main()