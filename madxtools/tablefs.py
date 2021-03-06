# -*- coding: utf-8 -*-
"""
MadXTools : TFS File Parser
===========================
Parses TFS files and converts them to Numpy arrays

This file is a part of MadXTools
Copyright 2017–2021 K.N. Sjobak, V. Berglyd Olsen, University of Oslo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import re

import numpy as np

logger = logging.getLogger(__name__)

class TableFS:

    def __init__(self, fileName=None):

        self.fileName  = fileName
        self.metaData  = {}
        self.varNames  = []
        self.varTypes  = []
        self.Data      = {}
        self.nLines    = 0
        self.sliceElem = {}
        self.hasNAME   = False

        if fileName is not None:
            self.readFile()

        return

    def clearData(self):
        """Clear the data arrays.
        """
        self.metaData  = {}
        self.varNames  = []
        self.varTypes  = []
        self.Data      = {}
        self.nLines    = 0
        self.sliceElem = {}
        self.hasNAME   = False

        return

    def readFile(self, fileName=None):
        """Parse a file and save the data in the data arrays. If a file
        name is not specified, the one specified in the contructor will
        be used instead.
        """
        if fileName is not None:
            self.fileName = fileName

        self.clearData()
        with open(self.fileName, "r") as tfsFile:
            for tfsLine in tfsFile:
                # Metadata
                if tfsLine[0] == "@":
                    spLines = tfsLine.lstrip().split(None, maxsplit=3)[1:]
                    if spLines[1].endswith("d"):
                        self.metaData[spLines[0]] = int(spLines[2])
                    elif spLines[1].endswith("le"):
                        self.metaData[spLines[0]] = float(spLines[2])
                    elif spLines[1].endswith("s"):
                        self.metaData[spLines[0]] = self._stripQuotes(spLines[2].strip())
                    else:
                        logger.warning(
                            "Unknown type '%s' for metadata variable '%s'" % (
                                spLines[1], spLines[2].strip()
                            )
                        )

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

                # Comment
                elif tfsLine.strip()[0] == "#":
                    pass

                # Data
                else:
                    spLines = tfsLine.split()
                    if len(spLines) != len(self.varNames):
                        raise IndexError("Mismatch between data lines and variable names")

                    for (spLine, vN, vT) in zip(spLines, self.varNames, self.varTypes):
                        self.Data[vN].append(spLine)
                        if vT == "%s":
                            self.Data[vN][-1] = self._stripQuotes(self.Data[vN][-1])
                    self.nLines += 1

            logger.info("%d lines of data read" % self.nLines)

        if "NAME" in self.Data:
            dataLines = len(self.Data["NAME"])
            self.hasNAME = True
        else:
            dataLines = len(self.Data[next(iter(self.Data.keys()), None)])
            self.hasNAME = False

        if self.nLines != dataLines:
            logger.warning("Mismatch between lines read (%d) and lines stored (%d)" % (
                self.nLines, dataLines
            ))

        return

    def convertToNumpy(self):
        """Convert data to NumPy arrays
        """
        for i in range(len(self.varNames)):

            vN = self.varNames[i]
            vT = self.varTypes[i]

            if vT.endswith("d"):
                self.Data[vN] = np.asarray(self.Data[vN], dtype="int")
            elif vT.endswith("le"):
                self.Data[vN] = np.asarray(self.Data[vN], dtype="float")
            elif vT.endswith("s"):
                self.Data[vN] = np.asarray(self.Data[vN], dtype="str")
            else:
                logger.error("Unknown type '%s' for variable '%s'" % (vT, vN))

        return

    def shiftSeq(self, newFirst):
        """Shift the sequence such that the element newFirst is the
        first in the sequence.
        """
        if not self.hasNAME:
            raise TypeError("This TFS table is not indexed by NAME")

        if not isinstance(self.Data["S"][0], float):
            raise ValueError("S column is not a number. Please run convertToNumpy().")

        # Find the index of the first element:
        idx = -1
        for (i, name) in zip(range(self.nLines), self.Data["NAME"]):
            if name == newFirst:
                idx = i
                break

        if idx == -1:
            raise KeyError("No element named '%s' found" % newFirst)

        # Shift all the data arrays
        for d in self.Data:
            self.Data[d] = np.roll(self.Data[d], -idx)

        # Rezero S
        s0 = self.Data["S"][0]

        for i in range(self.nLines):
            self.Data["S"][i] -= s0
            if self.Data["S"][i] < 0:
                self.Data["S"][i] += self.metaData["LENGTH"]

        if self.Data["S"][-1] == 0.0:
            logger.warning("Shifting last element from 0.0 to %d" % self.metaData["LENGTH"])
            self.Data["S"][-1] = self.metaData["LENGTH"]

        # Kill elements array which is no longer valid
        self.sliceElem = None

        return

    def findDataIndex(self, columnName, searchPattern):
        """Search a data column for a specific pattern
        """
        retVal = []
        for i in range(self.nLines):
            if re.match(searchPattern, self.Data[columnName][i]):
                retVal.append(i)

        return retVal

    ##
    #  Internal Functions
    ##

    def _stripQuotes(self, sVar):
        """Remove wrapping quotes from string.
        """
        if (sVar[0] == sVar[-1]) and sVar.startswith(("'", '"')):
            return sVar[1:-1]

        return sVar

## End Class TableFS
