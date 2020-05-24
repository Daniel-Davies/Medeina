import pickle
from config import *

def writeObjToDateStore(name,obj):
    with open(f'{BASEDIR}/{name}','wb') as fh:
        pickle.dump(obj,fh)

def retrieveObjFromStore(name):
    with open(f'{BASEDIR}/{name}','rb') as fh:
        existing = pickle.load(fh)
    
    return existing

def mostCommonInList(L):
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