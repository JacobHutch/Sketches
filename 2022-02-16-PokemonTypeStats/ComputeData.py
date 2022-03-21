def importCSV(fileName,includeHeader=False):
    nameFile = open(fileName)
    rows = []
    if not includeHeader:
        row = nameFile.readline()
    row = nameFile.readline()
    while row:
        strList = row.split(",")
        strList[-1] = strList[-1][:-1]
        rows.append(strList)
        row = nameFile.readline()
    nameFile.close()
    return rows

def compute():
    typeNames = importCSV("SourceData/types.csv")
    typeChart = importCSV("SourceData/type_efficacy.csv")

    outputChart = []

    #18 for gen 6+, 17 for gen 2-5, 15 for gen 1
    for i in typeChart:
        atk = int(i[0]) - 1
        dfn = int(i[1]) - 1
        out = [typeNames[atk][1],typeNames[dfn][1],str(int(i[2])/100)]
        outputChart.append(out)

    outFile = open("Data/Gen6+Chart.csv","w")
    outFile.write("attack,defend,value\n")
    for i in outputChart:
        outFile.write(",".join(i)+"\n")
    outFile.close()

compute()
