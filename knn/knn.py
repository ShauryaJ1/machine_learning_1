import sys; args = sys.argv[1:]
import csv
import math
import random
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from tqdm.auto import tqdm
import time

def euclidean_distances(point,data):
    distances = []
    for row in data:
        distances.append((math.sqrt(sum([(float(row[i])-float(point[i]))**2 for i in range(len(row)-1)])),row[-1]))
    return distances
def test_k(train_data,test_data,k):
    num_distance_calcs = 0
    correct = 0
    
    for row in test_data:
        distances = euclidean_distances(row[:-1],train_data)
        num_distance_calcs += len(distances)
        top_k = sorted(distances)[:k]
        prediction = max(set([row[1] for row in top_k]),key=[row[1] for row in top_k].count)
        if prediction == row[-1]:
            correct += 1
    accuracy = correct/len(test_data)
    return accuracy,num_distance_calcs
def measure_num_distance_calcs(data, k_values):
    num_distance_calcs = []
    for k in tqdm(k_values,"progress"):
        accuracy,num_distance_calcs_k = test_k(data, data[:10], k)
        num_distance_calcs.append(num_distance_calcs_k)
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, num_distance_calcs, marker='o', label='Number of Distance Calculations')

    plt.title('Number of Distance Calculations vs. K Values')
    plt.xlabel('K Values')
    plt.ylabel('Number of Distance Calculations')
    plt.grid(True)
    plt.legend()

    plt.savefig("num_distance_calcs_vs_k_values.png", dpi=300, bbox_inches='tight')
    # plt.show()
def main():
    if args[0] == "distances":
        
        X, y = make_blobs(n_samples=1000, centers=3, n_features=2,
                        random_state=0)

        # Plot the blobs
        

# Show the plot
        X = X.tolist()
        y = y.tolist()
        data = [X[i]+[y[i]] for i in range(len(X))]
        measure_num_distance_calcs(data, range(1, 1001))
    if len(args) != 3: # BLOB EXPERIMENTS, Parts 4 and 5
        X, y = make_blobs(n_samples=200, centers=3, n_features=2,
                        random_state=0)

        # Plot the blobs
        

# Show the plot
        X = X.tolist()
        y = y.tolist()
        X += [[random.uniform(-5, 5), random.uniform(-5, 5)] for _ in range(50)]
        y += [random.choice([0, 1, 2]) for _ in range(50)]
        data = [X[i]+[y[i]] for i in range(len(X))]
        plt.figure(figsize=(8, 6))
        plt.scatter([x[0] for x in X], [x[1] for x in X], c=y, cmap='viridis', s=50, edgecolor='k')

        # Customizing the plot
        plt.title('Blobs Visualization')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.grid(True)
        plt.savefig("blobs_visualization.png", dpi=300, bbox_inches='tight')
        train_percent = 0.8
        random.shuffle(data)
        train_data = data[:int(len(data)*train_percent)]
        test_data = data[int(len(data)*train_percent):]
        k_values = range(1, 51)
        accuracy_values = [test_k(train_data, test_data, k)[0] for k in k_values]
        plt.figure(figsize=(8, 6))
        plt.plot(k_values, accuracy_values, marker='o', label='Accuracy')

        plt.title('Accuracy vs. K Values')
        plt.xlabel('K Values')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)  
        plt.grid(True)
        plt.legend()

        plt.savefig("accuracy_vs_k_values.png", dpi=300, bbox_inches='tight')

    else: # REGULAR KNN TESTS WITH CSV FILES, IRIS AND OTHERS, Parts 1 and 3

        train_file = args[0]
        test_file = args[1]
        k = int(args[2])
        with open(train_file,'r') as file:
            train_data = [row for row in csv.reader(file)][1:]
        with open(test_file,'r') as file:
            test_data = [row for row in csv.reader(file)][1:]
        correct = 0
        
        for row in test_data:
            top_k = sorted(euclidean_distances(row[:-1],train_data))[:k]
            prediction = max(set([row[1] for row in top_k]),key=[row[1] for row in top_k].count)
            if prediction == row[-1]:
                correct += 1
        accuracy = correct/len(test_data)
        # print("True positives,",true_positives) 
        # print("False positives,",false_positives)
        # print("True negatives,",true_negatives)
        # print("False negatives,",false_negatives)
        print("Accuracy,",accuracy)
            
        k_values = range(1, 51)  
        accuracy_values = [test_k(train_data, test_data, k) for k in k_values]  

        plt.figure(figsize=(8, 6))
        plt.plot(k_values, accuracy_values, marker='o', label='Accuracy')

        plt.title('Accuracy vs. K Values')
        plt.xlabel('K Values')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)  
        plt.grid(True)
        plt.legend()

        plt.savefig("accuracy_vs_k_values.png", dpi=300, bbox_inches='tight')

    # plt.show()




if __name__ == '__main__':
    main()