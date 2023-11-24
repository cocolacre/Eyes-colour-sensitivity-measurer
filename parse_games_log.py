#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

data = []
with open("games_log.txt", "r") as fin:
	data = fin.readlines()

data = [list(line.split("', '")) for line in data]
l_deltas = [(item[8], item[9]) for item in data]
results = [(item[0].split("=")[1], item[1].split("=")[1].strip()) for item in l_deltas]
x1 = [({"Win":True, "Loss":False}[item[0]], float(item[1].replace("'",""))) for item in results]
x2 = [(item[0], str(item[1])+"00000") for item in x1]
x3 = [(item[0], item[1][0:4]) for item in x2]
x4 = [(item[0], float(item[1])) for item in x3]

#
x5_t = [item[1] for item in x4 if item[0] == True]
x5_f = [item[1] for item in x4 if item[0] == False]

#def between(value, _min, _max):
#    return value >= _min and value < _max

between = lambda value, _min, _max : value >= _min and value < _max

#lets  clusterize...
x6_1 = [(item[1], item[0]) for item in x4 if between(item[1], 0.0, 4)]
x6_2 = [(item[1], item[0]) for item in x4 if between(item[1], 4, 8)]
x6_3 = [(item[1], item[0]) for item in x4 if between(item[1], 8, 12)]
x6_4 = [(item[1], item[0]) for item in x4 if between(item[1], 12, 16)]
x6_5 = [(item[1], item[0]) for item in x4 if between(item[1], 16, 22)]
x6_6 = [(item[1], item[0]) for item in x4 if between(item[1], 22, 28)]
x6_7 = [(item[1], item[0]) for item in x4 if between(item[1], 28, 36)]
x6_8 = [(item[1], item[0]) for item in x4 if between(item[1], 36, 50)]

#lets count Losses in each group and divide by total items in group (loss ratio).
x7_1 = len([item for item in x6_1 if item[1] == False])/len(x6_1)
x7_2 = len([item for item in x6_2 if item[1] == False])/len(x6_2)
x7_3 = len([item for item in x6_3 if item[1] == False])/len(x6_3)
x7_4 = len([item for item in x6_4 if item[1] == False])/len(x6_4)
x7_5 = len([item for item in x6_5 if item[1] == False])/len(x6_5)
x7_6 = len([item for item in x6_6 if item[1] == False])/len(x6_6)
x7_7 = len([item for item in x6_7 if item[1] == False])/len(x6_7)
x7_8 = len([item for item in x6_8 if item[1] == False])/len(x6_8)

print(f"0 - 4:   {int(x7_1*100)}% errors     total items={len(x6_1)}")
print(f"4 - 8:   {int(x7_2*100)}% errors     total items={len(x6_2)}")
print(f"8 - 12:  {int(x7_3*100)}% errors     total items={len(x6_3)}")
print(f"12 - 16: {int(x7_4*100)}% errors     total items={len(x6_4)}")
print(f"16 - 22: {int(x7_5*100)}% errors     total items={len(x6_5)}")
print(f"22 - 28: {int(x7_6*100)}% errors     total items={len(x6_6)}")
print(f"28 - 36: {int(x7_7*100)}% errors     total items={len(x6_7)}")
print(f"36 - 50: {int(x7_8*100)}% errors     total items={len(x6_8)}")


print(f"0 - 4  : {int(x7_1*100)}     {len(x6_1)}")
print(f"4 - 8  : {int(x7_2*100)}     {len(x6_2)}")
print(f"8 - 12 : {int(x7_3*100)}     {len(x6_3)}")
print(f"12 - 16: {int(x7_4*100)}     {len(x6_4)}")
print(f"16 - 22: {int(x7_5*100)}     {len(x6_5)}")
print(f"22 - 28: {int(x7_6*100)}     {len(x6_6)}")
print(f"28 - 36: {int(x7_7*100)}     {len(x6_7)}")
print(f"36 - 50: {int(x7_8*100)}     {len(x6_8)}")