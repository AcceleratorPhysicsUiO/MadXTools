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

__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.1.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "v.k.b.olsen@cern.ch"
__status__     = "Development"

logging.basicConfig(
    format  = "[%(asctime)s] [%(name)20s:%(lineno)-4d] %(levelname) :: %(message)s",
    level   = logging.DEBUG,
#   datefmt = "%Y-%m-%d %H:%M:%S",
    datefmt = "%H:%M:%S",
)

if __name__ == '__main__':
    print("Mad-X Tools")
