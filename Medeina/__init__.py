from os import path
from .Web import Web
from .TrophicWeb import TrophicWeb
from .PollinationWeb import PollinationWeb
from .webStore import WebStore
from .config import *

if not path.exists(BASEDIR):
    WebStore()
