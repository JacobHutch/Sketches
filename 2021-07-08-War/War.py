import random, time, math
import matplotlib.pyplot as plt

#random.seed(150)

def war():
    deck = []
    for x in range(2,15):
        deck.append(x)
        deck.append(x)
        deck.append(x)
        deck.append(x)
    random.shuffle(deck)

    p1 = deck[:26]
    p2 = deck[26:]
    p1o = []
    p2o = []

    turns = 0
    warDeath = False

    while True:
        if len(p1) > 0:
            p1c = p1.pop()
        elif len(p1o) > 0:
            random.shuffle(p1o)
            p1 = p1o
            p1c = p1.pop()
        else:
            winner = 1
            break

        if len(p2) > 0:
            p2c = p2.pop()
        elif len(p2o) > 0:
            random.shuffle(p2o)
            p2 = p2o
            p2c = p2.pop()
        else:
            winner = 2
            break

        if p1c > p2c:
            p1o.append(p1c)
            p1o.append(p2c)
        elif p1c < p2c:
            p2o.append(p1c)
            p2o.append(p2c)
        elif p1c == p2c:
            war = []
            while p1c == p2c:
                if (len(p1) < 4):
                    if (len(p1)+len(p1o) > 3):
                        random.shuffle(p1o)
                        p1 = p1o + p1
                    else:
                        warDeath = True
                        winner = 2
                        break
                if (len(p2) < 4):
                    if (len(p2)+len(p2o) > 3):
                        random.shuffle(p2o)
                        p2 = p2o + p2
                    else:
                        warDeath = True
                        winner = 1
                        break
                war.append(p1c)
                war.append(p2c)
                war.append(p1.pop())
                war.append(p1.pop())
                war.append(p1.pop())
                war.append(p2.pop())
                war.append(p2.pop())
                war.append(p2.pop())
                p1c = p1.pop()
                p2c = p2.pop()
                if p1c > p2c:
                    p1o.extend(war)
                    p1o.append(p1c)
                    p1o.append(p2c)
                    break
                elif p1c < p2c:
                    p2o.extend(war)
                    p2o.append(p1c)
                    p2o.append(p1c)
                    break

            if warDeath:
                break

        turns += 1

    return [winner,turns]

iterations = 10000
avg = 0
max = 0
min = math.inf
xplt = []
y1plt = []
y2plt = []
plt.axis("auto")
for i in range(iterations):
    warres = war()
    if warres[1] > max:
        max = warres[1]
    if warres[1] < min:
        min = warres[1]
    avg += warres[1]
    xplt.append(i)
    if warres[0] == 1:
        y1plt.append(warres[1])
        y2plt.append(0)
    else:
        y1plt.append(0)
        y2plt.append(warres[1])
avg = avg / iterations
plt.scatter(xplt,y1plt,1)
plt.scatter(xplt,y2plt,1)
plt.title("Average: "+str(avg)+"   Min/Max: "+str(min)+"/"+str(max))
plt.show()
