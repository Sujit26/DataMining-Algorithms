import itertools
from operator import le
import time
from collections import defaultdict
# ---------------------------------------------------------------------------------------------------


def returtTransactionList(data_iterator):
    # List for all transactions
    # set for ItemSetFor particular transaction
    # use frozenset becuase we don't want to change itemSet while we are working on them
    itemSet = set()
    transactionList = list()

    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        itemSet.update(transaction)

    updatedItemSet = set()
    for item in itemSet:
        updatedItemSet.add(frozenset([item]))

    return updatedItemSet, transactionList

# ---------------------------------------------------------------------------------------------------


def filter_Itemset_By_MinimumSupport(itemSet, transactionList, minSupport, freqSet, k):
    # calculates the support for items in the itemSet
    # returns a subset of the itemSet each of whose elements satisfies the minimum support
    globalSet = defaultdict(int)
    _itemSet = set()

    for transaction in transactionList:
        tranction_K_Subsets = set(frozenset(element)
                                  for element in itertools.combinations(transaction, k))
        common_item_set = itemSet.intersection(tranction_K_Subsets)

        for item in common_item_set:
            freqSet[item] += 1
            globalSet[item] += 1

    for item, count in globalSet.items():

        if count >= (minSupport*len(transactionList)):
            _itemSet.add(item)

    return _itemSet

# ---------------------------------------------------------------------------------------------------


def returnFrequentItemSet(data_iter, minSupport):

    itemSet, transactionList = returtTransactionList(data_iter)

    # declration of frequentSet and intialize it with default dictionary
    freqSet = defaultdict(int)

    largeSet = dict()

    # STEP1 geneterate C1 set (set for all items having support greater then minSupport)
    c1_set = filter_Itemset_By_MinimumSupport(itemSet,
                                               transactionList,
                                               minSupport,
                                               freqSet,
                                               1)

    print("Lenght of C(", 1, "): ", len(c1_set))
    cK_set = c1_set
    k = 2

    # Lets calculate for C(k) where K>=2
    while(cK_set != set([])):
        largeSet[k-1] = cK_set

        # result = set(itertools.combinations(itemSet, k))

        cK_set = set(
            [i.union(j) for i in cK_set for j in itemSet if len(i.union(j)) == k])

        currentCSet = filter_Itemset_By_MinimumSupport(cK_set,
                                                       transactionList,
                                                       minSupport,
                                                       freqSet, k)
        cK_set = currentCSet
        print("Lenght of C(", k, "): ", len(cK_set))
        k = k + 1


    finalItemList = []
    for key, value in largeSet.items():
        finalItemList.extend([(tuple(item), int(freqSet[item]))
                           for item in value])
    return finalItemList

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


    ########## DATA FROM FILE ########
    dataIterator = dataFromFile(fileName)

    old_time = time.time()
    print("Start Time :", old_time)
    items = returnFrequentItemSet(dataIterator, minSupport)

    new_time = time.time()
    print("End Time :", new_time)
    
    print("")
    print("Minimum Support:", minSupport)
    print("DataSet:", fileName)
    print("")

    print("Total Number of frequent sets:", len(items))
    print("Time in seconds :", new_time-old_time)



    


        
