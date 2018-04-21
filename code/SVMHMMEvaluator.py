"""
This file contains code for running and evaluating SVM HMMs 
"""
#creates encoding dictionary
def createTagEncoding(words):
    wordEncoding = {}
    mapVal = 1
    for word in words:
        wordEncoding[word] = mapVal
        mapVal += 1
    return wordEncoding

"""
Create input strings using fifteen character windows
"""
def createInputStrings(sequences, labels, words):
    encoding = createTagEncoding(words)
    finalStrings = []
    for i in range(len(sequences)):
        strings, NA = get15CharExamples(sequences[i], labels[i], True, i, encoding)
        for string in strings:
            finalStrings.append(string)
    return finalStrings
        

"""
write each example in examples to a file
each example occupies one line
"""
def SVMWriteToFile(filename, examples):
    with open(filename, 'w') as outFile:
        for example in examples:
            example += "\n"
            outFile.write(example)


"""
obtain a set of fifteen character windows given a sequence
"""
def get15CharExamples(seq, lab, train, exnum, encoding):
    labelDict = {'h': '1', 'b': '2', 'c': '3'}
    data = []
    labelOutput = []
    startIdx = 0
    endIdx = 14 
    labIdx = 7 
    while endIdx != len(seq)-1:
        curr_str = ""
        if train == True:
            curr_str += labelDict[lab[labIdx]]
        else:
            labelOutput.append(lab[labIdx])

        curr_str += " "
        curr_str += "qid:"
        curr_str += str(exnum)
        curr_str += " "

        window = seq[startIdx:endIdx+1]
        curr_str += convertToInputType(window, encoding)
        startIdx += 1
        endIdx += 1
        labIdx += 1
        data.append(curr_str)
    return data, labelOutput 

"""
given a string and an encoding, convert the string
based on the encoding and output it
"""
def convertToInputType(string, encoding):
    finalOutput = ""
    for i in range(len(string)):
        finalOutput += str(i+1)
        finalOutput += ":"
        finalOutput += str(encoding[string[i]])
        finalOutput += " "
    finalOutput += "#"
    finalOutput += str(string)
    return finalOutput

"""
calculate the results when testing the data after the
output tag file has been created
"""
def getResults():
    labelDict = {'1': 'h', '2': 'b', '3': 'c'}
    testFileName = "svm_binaries/svmTestInput"
    predictionFileName = "svm_binaries/classify.tags"

    actualSeq = ""
    with open(testFileName, 'r') as inFile:
        for line in inFile:
            char = line[0]
            actualSeq += labelDict[char]

    taggedSeq = ""
    with open(predictionFileName, 'r') as inFile:
        for line in inFile:
            char = line[0]
            taggedSeq += labelDict[char]

    print len(taggedSeq)
    print len(actualSeq)
    calcSVMError(taggedSeq, actualSeq)


"""
helper function for calculating error counts
"""
def calcSVMError(taggedSeq, actualSeq):
    truePosH = 0
    falsePosH = 0
    trueNegH = 0
    falseNegH = 0

    truePosB = 0
    falsePosB = 0
    trueNegB = 0
    falseNegB = 0

    truePosC = 0
    falsePosC = 0
    trueNegC = 0
    falseNegC = 0



    for i in range(len(taggedSeq)):
        if taggedSeq[i] == 'c':
            if taggedSeq[i] == actualSeq[i]:
                truePosC += 1
                trueNegB += 1
                trueNegH += 1
            else:
                if actualSeq[i] == 'b':
                    falseNegB += 1
                elif actualSeq[i] == 'h':
                    falseNegH += 1
                falsePosC += 1

        elif taggedSeq[i] == 'h':
            if taggedSeq[i] == actualSeq[i]:
                truePosH += 1
                trueNegC += 1
                trueNegB += 1
            else:
                if actualSeq[i] == 'c':
                    falseNegC += 1
                elif actualSeq[i] == 'b':
                    falseNegB += 1
                falsePosH += 1

        elif taggedSeq[i] == 'b':
            if taggedSeq[i] == actualSeq[i]:
                truePosB += 1
                trueNegC += 1
                trueNegH += 1
            else:
                if actualSeq[i] == 'c':
                    falseNegC += 1
                elif actualSeq[i] == 'h':
                    falseNegH += 1
                falsePosB += 1

    print"\nH DATA:"
    print "True Positive H: %d" %truePosH
    print "False Positive H: %d" %falsePosH
    print "True Negative H: %d" %trueNegH
    print "False Negative H: %d" %falseNegH

    print"\nB DATA:"
    print "True Positive B: %d" %truePosB
    print "False Positive B: %d" %falsePosB
    print "True Negative B: %d" %trueNegB
    print "False Negative B: %d" %falseNegB

    print"\nC DATA:"
    print "True Positive C: %d" %truePosC
    print "False Positive C: %d" %falsePosC
    print "True Negative C: %d" %trueNegC
    print "False Negative C: %d" %falseNegC



"""
creates input for svm hmms
"""
def createInput(sequences, labels, words, filename):
    examples = createInputStrings(sequences, labels, words)
    SVMWriteToFile(filename, examples)
