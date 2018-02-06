# -*- coding: utf-8 -*
"""TFS File Parser

  Mad-X Tools - TFS File Parser
 ===============================
  Parses TFS files and converts them to Numpy arrays
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

  Based on Kyrre Ness Sjøbæk's class TwissTable.py
  https://github.com/kyrsjo/MadxTools

  Updated to work with Python3

"""

import logging
import numpy   as np
import re

logger = logging.getLogger(__name__)

class TableFS:
    
    fileName  = None
    metaData  = None
    varNames  = None
    varTypes  = None
    Data      = None
    
    nLines    = None
    sliceElem = None
    
    def __init__(self, fileName):
        
        self.fileName = fileName
        self.metaData = {}
        self.varNames = []
        self.varTypes = []
        self.Data     = {}
        
        self.nLines   = 0
        
        # Read File
        with open(fileName,'r') as tfsFile:
            
            for tfsLine in tfsFile:
                
                # Metadata
                if tfsLine[0] == "@":
                    spLines = tfsLine.split()[1:]
                    if   spLines[1][-1] == "d":
                        self.metaData[spLines[0]] = int(spLines[2])
                    elif spLines[1][-1] == "e":
                        self.metaData[spLines[0]] = float(spLines[2])
                    elif spLines[1][-1] == "s":
                        self.metaData[spLines[0]] = self.stripQuotes(spLines[2])
                    else:
                        logger.error("Unknown type '%s' for metadata variable '%s'" % (spLines[1], spLines[2]))
                        return False
                        
                # Header/Variable Names
                elif tfsLine[0] == "*":
                    spLines = tfsLine.split()[1:]
                    for spLine in spLines:
                        self.varNames.append(spLine)
                        self.Data[spLine] = []
                    
                # Header/Variable Type
                elif tfsLine[0] == "$":
                    spLines = tfsLine.split()[1:]
                    for spLine in spLines:
                        self.varTypes.append(spLine)
                
                # Data
                else:
                    spLines = tfsLine.split()
                    assert len(spLines) == len(self.varNames)
                    for (spLine,vN,vT) in zip(spLines,self.varNames,self.varTypes):
                        self.Data[vN].append(spLine)
                        if vT == "%s":
                            self.Data[vN][-1] = self.stripQuotes(self.Data[vN][-1])
                    self.nLines += 1
                
            logger.info("%d lines of data read" % self.nLines)
            
        assert self.nLines == len(self.Data["NAME"])
        
        return
        
        
    def convertToNumpy(self):
        """
        Convert data to NumPy arrays
        """
        
        for i in range(len(self.varNames)):
            
            vN = self.varNames[i]
            vT = self.varTypes[i]
            
            if   vT[-1] == "d":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="int")
            elif vT[-1] == "e":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="float")
            elif vT[-1] == "s":
                self.Data[vN] = np.asarray(self.Data[vN],dtype="str")
            else:
                logger.error("Unknown type '%s' for variable '%s'" % (vT, vN))
                return False
            
        return True
        
    def slicedRebuild(self, maxSearch=None):
        """
        Rebuild sliced elements
        """
        
        logger.info("Rebuilding sliced elements.")
        
        currElementName  = None
        currElementStart = None
        currElementEnd   = None
        self.sliceElem   = {}
        
        for i in range(self.nLines):
            
            # Look for sliced element
            
            name1 = self.Data["NAME"][i]
            ns1   = name1.split("..")
            
            if len(ns1) == 2:
                if not ns1[0] in self.elements:
                    idx = int(ns1[1])
                    if idx != 1:
                        logger.warn("Starting in the middle of a sliced element\t Element name = '%s'\t First idx = %d" % (ns1[0], idx))
                    
                    sMin = float(self.Data["S"][i])
                    sMax = float(self.Data["S"][i])
                    maxJ = self.nLines
                    
                    if maxSearch != None:
                        maxJ = min(self.nLines,i+1+maxSearch)
                    
                    for j in range(i+1, maxJ):
                        name2 = self.Data["NAME"][j]
                        ns2   = name2.split("..")
                        if len(ns2)==2:
                            if ns2[0] == ns1[0]:
                                idx += 1
                                assert idx == int(ns2[1])
                                sMax = float(self.Data["S"][j])
                    
                    self.sliceElem[ns1[0]] = (sMin,sMax)
        
        return True
        
    def shiftSeq(self, newFirst):
        """
        Shift the sequence such that the element newFirst is the first in the sequence.
        """
        
        # Find the index of the first element:
        idx = -1
        for (i,name) in zip(range(self.nLines),self.Data["NAME"]):
            if name == newFirst:
                idx = i
                break
        if idx==-1:
            logger.warn("No element named '%s' found" % newFirst)
            return False
        
        # Shift all the data arrays
        for d in self.Data:
            self.Data[d] = np.roll(self.Data[d],-idx)
        
        # Rezero S
        s0 = self.Data["S"][0]
        L  = self.metaData["LENGTH"]
        
        for i in range(self.nLines):
            self.Data["S"][i] -= s0
            if self.Data["S"][i] < 0:
                self.Data["S"][i] += self.metaData["LENGTH"]
        
        if self.Data["S"][-1] == 0.0:
            logger.warn("Shifting last element from 0.0 to %d" % self.metaData["LENGTH"])
            self.Data["S"][-1] = self.metaData["LENGTH"]
        
        # Kill elements array which is no longer valid
        self.sliceElem = None
        
        return True
        
    def findDataIndex(self, columnName, searchPattern):
        """
        Search a data column for a specific pattern
        """
        
        retVal = []
        
        for i in range(self.nLines):
            if re.match(searchPattern,self.Data[columnName][i]):
                retVal.append(i)
        
        return retVal
        
    #
    # Internal Functions
    #
    
    def stripQuotes(self, sVar):
        
        if (sVar[0] == sVar[-1]) and sVar.startswith(("'", '"')):
            return sVar[1:-1]
        
        return sVar
    
## End Class TableFS
