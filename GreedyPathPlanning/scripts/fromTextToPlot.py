# opens a txt file with data like this:
# Time for epoch 4995 is 5.113535642623901 sec // gLoss: 2.5299394130706787 | dLoss: 0.48891374468803406
# Time for epoch 4996 is 5.114245653152466 sec // gLoss: 2.52972149848938 | dLoss: 0.5392293334007263
# Time for epoch 4997 is 5.11424446105957 sec // gLoss: 2.7987895011901855 | dLoss: 0.39265263080596924
# Time for epoch 4998 is 5.114327669143677 sec // gLoss: 3.0322325229644775 | dLoss: 0.2981226444244385
# Time for epoch 4999 is 5.115389108657837 sec // gLoss: 3.271099090576172 | dLoss: 0.2446509748697281
# Time for epoch 5000 is 5.113909006118774 sec // gLoss: 3.418112277984619 | dLoss: 0.19863002002239227

# and plots the data in a graph

import matplotlib.pyplot as plt
import numpy as np

# open the file
f = open("output.txt", "r")

# read the file
lines = f.readlines()

# close the file
f.close()

# create the lists
gLoss = []
dLoss = []
time = []

# iterate through the lines
for line in lines:
    # split the line
    splitLine = line.split(" ")
    # append the values to the lists
    gLoss.append(float(splitLine[9]))
    dLoss.append(float(splitLine[12]))
    time.append(float(splitLine[3]))

# create the plot
plt.plot(time, gLoss, label="gLoss")
plt.plot(time, dLoss, label="dLoss")

# add the labels
plt.xlabel("Epoch")
plt.ylabel("Loss")

# add the legend
plt.legend()

# show the plot
plt.show()
