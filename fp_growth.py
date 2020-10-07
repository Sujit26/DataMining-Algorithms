from itertools import chain, combinations
from collections import defaultdict
from typing import Iterator
import itertools
import time
isPrint = True

# ---------------------------------------------------------------------------------------------------


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}

    def incrementCount(self, countToAdd):
        self.count += countToAdd

    def disp(self, ind=1):
        print('  '*ind, self.name)
        for child in self.children.values():
            child.disp(ind+1)

    def visittree(self):
        output = []
        output.append(str(self.name) + " " + str(self.count))
        if len(self.children.keys()) > 0:
            for i in (list(self.children.keys())):
                output.append(self.children[i].visittree())
        return output


def updatePointerTable(testNode, targetNode):
    while(testNode.nodeLink != None):
        testNode = testNode.nodeLink

    testNode.nodeLink = targetNode


# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------


def updateTree(items, inTree, pointerTable, count):

    # increment count if item is already present in children
    if items[0] in inTree.children:
        inTree.children[items[0]].incrementCount(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # here we also have to update the pointerTable we have
        if(pointerTable[items[0]][1] == None):
            pointerTable[items[0]][1] = inTree.children[items[0]]
        else:
            inTree.children[items[0]].nodeLink = pointerTable[items[0]][1]
            pointerTable[items[0]][1] = inTree.children[items[0]]

    if (len(items) > 1):
        updateTree(items[1::], inTree.children[items[0]], pointerTable, count)
# ---------------------------------------------------------------------------------------------------


def buildTree(dataList, minSupportCount=1):
    pointerTable = {}

    # count the frewuency of item
    for transaction in dataList:
        for item in transaction:
            pointerTable[item] = pointerTable.get(item, 0) + 1

    # remove item less minimumCountSupport
    for item in list(pointerTable):
        if(pointerTable[item] < minSupportCount):
            del(pointerTable[item])

    freqItemSet = set(pointerTable.keys())
    # let start and create tree
    returnTree = treeNode('Null Set', 1, None)

    # if no item in itemSet return emptyTree
    if(len(freqItemSet) == 0):
        return returnTree,pointerTable

    for item in pointerTable:
        pointerTable[item] = [pointerTable[item], None]


    for tranSet in dataList:
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = pointerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(
                localD.items(), key=lambda p: p[1], reverse=True)]
            # populate tree with ordered freq itemset
            updateTree(orderedItems, returnTree, pointerTable, 1)

    return returnTree, pointerTable  # return tree and header table


# ---------------------------------------------------------------------------------------------------
def returnFrequentSet(tree:treeNode, pointerTable, minSupportCount,parent=None):

    if len(list(tree.children.keys())) == 0:
        return None

    result = []
    sorted_items = sorted(
        pointerTable.keys(), key=lambda k: pointerTable[k][0]
    )
    for item in sorted_items:
        fqset = set()
        if(parent != None):
            fqset = {item}.union(parent)
        else:
            fqset = {item}
        result.append(fqset)

        condtionalTranscations = returnContionalTransactions(pointerTable[item])
        contree, updatedPointerTable = buildTree(condtionalTranscations, minSupportCount)
        conwords = returnFrequentSet(contree,updatedPointerTable,minSupportCount,fqset)

        if conwords is not None:
            result.extend(conwords)
    return result

# ---------------------------------------------------------------------------------------------------


def returnContionalTransactions( pointerTable):
    conditional_txns = []
    current = pointerTable[1]
    while current!=None:
        line = []
        parent = current.parent
        while parent.parent != None:
            line.append(parent.name)
            parent = parent.parent
        line = line[::-1]
        for i in range(0, pointerTable[0]):
            conditional_txns.append(line)
        current = current.nodeLink
    return conditional_txns


def runFP(dataIterator,minSupport,transactions):

    

    tree, pointerTable = buildTree(
        transactions, float(minSupport)*float(len(transactions)))
    
    items = returnFrequentSet(tree, pointerTable, float(
        minSupport)*float(len(transactions)))
    return items

# ---------------------------------------------------------------------------------------------------


def dataFromFile(fileName):
    with open(fileName, 'r') as iterator:
        for line in iterator:
            line = line.strip()
            record = set(line.split())
            yield record
# ---------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # FILE NAME

    dataSet1 = './small.csv'   # 100 transactions
    dataSet2 = './test.dat.txt'
    dataSet3 = './T10I4D100K.dat.txt'  # big dataSet
    dataSet4 = './T40I10D100K.dat.txt'

    fileName = dataSet1
    minSupport = float(input("MinSupport:"))

    ########### DATA FROM FILE ########
    dataIterator = dataFromFile(fileName)
    transactions = list()
    for line in dataIterator:
        transactions.append(line)
    
    old_time = time.time()
    if(isPrint):
        print("Start Time :", old_time)

    items = runFP(dataIterator,minSupport,transactions)



    new_time = time.time()
    if(isPrint):
        print("End Time :", new_time)
        print("")
        print("Minimum Support:", minSupport)
        print("DataSet:", fileName)
        print("")
        print("Total Number of frequent sets:", len(items))
        print("Time in seconds :", new_time-old_time)
