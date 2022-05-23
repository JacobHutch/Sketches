class Statistician:
    def __init__(self,dictionary):
        self.dictionary = dictionary

    def compileReport(self,dice):
        report = {}

        counts = {0:0,1:0,2:0,3:0,4:0,5:0}
        for i in dice:
            counts[i] += 1

        currentPoints = 0
        remainingDice = 0
        for i in counts:
            currentPoints += max(0,counts[i] - 2)
            if counts[i] < 2:
                remainingDice += counts[i]



        report["Counts"] = counts
        report["CurrentPoints"] = currentPoints
        report["RemainingDice"] = remainingDice
        return report



dict = {0:"Knife",1:"Ladder",2:"Lantern",3:"Shovel",4:"Key",5:"Guard"}
dice = [1,1,3,4,5,5]
stat = Statistician(dict)
report = stat.compileReport(dice)
print(report)
