from .Web import Web
from .TrophicWeb import TrophicWeb
from .PollinationWeb import PollinationWeb 
from .webStore import WebStore
from .config import *
from os import path

if not path.exists(BASEDIR):
    WebStore()