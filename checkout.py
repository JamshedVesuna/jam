"""Better file syncing"""
"""      CHECKOUT     """

import os
import sys

from jam import Jam


def main(argv):
    j = Jam()
    j.checkout("/".join([os.getcwd(), argv]))

if __name__ == "__main__":
    main(sys.argv[1])
