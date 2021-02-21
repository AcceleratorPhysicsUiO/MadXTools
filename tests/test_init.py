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
import logging

from madxtools import _initLogging

@pytest.mark.core
def testCore_InitLogging():
    """Test package initialisation.
    """
    os.environ["MADXTOOLS_LOGLEVEL"] = "DEBUG"
    logger = logging.getLogger(__name__)
    _initLogging(logger)
    assert logger.getEffectiveLevel() == logging.DEBUG

    os.environ["MADXTOOLS_LOGLEVEL"] = "INVALID"
    logger = logging.getLogger(__name__)
    _initLogging(logger)
    assert logger.getEffectiveLevel() == logging.INFO

# END Test testCore_InitLogging
