import re, math
bits = 8
variablen = {}
def printPLA(numOfOnes=3, numOfXs0=0, variables=None):
    if (variables is None):
        variables = []
    else: variables = variables
    print(f"\t1"*numOfOnes)
    for i in range(numOfXs0):
        string = f"x{(numOfXs0-1)-i}"
        for one in range(numOfOnes):
            string += f"\t{variables[one][i]}"
        print(string)
    print("0", f"\t1" * numOfOnes)
def makeVariablesFromKDNF(kdnf=None): # -x = 3, x = 2 none = 0
    variables = [[7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7]]
    if (kdnf is None): return variables
    varString = ""
    for i in range(numOfVar):
        varString += f"x{numOfVar-i-1}"
    print ("PLA:")
    variables = [varString for i in range(kdnf.count(" ")+1)] # anzahl der min-therme
    kdnf = kdnf.split()
    for i in range(len(kdnf)):
        for j in range(len(kdnf[i])):
            if (kdnf[i][j:j+2] == "-x"): # nand
                variables[i] = re.sub(kdnf[i][j+1:j+3], "3", variables[i])
                #print(f"Treffer {kdnf[i][j+1:j+3]}")
                #print(variables[i])
            elif (kdnf[i][j] == "x" and kdnf[i][j-1:j+1] != "-x"):
                #print(f"Treffer {kdnf[i][j]}, {kdnf[i][j-1:j+1]}, {kdnf[i][j:j+2]}")
                #print(variables[i])
                variables[i] = re.sub(kdnf[i][j:j+2], "2", variables[i])
    #print(variables)
    for i in range(len(variables)):
        j = 0
        while (j < len(variables[i])):
            if (variables[i][j] == "x"):
                variables[i] = re.sub(variables[i][j:j+2], "0", variables[i])
                j = 0
            j += 1
    ergList = []
    for i in variables:
        ergList.append([int(char) for char in i])
    #print(ergList)
    return ergList
def startPLA():
    print("z.B. 3 wenn x2x1x0 oder 4 wenn x3x2x1x0")
    global numOfVar
    numOfVar = int(input("Anazhl der Unbekannten: "))
    print("z.B. -x3-x1 -x2-x1 -x3x2-x0")
    print("Bitte Reihenfolge beachten (nicht x0x1x2) sondern (x2x1x0)")
    print('"-" steht für not')
    userInput = input("KDNF: ")
    variablen = makeVariablesFromKDNF(userInput)
    printPLA(len(variablen), numOfVar, variablen)
def kPlan(): # 4 bit
    print("z.B. 1,2,3,4,5")
    userInput = input("V kj = ")
    if (userInput in variablen): userInput = variablen[userInput]
    print("V kj = {"+f"{userInput}"+"}")
    funktion = userInput.split(",")
    for digit in range(len(funktion)): funktion[digit] = dezToBin(1, int(funktion[digit]), 4, 1)
    inside = []
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    inside.append({f"{a}{b}{c}{d}": "0"})
    for digit in funktion:
        for i in range(16):
            if (digit in inside[i]):
                inside[i][digit] = 1
    print("\tx1x0")
    print(f"\t\t\t|\t00\t01\t11\t10")
    print("\t\t----+-----------------")
    print(f"x3x2\t00\t|\t{inside[0]['0000']}\t{inside[1]['0001']}\t{inside[3]['0011']}\t{inside[2]['0010']}")
    print(f"\t\t01\t|\t{inside[4]['0100']}\t{inside[5]['0101']}\t{inside[7]['0111']}\t{inside[6]['0110']}")
    print(f"\t\t11\t|\t{inside[12]['1100']}\t{inside[13]['1101']}\t{inside[15]['1111']}\t{inside[14]['1110']}")
    print(f"\t\t10\t|\t{inside[8]['1000']}\t{inside[9]['1001']}\t{inside[11]['1011']}\t{inside[10]['1010']}")
    marksInKP = []
    for i in inside:
        for binCode, val in i.items():
            if (val == 1): marksInKP.append(list(binCode))
    for mark in range(len(marksInKP)):
        for num in range(len(marksInKP[mark])):
            if(marksInKP[mark][num] == '0'): marksInKP[mark][num] = f"~x{num}"
            if(marksInKP[mark][num] == '1'): marksInKP[mark][num] = f"x{num}"
    y = "y = "
    for i in range(len(marksInKP)):
        if (i == len(marksInKP)-1):
            y += f"{''.join(marksInKP[i])}"
            break
        y += f"{''.join(marksInKP[i])} ∨ "
    print(y)
    return y
def binRechner():
    global cFlag
    zFlag, cFlag, ovFlag, sFlag = 0, 0, 0, 0
    dezNumOne = input("Dez num: ")
    if (dezNumOne in variablen): dezNumOne = variablen[dezNumOne]
    numOne = dezToBin(1, int(dezNumOne), fill=bits)
    operator = input("Operation (+, -, *): ")
    dezNumTwo = input("Dez num: ")
    if (dezNumTwo in variablen): dezNumTwo = variablen[dezNumTwo]
    if (operator == "-"): numTwo = dezToBin(1, int(dezNumTwo) * -1, fill=bits)
    else: numTwo = dezToBin(1, dezNumTwo, fill=bits)
    print("")
    print(f"\t{numOne}")
    if (operator == "-"): print(f"+\t{numTwo}\t(Zweierkomplement von {dezNumTwo} - alle Bits negieren, 1 addieren)")
    else: print(f"+\t{numTwo}")
    print("-------------")
    binErg = ["0" for k in range(bits)]
    for i in range(bits):
        if (numOne[bits-1-i] != numTwo[bits-1-i]): # 1 + 0 = 1
            if (binErg[bits-1-i] == "1"): # 1 + 0 + 1
                binErg[bits-1-i] = "0"
                if (i<=bits-2): binErg[bits-2-i] = "1"
                if (i==bits-1): cFlag = 1 # carry flag gestzt
            else:
                binErg[bits-1-i] = "1"
        elif (numOne[bits-1-i] == numTwo[bits-1-i] and numTwo[bits-1-i] == "1"): # 1 + 1 = 0
            if (binErg[bits-1-i] == "1"):  # 1 + 1 + 1 = 1
                binErg[bits-1-i] = "1"
                if (i<=bits-2): binErg[bits-2-i] = "1"
                if (i==bits-1): # carry flag gesetzt
                    cFlag = 1
            else:
                binErg[bits-1-i] = "0"
                if (i<=bits-2): binErg[bits-2-i] = "1"
                if (i==bits-1): # carry flag gesetzt
                    cFlag = 1
    print(f"({cFlag})\t{''.join(binErg)}")
    if ("1" not in binErg): zFlag = 1
    sFlag = binErg[0]
    if (operator == "+"):
        if int(dezNumOne)+int(dezNumTwo) > ((2**bits)/2)-1 or int(dezNumOne)+int(dezNumTwo) < -(2**bits)/2: ovFlag = 1
    else:
        if int(dezNumOne)-int(dezNumTwo) > ((2**bits)/2)-1 or int(dezNumOne)-int(dezNumTwo) < -(2**bits)/2: ovFlag = 1
    print(f"S-Flag = {sFlag}\tC-Flag = {cFlag}")
    print(f"Ov-Flag = {ovFlag}\tZ-Flag = {zFlag}")
def zweierKomplement(default=""):
    if (not default): tmpNum = dezToBin(1)
    else: tmpNum = default # kommt aus dez to bin
    zkNum= []
    for i in tmpNum:
        if (i == "0"): zkNum.append("1")
        if (i == "1"): zkNum.append("0")
    for j in range(len(zkNum)-1):
        if (zkNum[len(zkNum)-1-j] == "1"):
            zkNum[len(zkNum)-1-j] = "0"
        else:
            zkNum[len(zkNum)-1-j] = "1"
            break
    #print(f"Zahl:\t\t\t\t{tmpNum}")
    #print(f"Zweier Komplement:\t{''.join(zkNum)}")
    return ''.join(zkNum)
def binToHex(num=None):
    hexNum = []
    dict = {"0000":"0","0001":"1","0010":"2","0011":"3",
            "0100":"4","0101":"5","0110":"6","0111":"7",
            "1000":"8","1001":"9","1010":"A","1011":"B",
            "1100":"C","1101":"D","1110":"E","1111":"F"}
    if (num == None):
        binNum = input("Bin num: ")
        if (binNum in variablen): binNum = variablen[binNum]
    else: binNum = num
    for i in range(4, len(binNum)+4, 4):
        hexNum.append(dict[binNum[i-4:i]])
    return hexNum
def hexToBin(num=None):
    base = [i for i in "0123456789ABCDEF"] # ~ erhöht index auf 16 mit 16 relevanten elementen
    binNum = []
    if (num == None):
        hexNum = input("Hex num: 0x")
        if (hexNum in variablen): hexNum = variablen[hexNum]
    else: hexNum = num
    for i in  hexNum: binNum.append(dezToBin(1, base.index(i), 4))
    return binNum
def fltToIEEE(num=None, bit=32):
    global bias
    global vorzeichen
    vorzeichen = 0
    print("pls use '.' not ','")
    if (num == None):
        fltNum = input("float: ")
        if (fltNum in variablen): fltNum = variablen[fltNum]
    else: fltNum = num
    if ("-" in fltNum): vorzeichen = 1

    ########### 1. vorkomma in bin ###########
    print("---------------------------")
    print("1. vorkommastellen in binär")
    print("---------------------------")
    vrkNumDez = fltNum[:fltNum.index(".")]
    vrkNumBin = dezToBin(0, int(vrkNumDez), 0)
    print(f"Vorkommazahl: {vrkNumDez} in Binär: {vrkNumBin}")

    ########### 2. nachkomma in bin ##########
    print("---------------------------")
    print("2. nachkommastellen in binär")
    print("---------------------------")
    nchKommaDez = "0"+fltNum[fltNum.index("."):]
    nchKommaBin = f"{''.join(kommaToBin(nchKommaDez))}"
    print(f"Nachkommazahl: {nchKommaDez} in Binär: {nchKommaBin}")

    ############ 3. normalisieren ############
    print("---------------------------")
    print("3. normalisieren")
    print("---------------------------")
    print(f"{vrkNumBin}.{nchKommaBin*3}...*2^0")
    index, exp = 0, 0
    for i in range(len(nchKommaBin)):
        if (nchKommaBin[i] == "1"):
            index = i
            break
    if (vrkNumBin != "0"):
        exp = len(vrkNumBin) - 1
        print(f"{vrkNumBin[0]}.{vrkNumBin[1:]}{nchKommaBin*3}...*2^{exp}")
    else:
        exp = (index+1)*-1
        if (int(vorzeichen)):
            if (nchKommaBin[index+1:] == "0" or nchKommaBin[index+1:] == "1"):
                print(f"{nchKommaBin[index]}.{nchKommaBin[index+1:]}{nchKommaBin*2}...*2^{exp}")
            else: print(f"{nchKommaBin[index]}.{'0'*12}...*2^{exp}")
        else:
            if (nchKommaBin[index+1] == "0" or nchKommaBin[index+1] == "1"):
                print(f"{nchKommaBin[index]}.{nchKommaBin[index+1:]}{nchKommaBin*2}...*2^{exp}")
            else: print(f"{nchKommaBin[index]}.{'0'*12}...*2^{exp}")

    ########### 4. charakteristik ############
    if (bit == 32): bias = 127
    print(f"Bias: {bias}, Exponent: {exp}")
    print(f"Charakteristik = {exp} + {bias} = {bias+exp}")
    print()
    charak = dezToBin(0, bias+exp, 8) # 8 bits
    print(f"Charakteristik in Binär = {charak}")

    ############# 5. vorzeichen ##############
    print("---------------------------")
    print("5. vorzeichen")
    print("---------------------------")
    print(f"Vorzeichen = {vorzeichen}")

    ########### 6. gleitkommazahl ############
    print("---------------------------")
    print("6. gleitkommazahl")
    print("---------------------------")
    print(f"Vorzeichen Bit = {vorzeichen}")
    print(f"Char. 8 bit = {charak}")
    if (vrkNumBin != "0"): mantisse = (vrkNumBin[1:]+nchKommaBin*7)[0:23]
    else:
        if (int(vorzeichen)):
            if (nchKommaBin[index+1:] == "0" or nchKommaBin[index+1:] == "1"):
                mantisse = (nchKommaBin[index+1:]+nchKommaBin*100)[0:23]
            else: mantisse = "0"*23
        else:
            if (nchKommaBin[index+1] == "0" or nchKommaBin[index+1] == "1"):
                mantisse = (nchKommaBin[index+1:]+nchKommaBin*100)[0:23]
            else: mantisse = "0"*23

    print(f"Mantisse 23 bit = {mantisse}")
    print()
    gltBinNum = str(vorzeichen)+charak+mantisse
    print(f"Gleitkommazahl in bin= {gltBinNum}")
    print(f"Gleitkommazahl in hex= {''.join(binToHex(gltBinNum))}")
    return [gltBinNum, ''.join(binToHex(gltBinNum))]
def ieeeToFlt(num=None):
    bias, mantisse, exp, vorzeichen, charakt, fltNum = 127, "0"*23, "0", "0"*1, "0"*8, 0
    if (num is None):
        ieeeNum = input("IEEE: ")
        if (ieeeNum in variablen): ieeeNum = variablen[ieeeNum]
        if (len(ieeeNum) < 32): ieeeNum = "".join(hexToBin(ieeeNum))
    else: ieeeNum = num # vccccccccmmmmmmmmmmmmmmmmmmmmmmm
    # 1 01111011 00000000000000000000000
    print("Bin num: ", ieeeNum)
    ########### vorzeichen bestimmen ###########
    vorzeichen = int(ieeeNum[0]) # v

    ########### charakteristik bestimmen #######
    charakt = ieeeNum[1:9] # cccccccc

    ########### exponent bestimmen #############
    charakt = binToDez(charakt) # dez
    exp = charakt-bias

    ########### fraction bestimmen #############
    fraction = ieeeNum[9:] # mmmmmmmmmmmmmmmmmmmmmmm
    fraction = float(binToKomma(fraction)) # dez

    ########### gleitkommazahl bestimmen #############
    fltNum += ((-1)**vorzeichen)*(1+fraction)*(2**exp)
    print(fltNum)
    if (fltNum < 0.00000001): fltNum = 0
    if (fltNum > 100000000): fltNum = "+INF"
    return fltNum
def kommaToBin(num=None, output=True):
    marks = []
    binNum = []
    if (num is None):
        fltNum = input("vorkomma num: ")
        if (fltNum in variablen): fltNum = variablen[fltNum]
        fltNum = float(fltNum)
    else: fltNum = float(num)
    while (fltNum*2 not in marks):
        if (output): print(f"{fltNum} * 2 = {fltNum*2}\t{str(((fltNum*2)//1))[0]}")
        binNum.append(str(((fltNum*2)//1))[0])
        marks.append(fltNum*2)
        if (fltNum*2 >= 1):
            fltNum = float("0."+str(fltNum*2)[2:])
        else:
            fltNum = fltNum*2
    if (vorzeichen):
        for i in binNum:
            if (binNum[-1] == "0"): binNum = binNum[:len(binNum)-1]
    return binNum
def binToKomma(num=None):
    dez = 0
    if (num is None):
        num = input("Bin num:")
        if (num in variablen): num = variablen[num]
    else: binNum = num
    for i in range(len(num)):
        if (num[i]=="1"): dez += 2**(-i-1)
    return dez
def dezToBin(output=0, number=None, fill=8, kP=0):
    mark = 0
    try:
        if (number != None or kP): numOne = int(number)
        else:
            numOne = input("Dez num: ")
            if (numOne in variablen): numOne = int(variablen[numOne])
            numOne = int(numOne)
        if (numOne < 0):
            numOne *= -1
            mark = 1
        binNum = bin(numOne)
        while (numOne):
            if (output == 0): print(f"{numOne} % 2 = {numOne%2}")
            numOne //= 2
        binNum = re.sub('0b', '', binNum)
        if (mark): return zweierKomplement(str(binNum).zfill(8))
        return str(binNum).zfill(fill)
    except ValueError:
        print("pls enter a valid decimal num")
        dezToBin()
def binToDez(num=None):
    dez = 0
    if (num is not None):
        for i in range(len(num)):
            if (num[i]=="1"): dez += 2**(len(num)-1-i)
    else:
        try:
            binNum = input("Bin num: ")
            if (binNum in variablen): binNum = variablen[binNum]
            for i in range(len(binNum)):
                if (binNum[i] == "1"): dez += 2**(len(binNum)-1-i)
        except ValueError:
            print("pls enter a valid num")
            binToDez()
    return dez
def hamming(inside=None, ones=0, zeros=0):
    if (inside is None): inside = {'dez':[0,0,0], 'binCode':[0,0,0], 'hamDist':[0,0,0]}
    print()
    if (zeros+ones <= 8):
        print(f"\tDez Wert\t|\tBin Code\t|\tHamming-Distanz")
        print("\t------------+---------------+------------------")
        for i in range(len(inside['dez'])): print(f"\t\t{inside['dez'][i]}\t\t|\t\t{inside['binCode'][i]}\t|\t\t\t{inside['hamDist'][i]}")
    else: print("!!Darstellung geht nur bis x aus 8!!")
    print()
    print(f"Minimale Distanz\t\t\t= {min(inside['hamDist'][1:])}")
    print(f"Maximale Distanz\t\t\t= {max(inside['hamDist'][1:])}")
    print(f"Anzahl gültiger Codewörter\t= {len(inside['binCode'])}")
def getListFromHamming():
    listHamming = {'dez': [], 'binCode': [], 'hamDist': [0]}
    print("z.B. 2 aus 5, oder 7 aus 11")
    hammingMode = input("Code: ").split(" aus ")
    ones = int(hammingMode[0])
    zeros = int(hammingMode[1])-int(hammingMode[0])
    for i in range(2**(zeros+ones)):
        tmp = dezToBin(output=1, number=i, fill=zeros+ones)
        if (tmp.count("1") == ones):
            listHamming['dez'].append(binToDez(tmp))
            listHamming['binCode'].append(tmp)
    for i in range(len(listHamming['binCode'])-1):
        dist = 0
        for j in range(ones+zeros): # bits
            if listHamming['binCode'][i][j] != listHamming['binCode'][i + 1][j]:
                dist += 1
        listHamming['hamDist'].append(dist)
    return hamming(listHamming, ones, zeros)
def cache():
    # Direkt abbildender Cache
    storage = input("Byte-Adresierbarer Speicher: \t\t in MiB angeben \n")
    if (storage in variablen): storage = variablen[storage]
    storage = int(storage)
    print("\nDirektabbildender Cache")
    cache_line = input("Blockgröße (Cache Line): \t\t in Byte angeben \n")
    if (cache_line in variablen): cache_line = variablen[cache_line]
    cache_line = int(cache_line)
    total = input("Gesamte (Daten-)Größe des Cache \t in KiB angeben \n")
    if (total in variablen): total = variablen[total]
    total = int(total)
    print()
    # Länge der Adresse
    # 1 MiB = 1 048 576 Byte
    length = storage * 1048576
    length = int(math.log2(length))
    print("Gesamtlänge:", length)
    # Byte-Adresse
    byte_address = int(math.log2(cache_line))
    print("Byte-Adresse:", byte_address)
    # Line-Index
    # 1 KiB = 1024 Byte
    line_index = total * 1024
    line_index = int(math.log2(line_index))
    line_index -= byte_address
    print("Line-Index:", line_index)
    # Kennung(Tag)
    tag = length - byte_address - line_index
    print("Kennung(Tag)", tag)
    print()
    print("+----------------+------------+--------------+)")
    print("| Kennung (=Tag) | Line-Index | Byte-Adresse |")
    print("+----------------+------------+--------------+")
    print("|    ", tag, " Bit    |   ", line_index, "Bit  |   ", byte_address, " Bit    |")
    print("+----------------+------------+--------------+\n")
    # N-Wege-Satz-assoziativer Cache
    print("N-Wege-Satz-assoziativer Cache")
    n = input("N: ")
    n = int(n)
    # Satz-Index
    index = total * 1024
    index /= cache_line
    index /= n
    index = int(math.log2(index))
    # Kennung(Tag) aktualisieren
    tag = length - byte_address - index
    print("+----------------+------------+--------------+)")
    print("| Kennung (=Tag) | Line-Index | Byte-Adresse |")
    print("+----------------+------------+--------------+")
    print("|    ", tag, " Bit    |   ", index, "Bit  |   ", byte_address, " Bit    |")
    print("+----------------+------------+--------------+\n")


def mainFrame(outPutMenue=False):
    global bits
    modes = [
        ["Binär Rechnen","br"],
        ["Zweier Kompl.","zk"],
        ["Binary to Dez","btd"],
        ["Decimal to Bin","dtb"],
        ["Karnaugh-Plan","kp"],
        ["PLA\t\t\t","pla"],
        ["Hamming Code","hc"],
        ["Binary to hex","bth"],
        ["Hex to bin\t","htb"],
        ["Dez to IEEE\t","dti"],
        ["Komma to bin","ktb"],
        ["IEEE to flt\t","itf"],
        ["Bin to Komma","btk"],
        ["Cache\t\t","c"]]
    if (outPutMenue):
        print("Name\t\t\t\tShortcut\t\tMode")
        print("-----------------------------------------")
        for i in range(len(modes)): print(f"{modes[i][0]}\t\t{modes[i][1]}\t\t\t\t{i+1}")
        print("-----------------------------------------")
    mode = input(">>> ")
    if (mode == "1" or mode == modes[0][1]): binRechner()
    elif (mode == "2" or mode == modes[1][1]): print(f"Zweierkomplement: {zweierKomplement()}")
    elif (mode == "3" or mode == modes[2][1]): print(binToDez())
    elif (mode == "4" or mode == modes[3][1]): print("Binary Number = ",dezToBin(fill=bits))
    elif (mode == "5" or mode == modes[4][1]): kPlan()
    elif (mode == "6" or mode == modes[5][1]): startPLA()
    elif (mode == "7" or mode == modes[6][1]): getListFromHamming()
    elif (mode == "8" or mode == modes[7][1]): print(f"Hex: 0x{''.join(binToHex())}")
    elif (mode == "9" or mode == modes[8][1]): print(f"Bin: {''.join(hexToBin())}")
    elif (mode == "10" or mode == modes[9][1]): fltToIEEE()
    elif (mode == "11" or mode == modes[10][1]): print(f"Bin num: {''.join(kommaToBin())}")
    elif (mode == "12" or mode == modes[11][1]): print(f"Flt num: {ieeeToFlt()}")
    elif (mode == "13" or mode == modes[12][1]): print(f"Komma num: {binToKomma()}")
    elif (mode == "14" or mode == modes[13][1]): cache()
    elif (mode in ["?", "help", "hilfe", "h"]): mainFrame(True)
    elif (mode == "var"):
        name = input("Name: ")
        if (name == "all"):
            for name, val in variablen.items(): print(f"{name}: {val}")
        else: print(variablen[name])
    elif (mode in ["clear", "clean", "cls"]):
        for i in range(100): print()
    elif (mode == "bits"): bits = int(input("Set bits to: "))
    elif (mode in ["new", "neu"]):
        name = input("Name of new var: ")
        val = input("value: ")
        if (val == modes[0][1]): binRechner()
        elif (val == modes[1][1]): val = f"{zweierKomplement()}"
        elif (val == modes[2][1]): val = binToDez()
        elif (val == modes[3][1]): val = dezToBin(fill=bits)
        elif (val == modes[4][1]): val = kPlan()
        elif (val == modes[7][1]): val = f"{''.join(binToHex())}"
        elif (val == modes[8][1]): val = f"{''.join(hexToBin())}"
        elif (val == modes[9][1]): val = fltToIEEE()
        elif (val == modes[10][1]): val = f"{''.join(kommaToBin())}"
        elif (val == modes[11][1]): val = f"{ieeeToFlt()}"
        elif (val == modes[12][1]): val = f"{binToKomma()}"
        variablen[name] = val
    mainFrame()

if __name__ == "__main__":
    #ieeeToFlt("10111101100000000000000000000000")
    mainFrame()

#   mit 'new' oder 'neu' können variablen angelegt werden
#   diese können benutzer speziefische belegungen haben oder
#   rückgabewerte von den verfügbaren funktionen. Dazu kann
#   man einfach den shortcut eingeben wenn nach dem value der
#   variable gefragt ist
#
#   mit 'var' kann eine belibige oder alle variable/n angezeigt werden
#   dazu den namen der variable oder 'all' eingeben wenn nach name gefragt ist