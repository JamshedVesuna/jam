"""Better file syncing"""
"""       STASH       """

import os
import sys

from jam import Jam


def main(argv):
    j = Jam()
    j.stash("/".join([os.getcwd(), argv]), "".join([j.REMOTEPwd, argv]))

if __name__ == "__main__":
    main(sys.argv[1])
