import csv
with open("../oneR_discretized.csv") as f:
    reader = csv.reader(f)
    data = [row for row in reader][1:]
    print(data[1])
count_classes = {i:{0:[],1:[],2:[],3:[]} for i in range(0, len(data[0]))}
count_classes[len(data[0])-1] = {0:[],1:[]}
print(count_classes)
for row in data:
    for i, v in enumerate(row):
        count_classes[i][int(v)].append(v)
print({k: {kk: len(vv) for kk, vv in v.items()} for k, v in count_classes.items()})