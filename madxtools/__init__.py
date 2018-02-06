#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""Python Toolbox for Mad-X

  Mad-X Tools
 =============
  Python Toolbox for Mad-X
  By: Veronica Berglyd Olsen
      CERN (BE-ABP-HSS)
      Geneva, Switzerland

"""

import logging

# Submodules
from .tablefs import TableFS

logger = logging.getLogger(__name__)

__all__ = ["TableFS"]

# Package Meta
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Development"

logLevel = logging.INFO

if logLevel == logging.DEBUG:
    logging.basicConfig(
        format  = "[%(asctime)s] %(name)s:%(lineno)d %(levelname)s: %(message)s",
        level   = logging.DEBUG,
        datefmt = "%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        format  = "%(levelname)s: %(message)s",
        level   = logLevel,
        datefmt = "%H:%M:%S",
    )

if __name__ == '__main__':
    print("Mad-X Tools")
