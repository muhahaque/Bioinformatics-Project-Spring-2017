"""
Implement Hidden Markov Models using NLTK
"""

#importing HMM module
from nltk.tag import hmm

"""
Uses the NLTK package to run a Hidden Markov model
Creates a training set given sequences and tag
and is then trained on the training set and tested on the given test set
"""
def runHMM(train_data, test_data, words, tags):
    """
    print "RUNNING THE NLTK HMM ON A TRAINING SET",
    print "CONTAINING %d EXAMPLES AND A TEST SET" %len(train_data),
    print "CONTAINING %d examples" %len(test_data)
    """

    print "%d, " %len(train_data),
    #create a trainer
    #print "\n\nTAGS: ", tags, "\n\n"
    #print "\n\nWORDS: ", words, "\n\n"

    trainer = hmm.HiddenMarkovModelTrainer(tags, words)
    tagger = trainer.train_supervised(train_data)
    #print "\n\nTRANSITIONS: ", tagger._transitions.unicode_repr(), "\n\n"

    #print tagger

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

    
    for example in test_data:
        sequence = []
        actualLab = ""
        for entry in example:
            sequence.append(entry[0])
            actualLab += entry[1]
        bestPath = tagger.best_path(sequence)

        tag = ""
        for entry in bestPath:
            tag += entry

        truePosH, falsePosH, trueNegH, falseNegH, truePosB, falsePosB, trueNegB, falseNegB, truePosC, falsePosC, trueNegC, falseNegC = calcError(
                tag, actualLab)

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

    """
    print"\nH DATA:"
    print "True Positive H: %d" %totalTruePosH
    print "False Positive H: %d" %totalFalsePosH
    print "True Negative H: %d" %totalTrueNegH
    print "False Negative H: %d" %totalFalseNegH

    print"\nB DATA:"
    print "True Positive B: %d" %totalTruePosB
    print "False Positive B: %d" %totalFalsePosB
    print "True Negative B: %d" %totalTrueNegB
    print "False Negative B: %d" %totalFalseNegB

    print"\nC DATA:"
    print "True Positive C: %d" %totalTruePosC
    print "False Positive C: %d" %totalFalsePosC
    print "True Negative C: %d" %totalTrueNegC
    print "False Negative C: %d" %totalFalseNegC
    """

    return totalTruePosH, totalFalsePosH, totalTrueNegH, totalFalseNegH, totalTruePosB, totalFalsePosB, totalTrueNegB, totalFalseNegB, totalTruePosC, totalFalsePosC, totalTrueNegC, totalFalseNegC


"""
Oututs statistics that indicate the prediction accuracy of the model on the test set when compared to the actual secondary structures
"""
def calcError(taggedSeq, actualSeq):
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

    return truePosH, falsePosH, trueNegH, falseNegH, truePosB, falsePosB, trueNegB, falseNegB, truePosC, falsePosC, trueNegC, falseNegC

