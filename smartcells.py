# -*- coding: utf-8 -*-
#import numpy
# should be faster but we have to install
# could try to make all operations as matrixes of numpy and then select best
#for distances

#also try to use binary teers but not implemented directly we have to get from pypi
# and also slower than dicts
# how about orderedDict, the problem is to find the next element

# how about using bisect for an index to the dict


from utils import IndexedDict

class Poscells(IndexedDict):
    '''Trys to create a speedup class to search for cells in positions,
        useful for detect and colisions, also will add consider type of
        cell .
        wondering if is best to reset completely each time actaulize world,
        or just considere de changes, if the changes are small perhaps better
        list.sort than sorted(list)'''
    def __init__(self, *args,world=None,delay=False):
        keys=['pos.x','pos.y']
        self.world=world
        super(Poscells, self).__init__(*args,keys=keys)
        self.deleted=set()
        self._types={}
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.values() \
                                   if cell.tipo==_type)
        self.refresh()

    def refresh (self):
        for _type in self.world.tipos:
            self._types[_type]= set(cell for cell in self.values() \
                                   if cell.tipo==_type)
        super(Poscells, self)._refresh()

    def __setitem__(self,key,value):
        super(Poscells, self).__setitem__(key,value)
        self._types[value.tipo].add(value)

    def __delitem__(self,key):
        value=self[key]
        self._types[value.tipo].remove(value)
        super(Poscells, self).__delitem__(key)

    def refreshItem(self,value):
        self[value.name]=value

    def deleteByFunc(self,func): # use de func
        delete=[val for val in self.values() if func(val)]
        self.deleted.update(delete)
        for cell in delete:
            del self[cell.name]

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
        _sx=set(self.subrange('pos.x',(x-rango,x+rango)))
        _sy=set(self.subrange('pos.y',(y-rango,y+rango)))
        result = (_sx & _sy)-excl
        if result and first:
            result=set([result.__iter__().__next__()])
        return result

        # in future add use if circle=True filter by
        # (cell.pos.get_distance(pos) < rango)
