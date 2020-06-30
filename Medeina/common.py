from .config import *
import itertools
import operator 
import json 
import copy 
import msgpack

def writeObjToDateStore(directory,name,obj):
    with open(f'{directory}/{name}','wb') as fh:
        packed = msgpack.packb(obj)
        fh.write(packed)

def retrieveObjFromStore(directory,name):
    with open(f'{directory}/{name}','rb') as fh:
        byteData = fh.read()
        existing = msgpack.unpackb(byteData,strict_map_key=False)
    
    return existing

def mostCommonInList(L,defaultBlank=''):
  if len(L) == 0: return defaultBlank
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  return max(groups, key=_auxfun)[0]

def prettyPrintDict(dict_):
    for k, v in dict_.items():
        print(str(k) + " --- " + str(v))
    
def serialise(pythonObj):
    return copy.deepcopy(pythonObj)