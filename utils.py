# -*- coding: utf-8 -*-
from functools import wraps
from operator import itemgetter, attrgetter
import bisect as bs

def bound_func(instance,func):
    '''quick temporal method to bound external functions to methods
    still needs wrapping, probaly use a class, etc..), and try to learn
    exactly what python does
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
    def __init__(self, keys=[]):
        super(IndexedDict, self).__init__()
        self.keys=keys
        self.index={key:{} for key in self.keys}
        self.refresh()

    def updateindex (self,*args,key=None,op=None):
        _ik=bs.bisect_left(self.index[key]['index'],value[key])
        index=self.index[key]
        argum=[index['index'],_ik];argum.extend(args[0])
        op(*argum)
        argum=[index['key'],_ik]; argum.extend(args[1])
        op(*argum)

    def refresh (self):
        # for each main key of the dictionary we store the position of each key
        mindict=[val for val in self.items()]
        for key in self.keys:  # create an ordered list of items for each key
            self.index[key]['key']=sorted (mindict,key=attrgetter(key))
            self.index[key]['index']=[val[1][key] for val in \
                                                   self.index[key]['key']]

    def __setitem__(self,mainkey,value):
        '''If the item already exists we delete it before adding the new one
        so the indexes are already updated when we insert in each index
        *** wont work because self.keys is not updated for the other elements
        so perhaps is cheaper to do a total refresh'''
        if mainkey in self:
            for key in self.keys:
                val=getattr(value,key)
                _ik=bs.bisect_left(self.index[key]['index'],val)
                self.index[key]['index'][_ik]= val
                self.index[key]['key'][_ik]=(mainkey, value)

                #or self.updateindex([value[key]],[mainkey,value[key]],key=mainkey,op=list.__setitem__)
        else:
            for key in self.keys:
                val=getattr(value,key)
                _ik=bs.bisect_left(self.index[key]['index'],val)
                self.index[key]['index'].insert(_ik, val)
                self.index[key]['key'].insert(_ik, (mainkey,value))

                #or self.updateindex([value[key]],[mainkey,value[key]],key=mainkey,op=list.insert)
        super(IndexedDict, self).__setitem__(mainkey,value)

    def __delitem__(self,mainkey):
        ''' Delete this item in all indexes and delete de item
        *** wont work because self.keys is not updated for the other elements
        so perhaps is cheaper to do a total refresh'''
        value=self[mainkey]
        for key in self.keys:
            val=getattr(value,key)
            _ik=bs.bisect_left(self.index[key]['index'],val)
            del self.index[key]['index'][_ik]
            del self.index[key]['key'][_ik]

            #or self.updateindex([],[],key=mainkey,op=list.__delitem__)
        super(IndexedDict, self).__delitem__(mainkey)


    def deleteByFunc(self,func): # use de func
        #a soft delete needs refresh to actualize indexex
        delete={item[0] for item in self.items() if func(item[1])}
        for key in delete:
            del self[key]

    def subrange(self,key,interval):
        _ik=bs.bisect_left(self.index[key]['index'], interval[0])
        _fk=bs.bisect_right(self.index[key]['index'], interval[1],lo=_ik)
        items=self.index[key]['key'][_ik:_fk]
        return items # [self[item] for item in items]


a=IndexedDict()
