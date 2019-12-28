import os


def enum(**named_values):
    return type('Enum', (), named_values)

#now you can use MaTypes.RalphStyle and MaTypes.NormalStyle
MaTypes = enum(RalphStyle = 1, NormalStyle = 2)

maType = MaTypes.RalphStyle # the default desired moving average type

#gets the users desired moving average type
def getMaType():
    ans = raw_input("What type of moving average? (r for RalphStyle, n for NormalStyle)  ")
    mtype = MaTypes.RalphStyle
    
    if ans == 'r':
        mtype = MaTypes.RalphStyle
    elif ans == 'n':
        mtype = MaTypes.NormalStyle
    else:
        print "BAD INPUT! Try Again"
        return getMaType()
    print "\n"
    
    return mtype

#asks the user how many number systems they want
def getSystems():
    systems = []
    cols = raw_input("How many systems/columns do you want? \n")
    try:
        cols = int(cols)
    except:
        print "BAD INPUT!"
        return getSystems()

    print "\n"
    for i in range(int(cols)):
        systems.append(getSysNumbers(i))

    return systems

#asks the user what numbers they want in a particular system
def getSysNumbers(sys):
    system = []
    val = 0
    while val is not 'q':
        val = raw_input("Enter numbers for system "+str(chr(sys+65)).lower()+"? (q to finish) ") #65 is ascii A
        if val is not 'q':
            try:
                system.append(int(val))
            except:
                print "BAD INPUT!"
    print "\n" 
    return system

#gets the indexes for which to run a versus system on
def getVsIndexes():
    input = raw_input("What columns do you want to play against each other? Example: xy \n")
    input = input.upper()
    parts = input.split(" ")
    if len(parts) == 1:
        teamA = ord(input[0])-65
        teamB = ord(input[1])-65
    elif len(parts) == 2:
        teamA = ord(parts[0])-65 #65 is ascii A
        teamB = ord(parts[1])-65 #65 is ascii A
    elif len(parts) != 2:
        print "BAD INPUT!\n"
        return getVsIndexes()
    return [teamA, teamB]

#gets the indexes to run a confirmation/agreement system on
def getConfirmationIndexes():
    input = raw_input("What columns do you want to confirm each other? Example: xy \n")
    input = input.upper()
    parts = input.split(" ")
    if len(parts) == 1:
        teamA = ord(input[0])-65
        teamB = ord(input[1])-65
    elif len(parts) == 2:
        teamA = ord(parts[0])-65 #65 is ascii A
        teamB = ord(parts[1])-65 #65 is ascii A
    elif len(parts) != 2:
        print "BAD INPUT!\n"
        return getConfirmationIndexes()
    return [teamA, teamB]

#gets an array of data from a particular file
def getData(filename = None):
    if filename is None:
        filename = raw_input("what data file do you want to use? \n")
    filename = filename.upper()
    filename += ".DAT"
    file_handle = open("C:/DOS_Program_Files/fib/"+filename, 'r')
    lines_list = file_handle.readlines()
    data = []
    for line in lines_list:
        data.append(int(line))
    print "\n"
    return data

#returns a collection of columns for each system
def calcSysCols(systems, data):
    cols = []
    for i in range(len(systems)):
        cols.append(calcSysCol(systems[i], data))
    return cols    

#given a list of number to comprise a system, calculates that systems column
def calcSysCol(sys, data):
    global maType
    col = [0] * len(data)
    for i in range(len(sys)):
        if maType == MaTypes.RalphStyle:
            numcol = calcNumColRalphsMA(sys[i], data)
        elif maType == MaTypes.NormalStyle:
            numcol = calculateNumColNormalMA(sys[i], data)
        for j in range(len(numcol)):
            col[j] += numcol[j]
    return col

#given a single number calculates the result of that number on the data
def calcNumColRalphsMA(num, data):
    part = num /2
    col = [0] * len(data)
    
    backsum = 0
    frontsum = 0
    transferNum = 0
    backnum = 0
    frontnum = 0
    for i in range(part):
        backsum += data[i]        #index 0 to 9 if num is 20
        frontsum += data[i+part]  #index 10 to 19 if num is 20

    #print "frontsum expecting 155: "+str(frontsum)
    #print "backsum expecting 55: "+str(backsum)
    #print "frontsum: "+str(frontsum)+", backsum: "+str(backsum)
    col[num - 1] = frontsum - backsum 
        
    #done using memoization:
    for i in range(num, len(data)):        #index 20 to 800
        backnum = data[i-num]              #remove index 0 
        #print "removing "+str(backnum)+" from backsum"
        backsum -= backnum
        transferNum = data[i - part]       #20 - 10 = index 10
        backsum += transferNum             #add index 10
        #print "adding "+str(transferNum)+" to backsum, removing from frontsum"
        frontsum -=transferNum             #remove index 10
        frontnum = data[i]
        frontsum += frontnum             #add index 20 
        #print "adding "+str(frontnum) +" to frontsum"
        #print "frontsum: "+str(frontsum)+", backsum: "+str(backsum)
        col[i] = frontsum - backsum
    return col   

#given a single moving average number calculates the result of that number on the data    
def calculateNumColNormalMA(num, data):
    col = [0] * len(data)
    sum = 0
    backnum = 0
    frontnum = 0
    
    for i in range(num):
        sum += data[i] #0 through 19 if the number is 20
        
    for i in range(num, len(data)):  #20 through the rest of the data indices
        backnum = data[i - num]      #remove index 0
        sum -= backnum

        frontnum = data[i]
        sum += frontnum              #add index 20
        col[i] =  data[i] - (sum/num)           #this ma vs todays close
        #col[i] = (sum/num)            #because regular moving average

    return col        

#prints a column
def printCol(col):
    for i in range(len(col)):
        print "inc "+str(i+1)+": "+str(col[i])

def printCols(data, cols, startInc = None):
    datastring = ""
    if startInc is None:
        for i in range(len(cols[0])):
            for j in range(len(cols)):
                datastring += "{0:10d}".format(cols[j][i])
            print "inc"+str(i+1)+", price="+str(data[i]).ljust(10)+datastring
            datastring = ""
    else:
        for i in range(startInc-1,startInc-1+48):
            if i < len(cols[0]):
                for j in range(len(cols)):
                    datastring += "{0:10d}".format(cols[j][i])
                print "inc"+str(i+1)+", price="+str(data[i]).ljust(10)+datastring
                datastring = ""

#given the system columns and teamA,teamB of vsIndexes, calculates a vs column
def calcVsCol(syscols, vsIndexes):
    #print "creating versus column for indexes "+str(vsIndexes[0])+" and "+str(vsIndexes[1])
    col = [0] * len(syscols[0])
    index1 = vsIndexes[0]
    index2 = vsIndexes[1]
    for i in range(len(syscols[0])):
        col[i] += syscols[index1][i]
        col[i] -= syscols[index2][i]
    return col

def calcConfCol(syscols, confIndexes):
    #print "calculating confirmation system on indexes: "+str(confIndexes[0])+" and "+str(confIndexes[1])
    col = [0] * len(syscols[0])
    for i in range(len(syscols[0])):
        if syscols[confIndexes[0]][i] < 0 and syscols[confIndexes[1]][i] < 0:
            col[i] = -1
        elif syscols[confIndexes[0]][i] > 0 and syscols[confIndexes[1]][i] > 0:
            col[i] = 1
        else:
            col[i] = 0
    return col

positions = {
    'long': 1, 
    'short': -1,
    'flat': 0}

stat = {
    'gt': 0,
    'trades': 1,
    'wins': 2,
    'losses': 3
}    
    
def printStats(stats):
    print "\n"
    banner = str("GRAND TOTAL:").ljust(26)
    for i in range(len(stats)):
        banner += str(stats[i][stat['gt']]).rjust(10)
    print banner
    
    banner = str("TRADE COUNT:").ljust(26)
    for i in range(len(stats)):
        banner += str(stats[i][stat['trades']]).rjust(10)
    print banner
    
    banner = str("WIN COUNT:").ljust(26)
    for i in range(len(stats)):
        banner += str(stats[i][stat['wins']]).rjust(10)
    print banner
    
    banner = str("LOSS COUNT:").ljust(26)
    for i in range(len(stats)):
        banner += str(stats[i][stat['losses']]).rjust(10)
    print banner
    
#gets a list of stats for every given column
def getAllStats(data, syscols):
    result = []
    for i in range(len(syscols)):
        result.append(getColStats(data, syscols, i))
    return result
    
#stats a particular column
def getColStats(data, syscols, sysindex):
    gt = 0
    tradeCount = 0
    winCount = 0
    lossCount = 0
    tieCount = 0
    position = positions['flat']
    positionPrice = 0
    price = 0
    winloss = 0
    linestring = ""
    for i in range(len(syscols[0])):
        price = data[i]
        linestring +="inc"+str(i+1)+", price="+str(data[i]).ljust(10)+", col: "+str(syscols[sysindex][i])+" "
        if(syscols[sysindex][i] > 0):
            if(position == positions['flat']):
                position = positions['long']
                positionPrice = price
            elif(position == positions['short']):
                #you've exited a short position
                winloss = positionPrice - price
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['long']
                positionPrice = price
                linestring += "long from short, winloss: "+str(winloss)
        elif(syscols[sysindex][i] < 0):
            if(position == positions['flat']):
                position = positions['short']
                positionPrice = price
            elif(position == positions['long']):
                #you've exited a long position
                winloss = price - positionPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['short']
                positionPrice = price
                linestring += "short from long, winloss: "+str(winloss)
        elif(syscols[sysindex][i] == 0):
            if(position == positions['long']):
                #you've exited a long position
                winloss = price - positionPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                linestring += "flat from long, winloss: "+str(winloss)
            elif(position == positions['short']):
                #you've exited a short position
                winloss = positionPrice - price
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                linestring += "flat from short, winloss: "+str(winloss)
            position = positions['flat']
            positionPrice = price
        #print linestring
        linestring = ""

    return [gt, tradeCount, winCount, lossCount]

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')    
    
def main(data):
    global maType
    maType = getMaType() #gets and sets the global moving average type
    systems = getSystems()
    syscols = calcSysCols(systems, data)

    count = 0
    doVersus = 'y'
    versusSystems = []
    while doVersus is 'y' or doVersus is not 'n':
        if doVersus is not 'y' and doVersus is not 'n':
            print "BAD INPUT!"
        a_another = "another" if count>0 else "a"
        doVersus = raw_input("Do you want to create "+a_another+" versus column? (y or n) \n") #65 is ascii A
        if doVersus is 'y':
            indexes = getVsIndexes()            #if they choose ab, returns list of those indices: [0,1]
            versusSystems.append(indexes)
            vscol = calcVsCol(syscols, indexes)
            print "\'"+str(chr(indexes[0]+65)).lower()+" played against "+str(chr(indexes[1]+65)).lower()+"\' was placed in column "+str(chr(len(syscols)+65)).lower()+"\n\n"
            syscols.append(vscol)
            count += 1
            
    count = 0
    doConfirmation = 'y'
    confirmationSystems = []
    while doConfirmation is 'y' or doConfirmation is not 'n':
        if doConfirmation is not 'y' and doConfirmation is not 'n':
            print "BAD INPUT!"
        a_another = "another" if count>0 else "a"    
        doConfirmation = raw_input("\nDo you want to create "+a_another+" confirmation column? (y or n) \n")
        if doConfirmation is 'y':
            indexes = getConfirmationIndexes()      #if they choose ab, returns list of those indices: [0,1]
            confirmationSystems.append(indexes)
            confcol = calcConfCol(syscols, indexes)
            print "\'"+str(chr(indexes[0]+65)).lower()+" confirming "+str(chr(indexes[1]+65)).lower()+"\' was placed in column "+str(chr(len(syscols)+65)).lower()+"\n\n" #65 is ascii A            
            syscols.append(confcol)
            count += 1
            
    cont = raw_input("\nPress Enter to view columns...\n")
    currentLine = len(data)-47
    printCols(data, syscols, currentLine)
    stats = getAllStats(data, syscols)
    printStats(stats)
    
    command = 0
    while command is not 'q':
        command = raw_input("commands: 6=page, c=change_data, g=grand_totals, q=quit, r=restart ")
        if command == 'q':
            return
        elif command == 'c':
            clearTerminal()
            data = getData()
            clearTerminal()
            syscols = calcSysCols(systems, data)
            for indexes in versusSystems:
                vscol = calcVsCol(syscols, indexes)
                syscols.append(vscol)
            for indexes in confirmationSystems:
                confcol = calcConfCol(syscols, indexes)
                syscols.append(confcol)
            printCols(data, syscols, currentLine)
            stats = getAllStats(data, syscols)
            printStats(stats)
        elif command == '6':
            currentLine = int(raw_input("What increment do you want to go to? (q to exit) "))
            printCols(data, syscols, currentLine)
        elif command == 'r':
            clearTerminal()
            data = getData()
            clearTerminal()
            main(data)
        elif command == 'g':
            printCols(data, syscols, currentLine)
            stats = getAllStats(data, syscols)
            printStats(stats)
try:
    data = getData()
    main(data)
except Exception as ex:
    print(ex)
    raw_input("There was an Error. Press Enter to Exit...")