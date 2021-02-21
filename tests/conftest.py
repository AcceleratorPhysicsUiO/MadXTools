# -*- coding: utf-8 -*-
"""
MadXTools : Test Suite Configuration
====================================

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

import sys
import pytest
import shutil
import os

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

##
#  Core Test Folders
##

@pytest.fixture(scope="session")
def tmpDir():
    """A temporary folder for the test session. This folder is
    presistent after the test so that the status of generated files can
    be checked. The folder is instead cleared before a new test session.
    """
    testDir = os.path.dirname(__file__)
    theDir = os.path.join(testDir, "temp")
    if os.path.isdir(theDir):
        shutil.rmtree(theDir)
    if not os.path.isdir(theDir):
        os.mkdir(theDir)
    return theDir

@pytest.fixture(scope="session")
def filesDir():
    """The folder where additional test files are stored.
    """
    testDir = os.path.dirname(__file__)
    theDir = os.path.join(testDir, "files")
    return theDir
