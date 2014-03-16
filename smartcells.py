# -*- coding: utf-8 -*-
#import numpy
# should be faster but we have to install
# could try to make all operations as matrixes of numpy and then select best
#for distances

#also try to use binary teers but not implemented directly we have to get from pypi
# and also slower than dicts
# how about orderedDict, the problem is to find the next element

# how about using bisect for an index to the dict


from operator import itemgetter, attrgetter
import bisect as bs

class Poscells(object):
    '''Trys to create a speedup class to search for cells in positions,
        useful for detect and colisions, also will add consider type of
        cell .
        wondering if is best to reset completely each time actaulize world,
        or just considere de changes, if the changes are small perhaps better
        list.sort than sorted(list)'''
    def __init__(self, cells):
        self._dict=cells
        _mindict=[(e,e.pos.x,e.pos.y) for e in cells.values()]
        _x=sorted (_mindict,key=itemgetter(1))
        _y=sorted (_mindict,key=itemgetter(2))
        self._xk=[e[1] for e in _x]
        self._xd=[e[0] for e in _x]
        self._yk=[e[2] for e in _y]
        self._yd=[e[0] for e in _y]

    def reset (self,cells):
        self._dict=cells
        _mindict=[(e,e.pos.x,e.pos.y) for e in cells.values()]
        _x=sorted (_mindict,key=itemgetter(1))
        _y=sorted (_mindict,key=itemgetter(2))
        self._xk=[e[1] for e in _x]
        self._xd=[e[0] for e in _x]
        self._yk=[e[2] for e in _y]
        self._yd=[e[0] for e in _y]

    def inrange(self,pos,rango):
        x,y= pos
        _ik=bs.bisect_left(self._xk, x-rango)
        _fk=bs.bisect_right(self._xk, x+rango,lo=_ik)
        _sx=set(self._xd[_ik:_fk])
        _ik=bs.bisect_left(self._yk, y-rango)
        _fk=bs.bisect_right(self._yk, y+rango,lo=_ik)
        _sy=set(self._yd[_ik:_fk])
        return _sx & _sy

    def add_cel(self,cell):
        _ik=bs.bisect_left(self._xk, cell.pos[0])
        self._xk.insert(_ik,cell.pos[0])
        self._xd.insert(_ik,cell)
        _ik=bs.bisect_left(self._yk, cell.pos[1])
        self._yk.insert(_ik,cell.pos[1])
        self._yd.insert(_ik,cell)
        self._dict[cell.name]=cell

    def del_cel(self,cell):
        # find it and take it decide if it is frecuent enough to create index
        _ik=bs.bisect_left(self._xk, cell.pos[0])
        self._xk.insert(_ik,cell.pos[0])
        self._xd.insert(_ik,cell)
        _ik=bs.bisect_left(self._yk, cell.pos[1])
        self._yk.insert(_ik,cell.pos[1])
        self._yd.insert(_ik,cell)
        self._dict[cell.name]=cell
