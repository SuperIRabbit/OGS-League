import codecs
import sys
import os

def loadList(pNameFile):   
    iList = []
    with codecs.open(pNameFile, "r", "utf-8") as f:
        for line in f:
            iList.append(line)
    return iList
            
if __name__ == "__main__":
    iCurrentIDs = loadList("current_ids.txt")
    iPreviousIDs = loadList("previous_ids.txt")
    iNames = loadList("current_names.txt")
    
    #iOldIDs = set(iCurrentIDs) & set(iPreviousIDs)
    
    f1 = open("overlap_ids.txt","w")
    f2 = open("overlap_names.txt","w")
    
    for i in range(len(iCurrentIDs)):
        if (iCurrentIDs[i] in set(iPreviousIDs)):
            f1.writelines(iCurrentIDs[i])
            f2.writelines(iNames[i])
            
    f1.close()
    f2.close()
    