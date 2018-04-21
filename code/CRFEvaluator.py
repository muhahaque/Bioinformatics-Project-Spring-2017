"""
File for running CRFs and evaluating their performance
"""
from sys import *
from os import path

"""
Used to write output from algorithm to a file
"""
def writeToFile(filename, CRF_examples):
    with open(filename, 'w') as outFile:
        for example in CRF_examples:
            example += "\n"
            outFile.write(example)

"""
Used to loop through a list of character lists and concatenate all their characters
"""         
def concatenateAll(char_lst):
    final_string = ""
    for lst in char_lst:
        for char in lst:
            final_string += char
    return final_string

"""
Used to take a list of characters and combine them into a string
"""
def makeStr(char_lst):
    final_string = ""
    for char in char_lst:
        final_string += char
    return final_string

"""
Used to create training data with features that are 15 amino acid windows,
labeled by the secondary structure of the middle amino acid
"""
def getCRFExamples(seq, lab, train):
    data = []
    labelOutput = []
    startIdx = 0
    endIdx = 14
    labIdx = 7
    while endIdx != len(seq)-1:
        curr_str = seq[startIdx:endIdx+1]
        curr_str = makeSpaces(curr_str)
        if train == True:
            curr_str += lab[labIdx]
        else:
            curr_str = curr_str.rstrip()
            labelOutput.append(lab[labIdx])
        startIdx += 1
        endIdx += 1
        labIdx += 1
        data.append(curr_str)
    return data, labelOutput 

"""
takes a string and inserts spaces between each character
"""
def makeSpaces(str):
    output = ""
    for char in str:
        output += char
        output += " "
    return output


"""
create the training and testing files for CRFs
as well as a file with the correct labels to help analyze the test result's accuracy
"""
def createCRFFiles(our_seq, our_lab, our_test_seq, our_test_lab):
    totalExamples = []
    for i in range(len(our_seq)):
        CRF_train_seq = makeStr(our_seq[i])
        CRF_train_lab = makeStr(our_lab[i])
        CRF_train_examples, NA = getCRFExamples(CRF_train_seq, CRF_train_lab, True)
        for example in CRF_train_examples:
            totalExamples.append(example)


    #CRF_train_seq = concatenateAll(our_seq)
    #CRF_train_lab = concatenateAll(our_lab)
    #CRF_train_examples, NA = getCRFExamples(CRF_train_seq, CRF_train_lab, True)
    writeToFile("trainEx", totalExamples)

    totalTestExamples = []
    totalLabelOutput = []
    for i in range(len(our_test_seq)):
        CRF_test_seq = makeStr(our_test_seq[i])
        CRF_test_lab = makeStr(our_test_lab[i])
        CRF_test_examples, labelOutput = getCRFExamples(CRF_test_seq, CRF_test_lab, False)
        for example in CRF_test_examples:
            totalTestExamples.append(example)
        for lab in labelOutput:
            totalLabelOutput.append(lab)

    #CRF_test_seq = concatenateAll(our_test_seq)
    #CRF_test_lab = concatenateAll(our_test_lab)
    #CRF_test_examples, labelOutput = getCRFExamples(CRF_test_seq, CRF_test_lab, False)
    writeToFile("testEx", totalTestExamples)
    writeToFile("correctLabel", totalLabelOutput)

"""
Used to evaluate the prediction accuracy of the CRF testing
"""
    
def runCRFEvaluation(train_data, test_data):
    """
    print "\n\n======================="
    print "RUNNING THE MALLET CRF ON A TRAINING SET",
    print "CONTAINING %d EXAMPLES AND A TEST SET" %len(train_data),
    print "CONTAINING %d examples" %len(test_data)
    """
    print "%d," %len(train_data),
    
    tagged_seq = readTaggedOutput("Mallet/exampleOutput")
    actual_seq = readTaggedOutput("correctLabel")
    calcCRFError(tagged_seq, actual_seq)
    #print "=======================\n\n"

"""
Used to read in a file with the tagged sequences
"""
def readTaggedOutput(filename):
    if not path.exists(filename):
        print "Could not find the data set. Exiting."
        exit(0)

    taggedSeq = ""
    with open(filename, 'r') as infile:
        for line in infile:
            currChar = line.rstrip("\n")
            currChar = line.rstrip()
            taggedSeq += currChar
    return taggedSeq


"""
Used to carry out the calculation of how accurate the test output is,
with true positives, true negatives, false negatives, and false positives for each of the possible secondary structures
"""
def calcCRFError(taggedSeq, actualSeq):

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
                    trueNegH += 1
                elif actualSeq[i] == 'h':
                    falseNegH += 1
                    trueNegB += 1
                falsePosC += 1

        elif taggedSeq[i] == 'h':
            if taggedSeq[i] == actualSeq[i]:
                truePosH += 1
                trueNegC += 1
                trueNegB += 1
            else:
                if actualSeq[i] == 'c':
                    falseNegC += 1
                    trueNegB += 1
                elif actualSeq[i] == 'b':
                    falseNegB += 1
                    trueNegC += 1
                falsePosH += 1

        elif taggedSeq[i] == 'b':
            if taggedSeq[i] == actualSeq[i]:
                truePosB += 1
                trueNegC += 1
                trueNegH += 1
            else:
                if actualSeq[i] == 'c':
                    falseNegC += 1
                    trueNegH += 1
                elif actualSeq[i] == 'h':
                    falseNegH += 1
                    trueNegC += 1
                falsePosB += 1

    """
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

    print "%d," %truePosH,
    print "%d," %falsePosH,
    print "%d," %trueNegH,
    print "%d," %falseNegH,

    print "%d," %truePosB,
    print "%d," %falsePosB,
    print "%d," %trueNegB,
    print "%d," %falseNegB,

    print "%d," %truePosC,
    print "%d," %falsePosC,
    print "%d," %trueNegC,
    print "%d" %falseNegC
