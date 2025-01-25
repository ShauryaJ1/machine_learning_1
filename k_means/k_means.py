import sys; args = sys.argv[1:]
import csv
import math
import random
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
import copy
from sklearn.datasets import make_blobs
def euclidean_distances(point,data):
    distances = []
    for row in data:
        distances.append(((math.sqrt(sum([(float(row[i])-float(point[i]))**2 for i in range(len(point))]))),row[-1]))
    return distances

def make_clusters(data, k_centroids, max_iterations):
    random.seed(0)
    centroid_positions = random.sample(data, k_centroids)
    centroid_positions = [row + [i] for i, row in enumerate(centroid_positions)]
    old_positions = []
    iterations = 0
    num_distance_calcs = 0
    data_with_clusters_assigned = [row + [random.choice([i for i in range(k_centroids)])] for row in data]
    new_data_with_clusters_assigned = [row + [random.choice([i for i in range(k_centroids)])] for row in data]
    while (
        iterations < max_iterations
        and centroid_positions != old_positions
        and not all(
            [
                row[-1] == new_row[-1]
                for row, new_row in zip(data_with_clusters_assigned, new_data_with_clusters_assigned)
            ]
        )
    ):
        data_with_clusters_assigned = copy.deepcopy(new_data_with_clusters_assigned)
        old_positions = copy.deepcopy(centroid_positions)

        for row in data_with_clusters_assigned:
            # if iterations>0:
            #     print("ROW",row,centroid_positions)
            #     break
            distances = euclidean_distances(row[:-1], centroid_positions)
            num_distance_calcs += len(centroid_positions)
            row[-1] = min(distances, key=lambda x: x[0])[1]

        for i in range(k_centroids):
            cluster = [row for row in data_with_clusters_assigned if row[-1] == i]
            if cluster:
                centroid_positions[i] = [
                    sum([row[j] for row in cluster]) / len(cluster)
                    for j in range(len(cluster[0]) - 1)
                ] + [i]

        # print(old_positions, centroid_positions, sep="\n------------\n")
        # print(data_with_clusters_assigned[:5])
        # print(new_data_with_clusters_assigned[:5])
        iterations += 1

    print(iterations)
    return data_with_clusters_assigned,num_distance_calcs,centroid_positions
def test_k_and_plot_num_distances(data, k_values, max_iterations):
    num_distance_calcs = []
    for k in tqdm(k_values,"progress"):
        data_with_clusters_assigned,num_distance_calcs_k ,centroid_positions= make_clusters(data, k, max_iterations)
        num_distance_calcs.append(num_distance_calcs_k)
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, num_distance_calcs, marker='o', label='Number of Distance Calculations')
    plt.title('Number of Distance Calculations vs. K Values')
    plt.xlabel('K Values')
    plt.ylabel('Number of Distance Calculations')
    plt.grid(True)
    plt.savefig("num_distance_calcs_vs_k.png", dpi=300, bbox_inches='tight')
def elbow_method(data, k_values, max_iterations):
    wss_values = []
    for k in k_values:
        data_with_clusters_assigned,num_distance_calcs,centroid_positions = make_clusters(data, k, max_iterations)
        k_wss_value = []
        for i in range(k):
            cluster = [row for row in data_with_clusters_assigned if row[-1] == i]
            k_wss_value.append(sum([sum([(row[j] - centroid_positions[i][j]) ** 2 for j in range(len(row) - 1)]) for row in cluster]))
        wss_values.append(sum(k_wss_value))
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, wss_values, marker='o', label='Within-Cluster Sum of Squares')
    plt.title('Within-Cluster Sum of Squares vs. K Values')
    plt.xlabel('K Values')
    plt.ylabel('Within-Cluster Sum of Squares')
    plt.grid(True)
    plt.savefig("wss_vs_k.png", dpi=300, bbox_inches='tight')
def main():
    random.seed(0)
    n_samples = int(args[3])
    n_features = 2
    centers = int(args[0]) 
    k = int(args[1])
    # print(k)
    cluster_std = 5.0  

    data, labels = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers,cluster_std=cluster_std)
    
    data = data.tolist()
    # data = [[random.uniform(-100, 100), random.uniform(-100, 100)] for _ in range(n_samples)]
    max_iterations = int(args[2])
    data_with_clusters_assigned,num_distance_calcs,_= make_clusters(data, k, max_iterations)

    plt.figure(figsize=(8, 6))
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'purple', 'orange', 'pink', 'brown', 'gray',"black","magenta","olive","lime","teal","navy","maroon","fuchsia","silver","white"]
    for i in range(k):
        cluster = [row for row in data_with_clusters_assigned if row[-1] == i]
        plt.scatter([row[0] for row in cluster], [row[1] for row in cluster], c=colors[i % len(colors)], s=50, edgecolor='k')
    plt.title('K-Means Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.grid(True)
    plt.savefig("k_means_clustering.png", dpi=300, bbox_inches='tight')
    k_values = range(1, 301)
    # test_k_and_plot_num_distances(data, k_values, max_iterations)
    # elbow_method(data, k_values, max_iterations)
if __name__ == "__main__":
    main()


    