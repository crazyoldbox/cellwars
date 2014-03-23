# -*- coding: utf-8 -*-
from functools import wraps
import operator
from operator import itemgetter, attrgetter
import bisect as bs

def bound_func(instance,func):
    '''quick temporal method to bound external functions to methods
    still needs wrapping, probaly use a class, etc..), and try to learn
    exactly what python does. Culd use partiall too
    '''
    @wraps(func)
    def nf(*args,**kargs):
        return func(instance,*args,**kargs)
    return nf

# progress towards a better bounding working but not used yet
class bound_descriptor:

    def __init__(self,instance,func):
        self.__self__=instance
        self.func=func

    def __call__(self,*args,**kargs):
        return self.func(self.__self__,*args,**kargs)

    def __get__(self):
        print ('descriptor for:',self.func)


class IndexedDict(dict):
    '''On progress A multi indexed dictionary, with sequential indexes
       anyways thats kind of a data base so better look up for something
       similar and dont reinvent the wheel'''
    def __init__(self,*args, keys=[]):
        super(IndexedDict, self).__init__(*args)
        self.keys=[(key,attrgetter(key)) for key in keys]
        self.index={key:{} for key,func in self.keys}
        self._refresh()

    def updateindex (self,*args,key=None,op=None):
        '''Not in use, we could use not to repeat code
           but it will cost speed'''
        _ik=bs.bisect_left(self.index[key]['index'],value[key])
        index=self.index[key]
        argum=[index['index'],_ik];argum.extend(args[0])
        op(*argum)
        argum=[index['key'],_ik]; argum.extend(args[1])
        op(*argum)

    def _refresh (self):
        '''For each key create an index as an ordered list of values
           with an ordered list of items.
        '''
        mindict=[val for val in self.values()]
        for key,func in self.keys:
            self.index[key]['key']=sorted (mindict,key=func)
            self.index[key]['index']=[func(val) for val in \
                                      self.index[key]['key']]
            self.index[key]['val']={val[0]:func(val[1]) for val in \
                                    self.items()}

    def __setitem__(self,mainkey,value):
        '''If the item already exists we delete it before adding the new one
        so the indexes are already updated when we insert in each index
        *** wont work because self.keys is not updated for the other elements
        so perhaps is cheaper to do a total refresh'''
        if mainkey in self:
            for key,func in self.keys:
                val=self.index[key]['val'][mainkey]
                _ik=bs.bisect_left(self.index[key]['index'],val)
                del self.index[key]['index'][_ik]
                del self.index[key]['key'][_ik]
                del self.index[key]['val'][mainkey]
                #or self.updateindex([],[],key=mainkey,op=list.__delitem__)
        for key,func in self.keys:
            val=func(value)
            _ik=bs.bisect_left(self.index[key]['index'],val)
            self.index[key]['index'].insert(_ik, val)
            self.index[key]['key'].insert(_ik, value)
            self.index[key]['val'][mainkey]=val
            #or self.updateindex([value[key]],[mainkey,value[key]],key=mainkey,op=list.insert)
        super(IndexedDict, self).__setitem__(mainkey,value)

    def __delitem__(self,mainkey):
        ''' Delete this item in all indexes and delete de item'''
        for key,func in self.keys:
            val=self.index[key]['val'][mainkey]
            _ik=bs.bisect_left(self.index[key]['index'],val)
            del self.index[key]['index'][_ik]
            del self.index[key]['key'][_ik]
            del self.index[key]['val'][mainkey]
            #or self.updateindex([],[],key=mainkey,op=list.__delitem__)
        super(IndexedDict, self).__delitem__(mainkey)


    def deleteByFunc(self,func):
        '''Try to use filter probably faster
           also to delete perhaps find firs a list of positions
           and then reconstruct withou those positions,
           perhaps there is a utility to do that as binary map or something'''
        delete={item[0] for item in self.items() if func(item[1])}
        for key in delete:
            del self[key]

    def subrange(self,key,interval):
        _ik=bs.bisect_left(self.index[key]['index'], interval[0])
        _fk=bs.bisect_right(self.index[key]['index'], interval[1],lo=_ik)
        items=self.index[key]['key'][_ik:_fk]
        return items # perhaps return an iterator iter()


