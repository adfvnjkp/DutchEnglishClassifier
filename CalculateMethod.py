import math
from TreeNode import *
from Sentence import *


def entropy(ratio: float) -> float:
    """
    helper func return entropy value
    :param ratio: ratio of current TreeNode layer
    :return: entropy value
b
    """
    # found ratio = 1
    return ratio * math.log(ratio + 1e-9) / math.log(2) + (1 - ratio + 1e-9) * math.log(1 - ratio + 1e-9) / math.log(2)


def entropyCalc(sentenceList: list) -> float:
    """
    helper func calculate current layer of entropy
    :param sentenceList: list of sentences in current layer for classifying
    :return: exit with error (undivided in full divided case) or float value of entropy

    """
    # counter on curr layer
    enCounter = 0
    total = len(sentenceList)
    # loop accumulate counter
    for sentence in sentenceList:
        if sentence.language == "en":
            enCounter += 1
    if (enCounter == 0) or (enCounter == total):
        return 0

    return (-1) * entropy(float(enCounter) / total)


def dtGainCalc(sentenceList: list, column: int) -> float:
    """
    helper func calculate gain for decision tree
    :param sentenceList: list of sentences current layer
    :param column: index of attr column
    :return: gain value of current layer

    """
    # curr layer entropy without gain divide
    tempEntropy = entropyCalc(sentenceList)
    tList = []
    fList = []
    # loop on sentence instances
    for sentence in sentenceList:
        if sentence.attr[column]:
            tList.append(sentence)
        else:
            fList.append(sentence)

    tEntropy = entropyCalc(tList)
    fEntropy = entropyCalc(fList)
    return tempEntropy - (((len(tList) / len(sentenceList)) * tEntropy) + (len(fList) / len(sentenceList)) * fEntropy)


def adGianCalc(sentneceList: list, column: int, sentenceWeights: list) -> float:
    """
    helper func calculate gain for ada-boost
    :param sentneceList: list of sentence in curr layer
    :param column: attr column index
    :param sentenceWeights: list of weight tobe updated
    :return: float gain of current if current attr column selected

    """
    # initialization
    tEnCounter, fEnCounter, tNlCounter, fNlCounter = 0, 0, 0, 0
    total = len(sentneceList)

    # loop compare attr column gain, update each weight
    for sentence, weight in zip(sentneceList, sentenceWeights):
        if sentence.attr[column]:
            if sentence.language == "en":
                tEnCounter += weight
            else:
                tNlCounter += weight
        else:
            if sentence.language == "en":
                fEnCounter += weight
            else:
                fNlCounter += weight

    # sum up of t/ f cases ratio, amount
    sumup = tNlCounter + tEnCounter + fEnCounter + fNlCounter
    # compute Eng entropy, true Eng over true entropy, false Eng over false entropy
    tempEntropy = -1 * entropy((tEnCounter + fEnCounter) / sumup)
    tEntropy = -1 * entropy(tEnCounter / (tEnCounter + tNlCounter))
    fEntropy = -1 * entropy(fEnCounter / (fEnCounter + fNlCounter))
    # return gain res
    return tempEntropy - ((tEnCounter + tNlCounter) * tEntropy + (fEnCounter + fNlCounter) * fEntropy) / sumup


def dtBuild(sentenceList: list, columnList: list) -> TreeNode:
    """
    helper entrance build decision tree
    :param sentenceList: list of sentence current hold
    :param columnList: list of column correspond to left attr
    :return: TreNode

    """
    # counter initialization, fetch current layer's sentences' amount
    enCounter, nlCounter = 0, 0
    layerTotal = len(sentenceList)
    # TreeNode initialization for return
    newNode = TreeNode(-1, "")
    # gain, best gain attr, attr column list initialization
    maxGain = 0
    maxGainColumn = -1
    furtherColumnList = []

    # loop for current layer gain calc
    for sentence in sentenceList:
        if sentence.language == "en":
            enCounter += 1
        else:
            nlCounter += 1
    # for absolute divide
    if enCounter == layerTotal:
        newNode.setLanguage("en")
        return newNode
    if nlCounter == layerTotal:
        newNode.setLanguage("nl")
        return newNode

    # for no better gain divide
    for col in columnList:
        tempGain = dtGainCalc(sentenceList, col)
        if tempGain > maxGain:
            maxGain = tempGain
            maxGainColumn = col

    if maxGain == 0:
        if enCounter > nlCounter:
            newNode.setLanguage("en")
            return newNode
        else:
            newNode.setLanguage("nl")
            return newNode

    # for further construction with gain exist
    for column in columnList:
        if column != maxGainColumn:
            furtherColumnList.append(column)
    tList = []
    fList = []

    for sentence in sentenceList:
        if sentence.attr[maxGainColumn]:
            tList.append(sentence)
        else:
            fList.append(sentence)
    newNode.setAttr(maxGainColumn)
    newNode.setLeft(dtBuild(tList, furtherColumnList))
    newNode.setRight(dtBuild(fList, furtherColumnList))
    return newNode


def stumpTree(senteceList: list, sentenceWeights: list) -> TreeNode:
    """
    stump instance (TreeNode) forming func
    :param senteceList: list of sentence instances
    :param sentenceWeights: weight list to current sentenceList
    :return: stump instance

    """
    # initialization of best gain and its attr column index
    maxGain = 0
    maxGainColumn = -1
    for columnIndex in range(10):
        tempGain = adGianCalc(senteceList, columnIndex, sentenceWeights)
        # update
        if maxGain <= tempGain:
            maxGain = tempGain
            maxGainColumn = columnIndex
    # if no Gian improved, set gain attr column to the first attr
    if (maxGain == 0) or (maxGainColumn == -1):
        maxGainColumn = 0

    # loop for stat of sentences' weight update
    tEnWeight, tNlWeight, fEnWeight, fNlWeight = 0, 0, 0, 0
    for sentence, weight in zip(senteceList, sentenceWeights):
        if sentence.attr[maxGainColumn]:
            if sentence.language == "en":
                tEnWeight += weight
            else:
                tNlWeight += weight
        else:
            if sentence.language == "en":
                fEnWeight += weight
            else:
                fNlWeight += weight
    # new stump (TreeNode) initialization, processed tobe returned
    newNode = TreeNode(maxGainColumn, "")
    # compare current stump correctness ratio
    if tEnWeight > tNlWeight:
        stepStump = TreeNode(-1, "en")
        newNode.setLeft(stepStump)
    else:
        stepStump = TreeNode(-1, "nl")
        newNode.setLeft(stepStump)
    # compare current stump incorrectness ratio
    if fEnWeight > fNlWeight:
        stepStump = TreeNode(-1, "en")
        newNode.setRight(stepStump)
    else:
        stepStump = TreeNode(-1, "nl")
        newNode.setRight(stepStump)

    return newNode


def updateWeights(sentenceList: list, sentenceWeight: list, currNode: TreeNode) -> float:
    """
    helper func update weight, return updated weight to current stump
    :param sentenceList: list of sentence
    :param sentenceWeight: weight to each sentence
    :param currNode: stump
    :return: float value

    """
    tempError = 0
    # loop update weight according incorrect classification
    for sentence, weight in zip(sentenceList, sentenceWeight):
        if sentence.attr[currNode.attr]:
            if not sentence.language == currNode.left.language:
                tempError += weight
        else:
            if not sentence.language == currNode.right.language:
                tempError += weight
    # loop update weight according correct classification
    for index in range(len(sentenceList)):
        if sentenceList[index].attr[currNode.attr]:
            if sentenceList[index].language == currNode.left.language:
                sentenceWeight[index] = sentenceWeight[index] * tempError / (1 - tempError)
        else:
            if sentenceList[index].language == currNode.right.language:
                sentenceWeight[index] = sentenceWeight[index] * tempError / (1 - tempError)
    # stat accumulator
    sumup = 0
    for weight in sentenceWeight:
        sumup += weight
    for ij, weight in enumerate(sentenceWeight):
        sentenceWeight[ij] = weight / sumup

    # return call
    return math.log((1 - tempError) / tempError) / math.log(2)


def adBuild(senteceList: list, stumps: int):
    """
    entrance building ada-boost, update each stumps weight recursively
    :param senteceList: list of sentence instance
    :param stumps: amount of stumps available
    :return: not required, list memory operation

    """
    # list of stumps
    adStumps = [i for i in range(stumps)]   # initialization using int
    # list of stumps' weight
    adWeights = [float(i) for i in range(stumps)]  # initialization using int
    # weight for each sentence instance
    sentenceWeights = [(1.0 / len(senteceList)) for _ in range(len(senteceList))]

    # loop update each stump & sentence's weight
    for index in range(stumps):
        adStumps[index] = stumpTree(senteceList, sentenceWeights)
        adWeights[index] = updateWeights(senteceList, sentenceWeights, adStumps[index])

    # TODO :: guarding  if any stump still not initialized
    for item in adStumps:
        if type(item) == int:
            print("found Int in func::adBuild() -> adStumps!")

    # return call
    return adStumps, adWeights


def dtPredict(sentence: Sentence, currNode: TreeNode) -> str:
    """
    func prediction through decision tree
    :param currNode: TreeNode instance
    :param sentence: sentence text feature
    :return: str label "en" / "nl"

    """
    # if reach bottom of tree
    if currNode.language != "":
        return currNode.language
    # if nodes left for decision
    else:
        if sentence.attr[currNode.attr]:
            return dtPredict(currNode.left, sentence)
        else:
            return dtPredict(currNode.right, sentence)


def adPredict(sentence: Sentence, adStumps: list, adWeights: list) -> str:
    """
    func predict through ada-boost
    :param sentence:  sentence instance
    :param adStumps: stump list holding TreeNode instances
    :param adWeights: float list holding stumps' weight
    :return: str label "en" / "nl"

    """
    enWeight, nlWeight = 0, 0
    for treeNode, weight in zip(adStumps, adWeights):
        if sentence.attr[treeNode.attr]:
            if treeNode.left.language == "en":
                enWeight += weight
            else:
                nlWeight += weight
        else:
            if treeNode.right.language == "en":
                enWeight += weight
            else:
                nlWeight += weight

    # compare weight to return result
    if enWeight >= nlWeight:
        return "en"
    else:
        return "nl"
