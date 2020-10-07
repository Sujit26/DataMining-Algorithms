import random
import csv


finalData = list()
transactionLength = int(input("Enter number of transactions:"))
# transactionLength = 30


# average width of the transactions,
averageTransactionWidth = int(input("Enter average width of transactions:"))
# averageTransactionWidth = 10

itemSetLength = int(input("Itemset length:"))
# itemSetLength = 40

print("################## FINAL DATA  ##################")
itemSet = set()

for i in range(0,itemSetLength):
    itemSet.add(i)

for i in range(0,int(transactionLength/2)):
    randomLength = random.randint(int(averageTransactionWidth/2),averageTransactionWidth-1)
    l1 = averageTransactionWidth-randomLength+2
    l2 = averageTransactionWidth+randomLength-2
    _trasaction = random.sample(range(0, itemSetLength), l1)

    finalData.append(_trasaction)
    
    __trasaction = random.sample(range(0, itemSetLength), l2)
    finalData.append(__trasaction)



    
with open('FINALDATA.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    print("################ DATA IN PROCESSING ###############")
    for transaction in finalData:
        writer.writerow(transaction)
        # print(finalData[transaction])
    print("################## DATA IS READY ##################")
