# libs
from os.path import abspath, dirname
from pathlib import Path

# function
def G3nius_Location():
    Location = dirname(abspath(__file__))
    Location = str(Path(Location).parent.parent)
    return Location