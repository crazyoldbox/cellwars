# -*- coding: utf-8 -*-
def bound_func(instance,func):
    '''quick temporal method to bound external functions to methods
    still needs wrapping, probaly use a class, etc..), and try to learn
    exactly what python does
    '''
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


