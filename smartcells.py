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

class Poscells(dict):
    '''Trys to create a speedup class to search for cells in positions,
        useful for detect and colisions, also will add consider type of
        cell .
        wondering if is best to reset completely each time actaulize world,
        or just considere de changes, if the changes are small perhaps better
        list.sort than sorted(list)'''
    def __init__(self, world):
        super(Poscells, self).__init__()
        self.world=world
        self.cells=set(self.values())
        self._types={}
        self.deleted=set()
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.cells \
                                   if cell.tipo==_type)
        _mindict=[(e,e.pos.x,e.pos.y,e.name) for e in self.cells]
        _x=sorted (_mindict,key=itemgetter(1))
        _y=sorted (_mindict,key=itemgetter(2))
        #_k=sorted (_mindict,key=itemgetter(3))
        self._xk=[e[1] for e in _x]
        self._xd=[e[0] for e in _x]
        self._xn=[e[3] for e in _x]
        self._yk=[e[2] for e in _y]
        self._yd=[e[0] for e in _y]
        self._yn=[e[3] for e in _y]

    def refresh (self):
        #self.cells=set(self.values())
        #self.deleted=set()  revisar tendriamos que vaciar delete
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.cells \
                                   if cell.tipo==_type)
        _mindict=[(e,e.pos.x,e.pos.y,e.name) for e in self.cells]
        _x=sorted (_mindict,key=itemgetter(1))
        _y=sorted (_mindict,key=itemgetter(2))
        #_k=sorted (_mindict,key=itemgetter(3))
        self._xk=[e[1] for e in _x]
        self._xd=[e[0] for e in _x]
        self._xn=[e[3] for e in _x]
        self._yk=[e[2] for e in _y]
        self._yd=[e[0] for e in _y]
        self._yn=[e[3] for e in _y]

    def __setitem__(self,key,value):
        # the key shouldnt exist im condidering new but im not controlling
        # also is a light asignment im not actualizing position index
        #il leave it for a refresh
        super(Poscells, self).__setitem__(key,value)
        self.cells.add(value)

    def __delitem__(self,key):
        # the key should exist but im not controlling
        # also is a light delete im not actualizing position index
        #il leave it for a refresh
        self.deleted(self[key])
        self.cells.remove(self[key])

    def add_cel(self,cell):
        if cell not in self.cells:
            self._types[cell.tipo].add(cell)
            _ik=bs.bisect_left(self._xk, cell.pos[0])
            self._xk.insert(_ik,cell.pos[0])
            self._xd.insert(_ik,cell)
            self._xn.insert(_ik,cell.name)
            _ik=bs.bisect_left(self._yk, cell.pos[1])
            self._yk.insert(_ik,cell.pos[1])
            self._yd.insert(_ik,cell)
            self._yn.insert(_ik,cell.name)
            self[cell.name]=cell
            self.cells.add(cell)

    def del_cel(self,cell):
        # find it and take it decide if it is frecuent enough to create index
        if cell in self.cells:
            self._types[cell.tipo].remove(cell)
            _ik=self._xn.index(cell.name)
            self._xk.pop(_ik)
            self._xd.pop(_ik)
            self._xn.pop(_ik)
            _ik=self._yn.index(cell.name)
            self._yk.pop(_ik)
            self._yd.pop(_ik)
            self._yn.pop(_ik)
            # self.pop(cell.name)# we shouldn delete
            self.cells.remove(cell)

    def deleteByFunc(self,func): # use de func
        #a soft delete needs refresh to actualize indexex
        selec=set([cell for cell in self.cells if func(cell)])# bounded func only
        for cell in selec:
            self.cells.remove(cell)
            self.deleted.add(cell)

    def inrange(self,pos,rango,exclude=False,First=False,circle=False):
        if not exclude:
            excl=set()
        elif type(exclude) is  str: # is the type of cell
            excl=self._types[exclude]
        else:
            excl= set([exclude])         # is a cell
            if not self.world.collisions:
                return set() # deactivating collisions
        x,y= pos
        _ik=bs.bisect_left(self._xk, x-rango)
        _fk=bs.bisect_right(self._xk, x+rango,lo=_ik)
        _sx=set(self._xd[_ik:_fk])
        _ik=bs.bisect_left(self._yk, y-rango)
        _fk=bs.bisect_right(self._yk, y+rango,lo=_ik)
        _sy=set(self._yd[_ik:_fk])
        return (_sx & _sy)-excl

        # in future add use if circle=True filter by
        # (cell.pos.get_distance(pos) < rango)
        # but then it will make sense to use first parameter
        # to get only the first one

