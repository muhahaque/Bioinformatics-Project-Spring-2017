"""
implementation of HMM manually implemented for secondary structure prediction

by Muha and Tahmid
"""
def viterbi(sequence, states, transitions, emissions):
    matrix = {}
    stateMatrix = {}

    for state in states:
        matrix[state] = {}
        stateMatrix[state] = {}
        for i in range(len(sequence)+1):
            matrix[state][i] = -1 
            stateMatrix[state][i] = None

    matrix['begin'][0] = 1
    for state in states:
        if state != 'begin':
            matrix[state][0] = 0

    for i in range(1, len(sequence)+1):
        for state in states:
            maxVal = None
            maxState = None

            if state != 'begin' and state != 'end':
                maxVal, maxState = findMaxEmitting(i, sequence, state, states,
                        transitions, emissions, matrix)
            else:
                maxVal, maxState = findMaxSilent(i, state, states, 
                        transitions, matrix)

            matrix[state][i] = maxVal
            stateMatrix[state][i] = maxState

    output = traceBack(stateMatrix, len(sequence))
    return output

def findMaxEmitting(index, sequence, state, states, transitions, emissions, matrix):
    maxVal = -1
    maxState = None
    emVal = emissions[state][(sequence[index-1])]
    for state2 in states:
        curVal = matrix[state][index-1] * transitions[state2][state] * emVal
        if curVal >= maxVal:
            maxVal = curVal
            maxState = state2
    return maxVal, maxState
        
def findMaxSilent(index, state, states, transitions, matrix):
    maxVal = -1 
    maxState = None

    for state2 in states:
        curVal = matrix[state2][index] * transitions[state2][state]
        if curVal >= maxVal:
            maxVal = curVal
            maxState = state2
    return maxVal, maxState

def traceBack(stateMatrix, lastIndex):
    finalOutput = ""
    curr = 'end'
    index = lastIndex
    while curr != 'begin' and index != 0:
        curr = stateMatrix[curr][index]
        finalOutput += curr
        index = index-1
    return finalOutput


def createHMM(characters, sequences, labels):
    states = ['begin', 'end', 'h','b', 'c']
    transitions = {}
    emissions = {}

    for state in states:
        emissions[state] = {}
        for char in characters:
            emissions[state][char] = float(1)/21

    for state in states:
        transitions[state] = {}
        for state2 in states:
            transitions[state][state2] = float(1)/5 

    #run E step and run m step
    for i in range(10):
        em_cts, trans_cts = E_step(characters, states, sequences, labels)
        transitions, emissions, transChange, emChange = M_step(transitions, 
                emissions, states, characters, em_cts, trans_cts)
        #print "TRANS CHANGE: ", transChange
        #print "EM CHANGE: ", emChange
        #print "\n\n"

    return states, characters, emissions, transitions


def E_step(characters, states, sequences, labels):
    emission_counts = {}
    transition_counts = {}

    for state in states:
        emission_counts[state] = {}
        for char in characters:
            emission_counts[state][char] = 0

    for state in states:
        transition_counts[state] = {}
        for state2 in states:
            transition_counts[state][state2] = 0

    for i in range(len(sequences)):
        currSeq = sequences[i]
        for j in range(len(currSeq)):
            currChar = currSeq[j]
            currEmission = labels[i][j]
            emission_counts[currEmission][currChar] += 1

    for i in range(len(sequences)):
        currSeq = sequences[i]
        for j in range(0, len(currSeq) + 1):
            if j == 0:
                prevState = 'begin'
            else:
                prevState = labels[i][j-1]
            if j == len(currSeq):
                currState = 'end'
            else:
                currState = labels[i][j]
            transition_counts[prevState][currState] += 1

    return emission_counts, transition_counts

def M_step(transitions, emissions, states, characters, em_cts, trans_cts):
    emChange = 0
    transChange = 0

    for state in states:
        totalCount = 1 
        for char in characters:
            totalCount += em_cts[state][char]
        for char in characters:
            newEmissions = float(em_cts[state][char])/ totalCount
            emChange += abs(emissions[state][char] - newEmissions)
            emissions[state][char] = newEmissions

    for state in states:
        totalCount = 1 
        for state2 in states:
            totalCount += trans_cts[state][state2]
        for state2 in states:
            newTrans = float(trans_cts[state][state2])/ totalCount
            transChange += abs(transitions[state][state2] - newTrans)
            transitions[state][state2] = newTrans

    return transitions, emissions, transChange, emChange


def runOurHMM(trainSeq, trainLab, testSeq, testLab, words):
    states, characters, emissions, transitions = createHMM(words, 
            trainSeq, trainLab)

    print "RUNNING OUR IMPLEMENTED HMM ON A TRAINING SET",
    print "CONTAINING %d EXAMPLES AND A TEST SET" %len(trainSeq),
    print "CONTAINING %d examples" %len(testSeq)
    """
    print "\nTRANSITIONS"
    for state in states:
        for state2 in states:
            print state, " - ", state2, " ", transitions[state][state2]
    print "\n\n"

    print "\nEMISSIONS"
    for state in states:
        print emissions[state]
        print "\n"
    print "\n\n"
    """

    totalCorH = 0
    totalWroH = 0
    totalCorB = 0
    totalWroB = 0
    totalCorC = 0
    totalWroC = 0

    for i in range(len(testSeq)):
        seqList = testSeq[i]
        labList = testLab[i]
        actualSeq = ""
        actualLab = ""
        for j in range(len(seqList)):
            actualSeq += seqList[j]
            actualLab += labList[j]

        tagging = viterbi(actualSeq, states, transitions, emissions)
        correctH, wrongH, correctB, wrongB, correctC, wrongC = calcError(
                tagging, actualLab)

        totalCorH += correctH
        totalWroH += wrongH
        totalCorB += correctB
        totalWroB += wrongB
        totalCorC += correctC
        totalWroC += wrongC
        """
        print "\n\nTAG:\n", tagging, "\n"
        print "ACTUAL: \n", actualLab, "\n\n"
        """
        
    print "\n\nH predicted correctly: %d" %totalCorH
    print "H predicted incorrectly: %d\n" %totalWroH

    print "B predicted correctly: %d" %totalCorB
    print "B predicted incorrectly: %d\n" %totalWroB

    print "C predicted correctly: %d" %totalCorC
    print "C predicted incorrectly: %d\n" %totalWroC

        
def calcError(taggedSeq, actualSeq):
    correctH = 0
    wrongH = 0
    correctB = 0
    wrongB = 0
    correctC = 0
    wrongC = 0

    for i in range(len(taggedSeq)):
        if taggedSeq[i] == 'c':
            if taggedSeq[i] == actualSeq[i]:
                correctC += 1
            else:
                wrongC += 1
        elif taggedSeq[i] == 'h':
            if taggedSeq[i] == actualSeq[i]:
                correctH += 1
            else:
                wrongH += 1
        elif taggedSeq[i] == 'b':
            if taggedSeq[i] == actualSeq[i]:
                correctB += 1
            else:
                wrongB += 1
    return correctH, wrongH, correctB, wrongB, correctC, wrongC

