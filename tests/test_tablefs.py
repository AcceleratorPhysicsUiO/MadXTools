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

# END Test testTFS_LatticeFile
