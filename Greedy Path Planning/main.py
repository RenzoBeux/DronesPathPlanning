from pathGenerator import runGreedy


if __name__ == "__main__":
    for k in range(70,100):
        for i in range(1, 10):
            runGreedy(i,k/100)