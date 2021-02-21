# -*- coding: utf-8 -*-
"""
MadXTools : TableFS Tests
=========================

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

import os
import pytest
import numpy

from dummy import causeOSError

from madxtools import TableFS

@pytest.mark.tfs
def testTFS_FileError(monkeypatch, caplog, filesDir):
    """Check files reading error handling.
    """
    testFile = os.path.join(filesDir, "fodothin_90.tfs")
    with monkeypatch.context() as mp:
        mp.setattr("builtins.open", causeOSError)
        tfsObj = TableFS(testFile)
        assert tfsObj.fileName == testFile
        assert tfsObj.Data == {}
        assert "ERROR" in caplog.text

# END Test testTFS_FileError

@pytest.mark.tfs
def testTFS_LatticeFile(caplog, filesDir):
    """Check the reading of a lattice files.
    """
    testFile = os.path.join(filesDir, "fodothin_90.tfs")

    tfsObj = TableFS()
    assert tfsObj.fileName is None

    assert tfsObj.readFile(testFile)
    assert tfsObj.fileName == testFile
    assert tfsObj.metaData == {
        "CHARGE": 1.0,
        "DATE": "20/02/21",
        "DUMMY_INT": 42,
        "ENERGY": 7000.0,
        "GAMMA": 7460.52,
        "MASS": 0.9382,
        "NAME": "TWISS",
        "ORIGIN": "Linux 64",
        "PARTICLE": "PROTON",
        "PC": 6999.99,
        "SEQUENCE": "FODOTHIN",
        "TIME": "12.34.56",
        "TITLE": "no-title",
        "TYPE": "TWISS"
    }
    assert tfsObj.varNames == [
        "NAME", "KEYWORD", "S", "L", "BETX", "ALFX", "MUX", "BETY", "ALFY", "MUY"
    ]
    assert tfsObj.varTypes == [
        "%s", "%s", "%le", "%le", "%le", "%le", "%le", "%le", "%le", "%le"
    ]
    assert tfsObj.nLines == 7

    # Data Types
    assert isinstance(tfsObj.Data["NAME"][0], str)
    assert isinstance(tfsObj.Data["KEYWORD"][0], str)
    assert isinstance(tfsObj.Data["S"][0], str)
    assert isinstance(tfsObj.Data["L"][0], str)
    assert isinstance(tfsObj.Data["BETX"][0], str)
    assert isinstance(tfsObj.Data["ALFX"][0], str)
    assert isinstance(tfsObj.Data["MUX"][0], str)
    assert isinstance(tfsObj.Data["BETY"][0], str)
    assert isinstance(tfsObj.Data["ALFY"][0], str)
    assert isinstance(tfsObj.Data["MUY"][0], str)

    # Numpy Conversion
    # ================

    assert tfsObj.convertToNumpy()
    assert isinstance(tfsObj.Data["NAME"][0], str)
    assert isinstance(tfsObj.Data["KEYWORD"][0], str)
    assert isinstance(tfsObj.Data["S"][0], numpy.float)
    assert isinstance(tfsObj.Data["L"][0], numpy.float)
    assert isinstance(tfsObj.Data["BETX"][0], numpy.float)
    assert isinstance(tfsObj.Data["ALFX"][0], numpy.float)
    assert isinstance(tfsObj.Data["MUX"][0], numpy.float)
    assert isinstance(tfsObj.Data["BETY"][0], numpy.float)
    assert isinstance(tfsObj.Data["ALFY"][0], numpy.float)
    assert isinstance(tfsObj.Data["MUY"][0], numpy.float)

# END Test testTFS_LatticeFile

@pytest.mark.tfs
def testTFS_TrackFile(caplog, filesDir):
    """Check the reading of a track files.
    """
    testFile = os.path.join(filesDir, "fodothintrack_90.tfs.obs0001.p0001")

    tfsObj = TableFS()
    assert tfsObj.fileName is None

    assert tfsObj.readFile(testFile)
    assert tfsObj.fileName == testFile
    assert tfsObj.metaData == {
        "DATE": "20/02/21",
        "NAME": "TRACK.OBS0001.P0001",
        "ORIGIN": "5.06.01 Linux 64",
        "TIME": "23.40.21",
        "TITLE": "no-title",
        "TYPE": "TRACKOBS"
    }
    assert tfsObj.varNames == ["NUMBER", "TURN", "X", "PX", "Y", "PY", "T", "PT", "S", "E"]
    assert tfsObj.varTypes == ["%d", "%d", "%le", "%le", "%le", "%le", "%le", "%le", "%le", "%le"]
    assert tfsObj.nLines == 9

    # Data Types
    assert isinstance(tfsObj.Data["NUMBER"][0], str)
    assert isinstance(tfsObj.Data["TURN"][0], str)
    assert isinstance(tfsObj.Data["X"][0], str)
    assert isinstance(tfsObj.Data["PX"][0], str)
    assert isinstance(tfsObj.Data["Y"][0], str)
    assert isinstance(tfsObj.Data["PY"][0], str)
    assert isinstance(tfsObj.Data["T"][0], str)
    assert isinstance(tfsObj.Data["PT"][0], str)
    assert isinstance(tfsObj.Data["S"][0], str)
    assert isinstance(tfsObj.Data["E"][0], str)

    # Numpy Conversion
    # ================

    assert tfsObj.convertToNumpy()
    assert isinstance(tfsObj.Data["NUMBER"][0], numpy.int64)
    assert isinstance(tfsObj.Data["TURN"][0], numpy.int64)
    assert isinstance(tfsObj.Data["X"][0], numpy.float)
    assert isinstance(tfsObj.Data["PX"][0], numpy.float)
    assert isinstance(tfsObj.Data["Y"][0], numpy.float)
    assert isinstance(tfsObj.Data["PY"][0], numpy.float)
    assert isinstance(tfsObj.Data["T"][0], numpy.float)
    assert isinstance(tfsObj.Data["PT"][0], numpy.float)
    assert isinstance(tfsObj.Data["S"][0], numpy.float)
    assert isinstance(tfsObj.Data["E"][0], numpy.float)

# END Test testTFS_TrackFile
