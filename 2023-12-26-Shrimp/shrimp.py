import math,random



COLOR_DICT = {0:"pink",1:"red",2:"orange",3:"yellow",4:"green",5:"blue",6:"purple"}



def clamp(val,mn,mx):
    return min(max(val,mn),mx)





class Card():
    def __init__(self,colors):
        self.colors = colors
        self.color = self.colors[0]
        self.uColors = self.colors[1:]
        random.shuffle(self.colors)



    def print(self):
        for c in self.colors:
            print(COLOR_DICT[c]+" ", end="")
        print()



    def printShort(self):
        print(COLOR_DICT[self.color])





class Player():
    def __init__(self,pid,ai,hand,players,victoryCount,playerMap):
        self.pid = pid
        self.ai = ai
        self.hand = hand
        self.scoreCount = 0
        self.victory = False
        self.players = players
        self.victoryCount = victoryCount
        self.playerMap = playerMap



    def print(self):
        print("player "+str(self.pid)+", score: "+str(self.scoreCount))
        for c in self.hand:
            c.printShort()
        if len(self.hand) == 0:
            print("no cards")
        print()



    def scanHand(self,color):
        count = 0
        for c in self.hand:
            if c.color == color:
                count += 1
        return count



    def turn(self,top):
        if self.ai:
            self.aiTurn(top)
        else:
            self.pTurn(top)



    def aiTurn(self,top):
        c = self.getChoice(top)
        if c[0] == 0:
            self.scoreTurn(top)
        else:
            self.aiStealTurn(top,c[1])



    def getChoice(self,top):
        data = self.gatherData(top)

        return [0]



    def gatherData(self,top):
        data = []
        scoreData = []
        prob = 0
        for c in top.colors:
            if c in [t.color for t in self.hand]:
                scoreData.append(self.scanHand(c)+1)
                prob += 1
            else:
                scoreData.append(0)
        scoreData.append(prob/3)
        data.append(scoreData)

        for p in self.players:
            if p == self:
                continue
            stealData = [p.pid]
            prob = 0
            for c in top.colors:
                if c in [t.color for t in p.hand]:
                    stealData.append(p.scanHand(c)+1)
                    prob += 1
                else:
                    stealData.append(0)
            stealData.append(prob/3)
            data.append(stealData)
        return data



    def pTurn(self,top):
        while True:
            choice = input("score (1) or steal (2): ")
            try:
                choice = int(choice)
            except:
                print("bad input, try again")
                continue

            if choice == 1:
                self.scoreTurn(top)
                break
            if choice == 2:
                self.pStealTurn(top)
                break
            else:
                print("bad input, try again")



    def scoreTurn(self,top):
        print("player "+str(self.pid)+" attempts to score")
        print("top card is: "+COLOR_DICT[top.color])
        print()
        if self.scanHand(top.color) > 0:
            print("player "+str(self.pid)+" scores "+str(self.scanHand(top.color)+1)+" points! "+str(self.scoreCount)+" -> "+str(self.scoreCount+self.scanHand(top.color)+1))
            self.scoreCount += self.scanHand(top.color)+1
            newHand = []
            for c in self.hand:
                if c.color != top.color:
                    newHand.append(c)
            self.hand = newHand
            if self.scoreCount >= self.victoryCount:
                self.victory = True
        else:
            print("player "+str(self.pid)+" fails to score")
            self.hand.append(top)



    def aiStealTurn(self,top,choice):
        print("player "+str(self.pid)+" attempts to steal from player "+str(self.players[choice].pid))
        print("top card is: "+COLOR_DICT[top.color])
        print()
        if self.players[choice].scanHand(top.color) > 0:
            print("player "+str(self.pid)+" successfully steals from player "+str(self.players[choice].pid)+"!")
            for c in self.players[choice].hand:
                if c.color == top.color:
                    self.hand.append(c)
            self.hand.append(top)
            newHand = []
            for c in self.players[choice].hand:
                if c.color != top.color:
                    newHand.append(c)
            self.players[choice].hand = newHand
        else:
            print("player "+str(self.pid)+" fails to steal from player "+str(self.players[choice].pid))
            self.players[choice].hand.append(top)


    def pStealTurn(self,top):
        while True:
            choice = input("player to steal from (#): ")
            try:
                choice = int(choice)
                self.players[choice]
            except:
                print("bad input, try again")
                continue

            if choice == 0:
                print("bad input, try again")
                continue
            else:
                self.aiStealTurn(top,choice)
                break





class Game():
    def __init__(self):
        pass



    def print(self):
        for i in range(40):
            print("=",end="")
        print()
        print("round: "+str(self.roundCounter)+", player turn: "+str(self.playerTurn))
        print()
        for i in self.playerMap:
            self.players[i].print()
        print("top card:")
        self.deck[-1].print()
        print()



    def start(self,count,playerCount,pauses):
        self.deck = []
        self.players = []
        self.playerMap = {}
        order = []
        count = clamp(count,2,6)
        for p in range(count):
            order.append(p)
        random.shuffle(order)
        print("turn order: ",end="")
        for p in range(count):
            print(str(order[p])+" ",end="")
            self.playerMap[order[p]] = p
        print()

        for i in range(7):
            for j in range(7):
                if j == i:
                    continue
                for k in range(j+1,7):
                    if k == i:
                        continue
                    self.deck.append(Card([i,j,k]))

        random.shuffle(self.deck)

        if count == 2:
            victoryCount = 15
        else:
            victoryCount = 10
        for i in range(count):
            self.players.append(Player(i,True,[self.deck.pop() for x in range(4)],self.players,victoryCount,self.playerMap))

        for i in range(playerCount):
            self.players[i].ai = False

        self.loop(pauses)
        while True:
            input()



    def loop(self,pauses):
        self.roundCounter = 1
        while True:
            self.playerTurn = 0
            for i in self.playerMap:
                if len(self.deck) == 0:
                    print("deck is empty")
                    slist = []
                    top = -1
                    for p in self.players:
                        if p.scoreCount > top:
                            top = p.scoreCount
                            slist = []
                            slist.append(p)
                        elif p.scoreCount == top:
                            slist.append(p)
                    if len(slist) > 1:
                        clist = []
                        top = -1
                        for p in slist:
                            if len(p.hand) > top:
                                top = len(p.hand)
                                clist = []
                                clist.append(p)
                            elif len(p.hand) == top:
                                clist.append(p)
                        if len(clist) > 1:
                            print("tie between players: ",end="")
                            for p in clist:
                                print(str(p.pid)+" ",end="")
                            return
                        else:
                           print("player "+str(clist[0].pid)+" victory!")
                           return
                    else:
                        print("player "+str(slist[0].pid)+" victory!")
                        return
                p = self.players[i]
                self.playerTurn = p.pid
                self.print()
                p.turn(self.deck.pop())
                if p.victory:
                    print("player "+str(p.pid)+" victory!")
                    return
                if pauses:
                    input()
            self.roundCounter += 1





game = Game()
game.start(4,0,False)
