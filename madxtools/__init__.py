#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
MadXTools : Package Init
========================
Python Toolbox for Mad-X

This file is a part of MadXTools
Copyright 2017–2021 K.N. Sjobak, V. Berglyd Olsen, Univesity of Oslo

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
import logging

from .tablefs import TableFS

logger = logging.getLogger(__name__)

__all__ = ["TableFS"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017–2021 K.N. Sjobak, V. Berglyd Olsen, Univesity of Oslo"
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2021"
__maintainer__ = "Kyrre Ness Sjøbæk"
__email__      = "k.n.sjobak@fys.uio.no"
__status__     = "Development"
__credits__    = ["Veronica Berglyd Olsen", "Kyrre Ness Sjøbæk"]

logLevel = logging.INFO

# Initiating logging
def _initLogging(logObj):
    strLevel = os.environ.get("MADXTOOLS_LOGLEVEL", "INFO")
    if hasattr(logging, strLevel):
        logLevel = getattr(logging, strLevel)
    else:
        print("Invalid logging level '%s' in environment variable MADXTOOLS_LOGLEVEL" % strLevel)
        logLevel = logging.INFO

    if logLevel < logging.INFO:
        logFormat = "[{asctime:s}] {levelname:8s} {message:}"
    else:
        logFormat = "{levelname:8s} {message:}"

    logFmt = logging.Formatter(fmt=logFormat, style="{")

    cHandle = logging.StreamHandler()
    cHandle.setLevel(logLevel)
    cHandle.setFormatter(logFmt)

    logObj.setLevel(logLevel)
    logObj.addHandler(cHandle)

    if logLevel < logging.INFO:
        logger.info("This is MadX Tools version %s" % __version__)

    return

# Logging Setup
logger = logging.getLogger(__name__)
_initLogging(logger)
