"""
Contains functions for parsing a data set containing proteins given a file
"""
from sys import *
from os import path
from hmm import *
from ourHmm import *
import nltk as nltk
from random import *
from CRFEvaluator import *
from SVMHMMEvaluator import *

"""
parseText takes in a filename and parses that file
The expectation is that the file consists of info about proteins, where
each protein takes up three lines

The first line contains irrelevant info about the protein.
The second line is the AA sequence.
The third line is the secondary structure.

This function grabs the second and third lines, and creates a list of lists 
where each sublist is the AA sequence and secondary structure of a protein.
"""
def parseText(filename):
    if not path.exists(filename):
        print "Could not find the data set. Exiting."
        exit(0)

    data = []
    with open(filename, 'r') as infile:
        entry = []
        count = 0
        for line in infile:
            if count == 1 or count == 2:
                entry.append(line.rstrip('\n'))
            if count == 2:
                data.append(entry)
                entry = []
            count = (count + 1) % 3
    return data

"""
This function takes in a list of lists, where each sublist is the AA sequence 
and secondary structure of a protein. It converts the seconary structure to 
contain only helices, beta sheets, and coils.
"""
def convertData(data, structureDict):
    words = []
    tags = ['b', 'h', 'c']
    convertedData = []
    normalData = []
    for entry in data:
        newEntry = []
        normalEntry = []
        structureLine = entry[1]
        convertedLine = ""
        normalLine = ""
        for i in range(len(structureLine)):
            currChar = structureLine[i]
            convertedLine += structureDict[currChar]
            normalLine += currChar
        for i in range(len(structureLine)):
            currChar = (entry[0])[i]
            currSym = convertedLine[i]
            normalSym = normalLine[i]
            currTup = (currChar, currSym)
            normalTup = (currChar, normalSym)
            newEntry.append(currTup)
            normalEntry.append(normalTup)
            if currChar not in words:
                words.append(currChar)
        convertedData.append(newEntry)
        normalData.append(normalEntry)
    return convertedData, words, tags, normalData
        

"""
creates a dictionary that maps secondary structure classifications to
the larger categories of helices, beta sheets, and coils
"""
def createStructureDict():
    """
    H, G, and I are helices
    E and B are beta strands
    T, S, and - are residues that arent helices or strands
    """

    structureDict = {}
    helixList = ['H', 'G', 'I']
    betaList = ['E', 'B']
    coilList = ['T', 'S', '-']

    for symb in helixList:
        structureDict[symb] = 'h'
    for symb in betaList:
        structureDict[symb] = 'b'
    for symb in coilList:
        structureDict[symb] = 'c'
    return structureDict

"""
takes in the converted data and outputs lists with the sequences and their
labels
"""
def createSeqAndLab(convertedData):
    sequences = []
    labels = []
    for seq in convertedData:
        currSeqEntry = []
        currLabEntry = []
        for tup in seq:
            currSeqEntry.append(tup[0])
            currLabEntry.append(tup[1])
        sequences.append(currSeqEntry)
        labels.append(currLabEntry)
    return sequences, labels

"""
takes in sequences, labels, a character, and the percentage we want to
limit that character to

used to remove examples with high percentages of certain characters
as part of an attempt to make the training set more suitable for learning
"""
def cullExamples(sequences, labels, percentage, character):
    #remove examples with high h_count percentage
    final_seqs = []
    final_labs = []
    for i in range(len(sequences)):
        h_count = 0
        seq = sequences[i]
        lab = labels[i]
        for char in lab:
            if char == character:
                h_count+=1
        examp_percent = float(h_count)/len(seq)
        if examp_percent < percentage:
            final_seqs.append(seq)
            final_labs.append(lab)
    return final_seqs, final_labs

"""
Outputs overall accuracy statistics using runHMM
"""
def getResultsForHMM(train_data, test_data, words, tags):
    totalTruePosH = 0
    totalFalsePosH = 0
    totalTrueNegH = 0
    totalFalseNegH = 0

    totalTruePosB = 0
    totalFalsePosB = 0
    totalTrueNegB = 0
    totalFalseNegB = 0

    totalTruePosC = 0
    totalFalsePosC = 0
    totalTrueNegC = 0
    totalFalseNegC = 0

    for i in range(3):
        truePosH, falsePosH, trueNegH, falseNegH, truePosB, falsePosB, trueNegB, falseNegB, truePosC, falsePosC, trueNegC, falseNegC = runHMM(train_data, test_data, words, tags)

        totalTruePosH += truePosH
        totalFalsePosH += falsePosH
        totalTrueNegH += trueNegH
        totalFalseNegH += falseNegH

        totalTruePosB += truePosB
        totalFalsePosB += falsePosB
        totalTrueNegB += trueNegB
        totalFalseNegB += falseNegB

        totalTruePosC += truePosC
        totalFalsePosC += falsePosC
        totalTrueNegC += trueNegC
        totalFalseNegC += falseNegC

    print "%d," %(totalTruePosH/float(3)),
    print "%d," %(totalFalsePosH/float(3)),
    print "%d," %(totalTrueNegH/float(3)),
    print "%d," %(totalFalseNegH/float(3)),

    print "%d," %(totalTruePosB/float(3)),
    print "%d," %(totalFalsePosB/float(3)),
    print "%d," %(totalTrueNegB/float(3)),
    print "%d," %(totalFalseNegB/float(3)),

    print "%d," %(totalTruePosC/float(3)),
    print "%d," %(totalFalsePosC/float(3)),
    print "%d," %(totalTrueNegC/float(3)),
    print "%d" %(totalFalseNegC/float(3))

    """
    print"\nH DATA:"
    print "True Positive H: %d" 
    print "False Positive H: %d" %(totalFalsePosH/float(3))
    print "True Negative H: %d" %(totalTrueNegH/float(3))
    print "False Negative H: %d" %(totalFalseNegH/float(3))

    print"\nB DATA:"
    print "True Positive B: %d" %(totalTruePosB/float(3))
    print "False Positive B: %d" %(totalFalsePosB/float(3))
    print "True Negative B: %d" %(totalTrueNegB/float(3))
    print "False Negative B: %d" %(totalFalseNegB/float(3))

    print"\nC DATA:"
    print "True Positive C: %d" %(totalTruePosC/float(3))
    print "False Positive C: %d" %(totalFalsePosC/float(3))
    print "True Negative C: %d" %(totalTrueNegC/float(3))
    print "False Negative C: %d" %(totalFalseNegC/float(3))
    """

"""
superMain ba da da dum
"""
def main():
    if len(argv) != 4:
        print "Should give just name of file to read in"
        exit(0)

    filename = argv[1] #file being read in
    n = argv[2] #size of training set
    creating = argv[3] #boolean for creating variable specified below

    if n.isdigit():
        if int(n) < 0 or int(n) > 1400:
            print 'Invalid choice for n. Try again.'
            exit(0)
    n = int(n)

    if creating.isdigit():
        if int(creating) < 0 or int(creating) > 1400:
            print 'creating needs to be 0 for false or anything else for true. Try again.'
            exit(0)
    creating = int(creating)

    if creating == 0:
        creating = False
    else:
        creating = True

    data = parseText(filename)
    structureDict = createStructureDict()
    convertedData, words, tags, normalData = convertData(data, structureDict)

    #print "Created list of lists, there are: %d entries" %(len(convertedData))

    shuffle(convertedData)

    train_data = convertedData[0:n]
    test_data = convertedData[1775:1975]

    our_seq, our_lab = createSeqAndLab(train_data)
    #our_seq, our_lab = cullExamples(our_seq, our_lab, 0.25, 'h')
    #our_seq, our_lab = cullExamples(our_seq, our_lab, 0.38, 'b')
    #our_seq, our_lab = cullExamples(our_seq, our_lab, 0.38, 'c')
    #print "\n\nIN THE END WE HAVE: ", len(our_seq), "\n"
    our_test_seq, our_test_lab = createSeqAndLab(test_data)


    #==============================================================
    #getResultsForHMM(train_data, test_data, words, tags)
    #==============================================================
    
    
    #==============================================================
    """
    if creating:
        createCRFFiles(our_seq, our_lab, our_test_seq, our_test_lab)
    else:
        runCRFEvaluation(our_seq, our_test_seq)
    """
    #==============================================================
    
    
    #==============================================================
    
    """
    if creating:
        createInput(our_seq, our_lab, words, "svmTrainInput")
        createInput(our_test_seq, our_test_lab, words, "svmTestInput")
    else:
        getResults()
    """
    
    #==============================================================

    """
    for example in CRF_examples:
        print example
    """




if __name__ == '__main__':
    main()
