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
    def __init__(self, world,*args):
        super(Poscells, self).__init__(*args)
        self.world=world
        self.cells=set(self.values())
        self._types={}
        self.deleted=set()
        self._xk,self._yk,self._xd,self._yd=[],[],[],[]
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.cells \
                                   if cell.tipo==_type)
        self.refresh()

    def refresh (self):
        #self.cells=set(self.values())
        #self.deleted=set()  revisar tendriamos que vaciar delete
        # so we dont have to go over all new inserted and deleted cells
        # perhaps amke a temp of inserted and deleted and use only that
        # to generate the sets of types
        # also we could try to save in temps the changes in pos to see
        # ir resorting could be speed up, and so is probable that order
        # hast change much maybe will be much faster a list.sort than a
        # sorted (list)
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.cells \
                                   if cell.tipo==_type)
        _mindict=[(e,e.pos.x,e.pos.y) for e in self.cells]
        _x=sorted (_mindict,key=itemgetter(1))
        _y=sorted (_mindict,key=itemgetter(2))
        self._xk,self._yk,self._xd,self._yd=[],[],[],[]
        #optimize in one loop range(len)
        for pos,e in enumerate(_x):
            self._xk.append(e[1])
            self._xd.append(e[0])
            e[0].__dpos=(pos,0)
        for pos,e in enumerate(_y):
            self._yk.append(e[2])
            self._yd.append(e[0])
            e[0].__dpos=(e[0].__dpos[0],pos)
        #print ('refr',self._xk)

    def __setitem__(self,key,value):
        # the key shouldnt exist im condidering new but im not controlling
        # also is a light asignment im not actualizing position index
        #il leave it for a refresh
        super(Poscells, self).__setitem__(key,value)
        self.cells.add(value)
        self._types[value.tipo].add(value)
        _ik1=bs.bisect_left(self._xk, value.pos[0])
        _ik2=bs.bisect_left(self._yk, value.pos[1])
        self._xk.insert(_ik1, value.pos[0])
        self._xd.insert(_ik1, value)
        self._yk.insert(_ik2, value.pos[1])
        self._yd.insert(_ik2, value)
        value.__dpos=(_ik1,_ik2)

    def __delitem__(self,key):
        # the key should exist but im not controlling
        # also is a light delete im not actualizing position index
        #il leave it for a refresh
        value=self[key]
        self.deleted.add(value)
        self.cells.remove(value)
        self._types[value.tipo].remove(value)
        _ik1,_ik2=value.__dpos
        #print('del',_ik1,len(self._xk))
        #print('itm',value.pos[0],self._xk[_ik1])
        #print (self._xk)
        del self._xk[_ik1]
        del self._xd[_ik1]
        del self._yk[_ik2]
        del self._yd[_ik2]
        super(Poscells, self).__delitem__(key)

    def refreshItem(self,value):
        self.__delitem__(value.name)
        self.__setitem__(value.name,value)

        print(value.pos.x,self._xk)
        a=1/0

    def deleteByFunc(self,func): # use de func
        delete={cell for cell in self.cells if func(cell)}
        if delete:
            self.cells-=delete
            self.deleted |=delete
            self.refresh() #we will refresh later
            # depend on len of delete perhaps consider del 1 by 1

    def inrange(self,pos,rango,exclude=False,first=False,circle=False):
        if not exclude:
            excl=set()
        elif type(exclude) is  str: # is the type of cell
            excl=self._types[exclude]
        else:
            excl= set([exclude])         # is a cell
            if not self.world.collisions:
                return set() # deactivating collisions
        x,y= pos
        print (x,y,rango)
        print(self._xk)
        _ik=bs.bisect_left(self._xk, x-rango)
        _fk=bs.bisect_right(self._xk, x+rango,lo=_ik)
        _sx=set(self._xd[_ik:_fk])
        _ik=bs.bisect_left(self._yk, y-rango)
        _fk=bs.bisect_right(self._yk, y+rango,lo=_ik)
        _sy=set(self._yd[_ik:_fk])
        result = (_sx & _sy)-excl
        if result and first:
            result=set([result.__iter__().__next__()])
        return result

        # in future add use if circle=True filter by
        # (cell.pos.get_distance(pos) < rango)

class Poscellsold(dict):
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
        # so we dont have to go over all new inserted and deleted cells
        # perhaps amke a temp of inserted and deleted and use only that
        # to generate the sets of types
        # also we could try to save in temps the changes in pos to see
        # ir resorting could be speed up, and so is probable that order
        # hast change much maybe will be much faster a list.sort than a
        # sorted (list)
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
        delete={cell for cell in self.cells if func(cell)}
        self.cells-=delete
        self.deleted |=delete

    def inrange(self,pos,rango,exclude=False,first=False,circle=False):
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
        result = (_sx & _sy)-excl
        if result and first:
            result=set([result.__iter__().__next__()])
        return result

        # in future add use if circle=True filter by
        # (cell.pos.get_distance(pos) < rango)
        # but then it will make sense to use first parameter
        # to get only the first one

