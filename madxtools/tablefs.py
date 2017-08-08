import numpy as np
import re

def stripQuotes(inStr):
    outStr = inStr
    if inStr[0]=='"' and inStr[-1]=='"':
        outStr = inStr[1:-1]
    return outStr

class TwissTable:
    tfsName = None
    metadata = None
    variableNames = None
    variableTypes  = None
    data = None

    N = None

    def __init__(self,tfsName):

        self.metadata = {}
        self.variableNames = []
        self.variableTypes  = []
        self.data = {}
        
        self.N = 0

        #Read the file
        self.tfsName = tfsName
        tfsFile = open(tfsName,'r')
        for line in tfsFile.xreadlines():
            #print line
            if line[0]=="@":
                #Metadata
                ls = line.split()[1:]
                if ls[1][-1]=="d":
                    self.metadata[ls[0]] = int(ls[2])
                elif ls[1][-1]=="e":
                    self.metadata[ls[0]] = float(ls[2])
                elif ls[1][-1]=="s":
                    self.metadata[ls[0]] = stripQuotes(ls[2])
                else:
                    print "Unknown type '"+ls[1]+"' for metadata variable '"+ls[2]+"'"
                    exit(1)

            elif line[0]=="*":
                #Header/variable names
                ls = line.split()[1:]
                for l in ls:
                    self.variableNames.append(l)
                    self.data[l]=[]
            elif line[0]=="$":
                #Header/variable types
                ls = line.split()[1:]
                for l in ls:
                    self.variableTypes.append(l)
            else:
                #Data
                ls = line.split()
                assert len(ls) == len(self.variableNames)
                for (l,vn,vt) in zip(ls,self.variableNames,self.variableTypes):
                    self.data[vn].append(l)
                    if vt=="%s":
                        self.data[vn][-1]=stripQuotes(self.data[vn][-1])
                self.N += 1
                #break
        tfsFile.close()
        
        assert self.N==len(self.data["NAME"])
        
        #print self.metadata
        #print self.variableNames
        #print self.variableTypes
        #print
        #print self.data

    def convertToNumpy(self):
        "Convert data to NumPy arrays"
        for i in xrange(len(self.variableNames)):
            vn = self.variableNames[i]
            vt = self.variableTypes[i]
            
            if vt[-1]=="d":
                #print vn,vt,"int"
                self.data[vn] = np.asarray(self.data[vn],dtype="int")
            elif vt[-1]=="e":
                #print vn,vt,"float"
                self.data[vn] = np.asarray(self.data[vn],dtype="float")
            elif vt[-1]=="s":
                #print vn,vt,"string"
                self.data[vn] = np.asarray(self.data[vn],dtype="str")
            else:
                print "Unknown type '"+vt+"' for variable '"+vn+"'"
                exit(1)
        
        
    
    elements = None
    def sliced_rebuild(self,maxSearch=None):
        "Rebuild sliced elements."
        print "TwissTable::sliced_rebuild()..."
        currElementName  = None
        currElementStart = None
        currElementEnd   = None
        self.elements = {}
        for i in xrange(self.N):
            #look for sliced element
            name1 = self.data["NAME"][i]
            ns1 = name1.split("..")
            if len(ns1) == 2:
                if not ns1[0] in self.elements:
                    #print "Searching for", ns1[0],i

                    idx = int(ns1[1])
                    #assert idx == 1, "Error in Slice_Rebuild"
                    if idx != 1:
                        print "Warning in TwissTable::sliced_rebuild()"
                        print "\t Starting in the middle of a sliced element"
                        print "\t Element name = '"+ns1[0]+"'"
                        print "\t First idx =", idx

                    sMin = float(self.data["S"][i])
                    sMax = float(self.data["S"][i])
                    maxj = self.N
                    if maxSearch != None:
                        maxj = min(self.N,i+1+maxSearch)
                    for j in xrange(i+1, maxj):
                        name2 = self.data["NAME"][j]
                        ns2 = name2.split("..")
                        if len(ns2)==2:
                            if ns2[0] == ns1[0]:
                                #print "\t sub", ns2[0],j
                                idx += 1
                                assert idx == int(ns2[1])
                                sMax = float(self.data["S"][j])
                    #print ns1[0],sMin,sMax
                    self.elements[ns1[0]] = (sMin,sMax)
    
    def shift(self,newFirst):
        """"
        Shift the sequence such that the element newFirst is the first in the sequence.
        """
        
        #Find the index of the first element:
        idx = -1
        for (i,name) in zip(xrange(self.N),self.data["NAME"]):
            if name == newFirst:
                idx = i
                break
        if idx==-1:
            print "SHIFT("+self.tfsName+"): No element named '"+newFirst+"' found"
            exit(1)
        
        #Shift all the data arrays
        for d in self.data:
            self.data[d] = np.roll(self.data[d],-idx)
        
        #Rezero S
        s0 = self.data["S"][0]
        L  = self.metadata["LENGTH"]
        for i in xrange(self.N):
            self.data["S"][i] -= s0
            if self.data["S"][i] < 0:
                self.data["S"][i] += self.metadata["LENGTH"]
        if self.data["S"][-1] == 0.0:
            print "Warning in TwissTable::shift()"
            print "\t Shifting last element from 0.0 to", self.metadata["LENGTH"]
            self.data["S"][-1] = self.metadata["LENGTH"]

        #Kill "elements" array which is no longer valid
        self.elements = None

    def findDataIndex(self,columnName,pattern):
        ret = []
        for i in xrange(self.N):
        #for i in xrange(5):
            #print pattern, self.data[columnName][i]
            if re.match(pattern,self.data[columnName][i]):
                ret.append(i)
        return ret
