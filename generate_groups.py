import codecs
import sys
import os

def convertRank(pRating):
    if (pRating >= 2100):
        return "%dd" % ((pRating - 2100) / 100 + 1);
    else:
        return "%dk" % ((2100 - pRating) / 100 + 1);

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
    iOverlapIDs = loadList("overlap_ids.txt")
    iCurrentRatings = loadList("current_ratings.txt")
    iPastPerformanceRaw = loadList("past_performance.txt")
    
    
    iPastPerformance = []
    
    for i in range(len(iPastPerformanceRaw)):
        iPastPerformance.append(list(map(int,iPastPerformanceRaw[i].split('\t'))));
    
    iNumPlayers = len(iCurrentIDs)
    
    for i in range(iNumPlayers):
        iNames[i] = iNames[i].replace("\r\n", "")
        iNames[i] = iNames[i].replace("\n", "")
        iCurrentIDs[i] = int(iCurrentIDs[i])
        iCurrentRatings[i] = float(iCurrentRatings[i])
        
    iPastIndex = [-1] * iNumPlayers
    iMaxTier = []
    
    for i in range(len(iCurrentIDs)):
        iTier = 10
        for j in range(len(iPastPerformance)):
            #print iPastPerformance[j][0];
            if iCurrentIDs[i] == iPastPerformance[j][0]:
                print "Yes!"
                iPastIndex[i] = j;
                if (iPastPerformance[j][2] <= 2):
                    iTier = iPastPerformance[j][1] - 1;
                elif (iPastPerformance[j][2] <= 5):
                    iTier = iPastPerformance[j][1];
                else:
                    iTier = iPastPerformance[j][1] + 1;
                if (iTier < 1):
                    iTier = 1;
                break;
        iMaxTier.append(iTier);
            
        
    fGroups = codecs.open("grouping.txt", "w", "utf-8");
    fHtml = codecs.open("grouping.html", "w", "utf-8");
    iNumAssigned = 0
    
    
    iCurrentTier = 1;
    iSlot = 10;
    
    iAssignedTier = [10] * iNumPlayers
    iEquivalentRating = [-3000] * iNumPlayers
    iBonus = [0] * iNumPlayers;
    
    while (iNumAssigned < iNumPlayers):    
        iOccupied = 0;
        for i in range(iNumPlayers):
            if iAssignedTier[i] == 10 and iMaxTier[i] <= iCurrentTier:
                iAssignedTier[i] = iCurrentTier;
                iEquivalentRating[i] = iCurrentRatings[i];
                iOccupied += 1;
                iNumAssigned += 1;
                if iOccupied > iSlot:
                    print "[Error] Not enough slot."
        if iOccupied < iSlot:
            iCandidates = [];

            for i in range(iNumPlayers):
                if iAssignedTier[i] == 10:
                    
                    iRating = iCurrentRatings[i];
                    j = iPastIndex[i];
                    tBonus = 0;
                    if (j != -1):
                        print "%s %d" % (iNames[i], iPastPerformance[j][2])
                        if iPastPerformance[j][1] == iCurrentTier: #Relegated
                            if (iPastPerformance[j][2] == 6):
                                tBonus = 300;
                            elif (iPastPerformance[j][2] == 7):
                                tBonus = 200;
                            elif (iPastPerformance[j][2] == 8):
                                tBonus = 100;
                        elif (iPastPerformance[j][1] == iCurrentTier + 1): #Lower league
                            if (iPastPerformance[j][2] == 3):
                                tBonus = 300;
                            elif (iPastPerformance[j][2] == 4):
                                tBonus = 200;
                            elif (iPastPerformance[j][2] == 5):
                                tBonus = 100;
                    iRating += tBonus;
                    
                    iCandidates.append((i, iRating))
                    
            #sort
            iCandidates = sorted(iCandidates, key=lambda iCandidates : iCandidates[1], reverse = True);
            
            iTop = iSlot - iOccupied;
            if iTop > len(iCandidates):
                iTop = len(iCandidates)
            
            for i in range(iTop):
                iAssignedTier[iCandidates[i][0]] = iCurrentTier
                iEquivalentRating[iCandidates[i][0]] = iCandidates[i][1]
                if iPastIndex[iCandidates[i][0]] == -1:
                    iBonus[iCandidates[i][0]] = 0
                else:
                    iBonus[iCandidates[i][0]] = iEquivalentRating[iCandidates[i][0]] - iCurrentRatings[iCandidates[i][0]]
                iNumAssigned += 1;
        
        iPlayers = [];
        
        fGroups.writelines("[Tier %d]:\n" % iCurrentTier);
        for i in range(iNumPlayers):
            if iAssignedTier[i] == iCurrentTier:
                fGroups.writelines("%s\t%.3f\t%.0f\n" % (iNames[i], iEquivalentRating[i], iBonus[i]));
                iPlayers.append((i, iCurrentRatings[i]))
                #if iPastIndex[iCandidates[i][0]] == -1:
                
        iPlayers = sorted(iPlayers, key=lambda iPlayers :iPlayers[1], reverse = True);
        nGroups = iSlot / 10;
        nRows = 10;
        if len(iPlayers) < iSlot:
            if len(iPlayers) * 2 < iSlot:
                nGroups = len(iPlayers) / 5;
                nRows = 5;
                if nGroups * 5 < len(iPlayers):
                    nRows += 1;
            else:
                nRows = len(iPlayers) / 16;
                if nRows * 16 < len(iPlayers):
                    nRows += 1;
        iGroups = [];
        for c in range(nGroups):
            iGroups.append([]);        
        c = 0;
        tInc = 1;
        for i in range(len(iPlayers)):
            iGroups[c].append((i, iPlayers[i]));
            c += tInc;
            if (c == nGroups):
                c = nGroups - 1;
                tInc = -1;
            elif (c == -1):
                c = 0;
                tInc = 1;
        
        fHtml.writelines("<b>Tier %d</b>\n" % iCurrentTier);
        fHtml.writelines("<table style=\"text-align:center;\" border='2'>\n");
        
        fHtml.writelines("\t<tr>\n");
        iNameTier = chr(ord('A') + iCurrentTier - 1);
        
        if iCurrentTier == 1:
            fHtml.writelines("\t\t<th colspan=7>Group A</th>")
        else:
            for c in range(nGroups):
                fHtml.writelines("\t\t<th colspan=7>Group %c%d</th>" % (iNameTier, c + 1));        
        fHtml.writelines("\n\t</tr>\n")
        
        fHtml.writelines("\t<tr>\n");
        
        for c in range(nGroups):
            fHtml.writelines("\t\t<th>Seed</th><th>ID</th><th>Rank</th><th>Rating</th><th>PT</th><th>PGR</th><th>Bonus</th>");        
        fHtml.writelines("\n\t</tr>\n")
        
        for r in range(nRows):
            fHtml.writelines("\t<tr>\n");
            for c in range(nGroups):
                fHtml.writelines("\t\t<td>")
                if r < len(iGroups[c]):
                    fHtml.writelines("%d" % (iGroups[c][r][0] + 1));
                fHtml.writelines("</td>")
                
                fHtml.writelines("<td>");
                if r < len(iGroups[c]):
                    fHtml.writelines("%s" % iNames[iGroups[c][r][1][0]])
                fHtml.writelines("</td>")
                
                fHtml.writelines("<td>")
                if r < len(iGroups[c]):
                    fHtml.writelines("%s" % convertRank(iCurrentRatings[iGroups[c][r][1][0]]));
                fHtml.writelines("</td>");
                
                fHtml.writelines("<td>")
                if r < len(iGroups[c]):
                    fHtml.writelines("%.3f" % iGroups[c][r][1][1]);
                fHtml.writelines("</td>")
                
                fHtml.writelines("<td>");
                if r < len(iGroups[c]):
                    j = iPastIndex[iGroups[c][r][1][0]];
                    if (j == -1):
                        fHtml.writelines("-");
                    else:
                        fHtml.writelines("%d" % iPastPerformance[j][1]);
                fHtml.writelines("</td>")
                
                fHtml.writelines("<td>");
                if r < len(iGroups[c]):
                    j = iPastIndex[iGroups[c][r][1][0]];
                    if (j == -1):
                        fHtml.writelines("-");
                    else:
                        fHtml.writelines("%d" % iPastPerformance[j][2]);
                fHtml.writelines("</td>")
                
                fHtml.writelines("<td>");
                if r < len(iGroups[c]):
                    fHtml.writelines("%d" % iBonus[iGroups[c][r][1][0]]);
                fHtml.writelines("</td>")
            fHtml.writelines("\n\t</tr>\n");
        
        fHtml.writelines("</table>\n");
        iCurrentTier += 1;
        iSlot *= 2;
    
    fGroups.close();
    fHtml.close();