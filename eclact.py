import time

isPrint = True

# ---------------------------------------------------------------------------------------------------


def getItemSetTransactionList(data_iterator):
    # List for all transactions
    # set for ItemSetFor particular transaction
    # use frozenset becuase we don't want to change itemSet while we are working on them
    transactionList = list()
    itemSet = set()

    itemDict = {}
    count = 0
    for record in data_iterator:
        transaction = list(record)
        transactionList.append(transaction)
        itemSet.update(transaction)
        
        for item in transaction:
            item = tuple([item])
            if item not in itemDict:
                itemDict[item] = set()
            itemDict[item].add(count)
        count = count+1

    updatedItemSet = set()


    for item in itemSet:
        # Generate 1-itemSets
        updatedItemSet.add(frozenset([item]))

    return itemDict, updatedItemSet, transactionList

# ---------------------------------------------------------------------------------------------------


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    kLengthDict = {}
    for item1 in itemSet:
        for item2 in itemSet:
            _union = sorted(set(item1).union(item2))
            if(len(_union) == length):
                kLengthDict[tuple(_union)] = set(
                    itemSet[item1]).intersection(itemSet[item2])

    return kLengthDict

# ---------------------------------------------------------------------------------------------------
def returnItemsWithMinSupport(itemDict, minSupportCount):
    # calculates the support for items in the itemSet
    # returns a subset of the itemSet each of whose elements satisfies the minimum support
    oneCSet = {}

    for item in itemDict:
        if(len(itemDict[item]) >= minSupportCount):
            # print(item,itemDict[item])
            oneCSet[item] = itemDict[item]

    return oneCSet

# ---------------------------------------------------------------------------------------------------




def runEclact(data_iter, minSupport):
    itemDict, itemSet, transactionList = getItemSetTransactionList(data_iter)
    
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support) and which satisfy minSupport

    # STEP1 geneterate C1 set (set for all items having support greater then minSupport)
    # oneCSet = returnItemsWithMinSupport(itemSet,
    #                                     transactionList,
    #                                     minSupport,
    #                                     freqSet,1)

    
    oneCSet = returnItemsWithMinSupport(
        itemDict, float(minSupport)*float(len(transactionList)))
    # print(float(minSupport)*float(len(transactionList)))
    # print(oneCSet)
    currentLSet = oneCSet
    if(isPrint):
        print("Lenght of C(", 1, "): ", len(currentLSet))
    k = 2
    # Lets calculate for C(k) where K>=2

    while(len(currentLSet) != 0):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(largeSet[k-1], k)


        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                float(minSupport)*float(len(transactionList)))

        currentLSet = currentCSet
        if(isPrint):
            print("Lenght of C(", k, "): ", len(currentLSet))
        k = k + 1

    
    toRetItems = []
    for key, value in largeSet.items():

        toRetItems.extend(value.keys())
                  
    return toRetItems

# ---------------------------------------------------------------------------------------------------

def dataFromFile(fileName):
    # return generator
    with open(fileName, 'r') as iterator:
        for line in iterator:
            line = line.strip()
            record = frozenset(line.split())
            yield record

# ---------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # FILE NAME

    dataSet1 = './small.csv'   # 100 transactions
    dataSet2 = './test.dat.txt'
    dataSet3 = './T10I4D100K.dat.txt'  # big dataSet
    dataSet4 = './T40I10D100K.dat.txt'

    fileName = dataSet3
    print("FileName:",fileName)
    minSupport = float(input("MinSupport:"))

    ########### DATA FROM FILE ########
    dataIterator = dataFromFile(fileName)

    old_time = time.time()
    if(isPrint):
        print("Start Time :", old_time)

    items = runEclact(dataIterator, minSupport)

    new_time = time.time()
    if(isPrint):
        print("End Time :", new_time)
        print("")
        print("Minimum Support:", minSupport)
        print("DataSet:", fileName)
        print("")
        print("Total Number of frequent sets:", len(items))
        print("Time in seconds :", new_time-old_time)
