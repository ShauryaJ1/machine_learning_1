import csv
with open("../oneR.csv") as f:
    reader = csv.reader(f)
    data = [row for row in reader][1:]
    num_attributes = len(data[0])
    attribute_values = dict()
    for i in range(0, num_attributes):
        values = set([row[i] for row in data])
        attribute_values[i] = list(values)
discrete_table = {k: dict() for k in attribute_values}
# print(discrete_table)
for k in discrete_table:
    for v in attribute_values[k]:
        discrete_table[k][v] = attribute_values[k].index(v)
print(discrete_table)
with open("../oneR_discretized.csv", "w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow([f"Attribute {i}" for i in range(0, num_attributes)])
    for row in data:
        writer.writerow([discrete_table[i][v] for i, v in enumerate(row)])
print("Done")