#-*- coding: utf-8 -*-
'''
Description: Cell class with primitive AI
Authors: Yago Varela & JAN
e-mail: varelayago@gmail.com
version: 0.03
'''
import random
import math
import time
from vec2d import vec2d as V2d
from animations import *
from smartcells import Poscells
from constants import *

class Cell:
    def __init__(self,world=None,tipo = 'Blue',name="Blue1"):
        # Identification of the cell
        self.world = world
        self.tipo, self.name = tipo,name
        # Relation of the cell with de world
        self.view_range,self.speed = CELL_W*4,CELL_W/4
        self.pos = V2d([random.random()*self.world.size[0],
                        random.random()*self.world.size[1]])
        self.dir=V2d([self.speed,0]).rotated(random.randint(0,360))
        # Relation of the cell with other cells
        self.armor, self.hp,self.hp_max = 0,100,100              # defend
        self.attack_range,self.dps = CELL_W*1.5,2                # attack
        # repr_rate is per 1000
        self.sons,self.repr_rate,self.repr_cost = 0,1,50        # reproduction
        self.energy, self.energy_max = 100,100                  # energy
        # Relation of the cell with the engine
        self.ticks=12; self.tick=random.randint(0,self.ticks-1)  # refresh rate
        self.text=''                                           # representation
        self.detected,self.attacking={},{}                     # auxiliary
        # Animates taking in account status
        self.status = 'idle'; self.animate = Animate(self)

    def __str__(self):
        return 'This is cell {} in {} position and {}HP left going {}'.\
                format(self.name,self.pos,self.hp,self.dir)

    def isDead(self):
        return (self.hp<=0)

    def reproduce(self):
        '''if the cell has enough energy and probability matches the repr_rate
           we consume energy and add a son to this cell and then return the
           son object else it returns None'''

        if random.randint(0,1000) <= self.repr_rate\
                                             and self.energy > self.repr_cost:
            self.energy -= self.repr_cost
            self.sons += 1
            name = self.name + '*' + str(self.sons)
            son = Cell(self.world, self.tipo, name)
            son.pos = self.pos + (0,CELL_W)
            return son
        else:
            return None

    def energyMod(self,amount = -1):
        '''Modifies energy amount'''
        if self.energy <= self.energy_max :
            self.energy += amount
        else: self.energy = self.energy_max

    def energyCheck(self):
        return (self.energy > 0)

    def regenerate(self, amount = 1):
        if self.hp < self.hp_max:
            self.hp += amount
            self.energyMod(-1)


    def move(self,data=None):

        '''Tries to move in the direction data specifies, correcting possible
           boundery crossings. Data is normally a V2d vector, but it wiil also
           accept a Cell object considering you want to move towards it.
           Other types of data or no data passed will move randomly '''

        if isinstance(data,V2d):
            self.dir=data
        elif isinstance(data,Cell):
            #we are doing a distance and a normalitzation lets calculate less
            # we could divide by distance instead of normalice
            distance=self.pos.get_distance(data.pos)
            self.dir=(data.pos-self.pos).normalized()
            if self.speed>(distance-CELL_W):
                self.dir*=(distance-CELL_W)
            else:
                self.dir*=self.speed
        else:
            print ('self.move:shouldn arrive here')
            self.dir=V2d([self.speed,0]).rotated(random.randint(0,360))
        newpos=(self.pos+self.dir)%self.world.size
        if not self.world.population.inrange(newpos,CELL_W,first=False,\
                                                          exclude=self):
            self.pos=newpos
            #self.energyMod()  do we really need it each iteration we already have
            # in primitiveAI
            self.world.population.refreshItem(self)
        else:
            a=self.world.population.inrange(newpos,CELL_W,first=False,\
                                                          exclude=self).__iter__().__next__()

        self.status = 'move'


    def detect(self,rango,selective = False,first=False):

        '''Given a population(has to be a dictionary),and a range it will
           return a list of cells. We use selective to look only for different
           tipo cells, and first to return a maximum of 1.
           ??? Could we optimize for attacking to look only in detected??
           Could we use a grid of tiles to simplify detecting proximity or perhaps
           two ordered lists of cells by x and y coordinate+-'''
        excl=self if not selective else self.tipo
        return self.world.population.inrange(self.pos,rango,\
                      first=first,exclude=excl)

    def attack(self):
        '''We first take away armor points and then go for HP. At the end
           we consume energy'''

        for cell in  self.attacking:
            if cell.armor > 0:
                cell.armor -= self.dps
            else:
                cell.hp -= self.dps
            self.energyMod(-1)
        self.status = 'attack'

    def primitiveAI(self):

        ''' If some cell is detected in his view_range he goes towards it,
            if there's more than one cell will choose the fist one he detected
            (not the closest one) and then attack! If no cell was detected
            then it will move randomly'''
        # Thinking
        # were to move
        self.energyMod(10) # why do an energy check if you just upgrade it
        if self.energyCheck():
            self.regenerate()
            self.attacking={}
            self.detected=self.detect(self.view_range,\
                                  selective = True,first=True)
            if self.detected:
                self.attacking=self.detect(self.attack_range,
                                                selective=True,first=True)
            if self.attacking:
                self.dir=self.attacking.__iter__().__next__()
                #slower but could use ..  next(iter(self.attacking))
            elif self.detected:
                self.dir=self.detected.__iter__().__next__()
            else:
                self.dir=V2d([self.speed,0]).rotated(random.randint(0,360))



    def primitiveIS(self):
        # Instincts
        if self.energyCheck():

            # the following line (??) is strange review why we should pass de direction to move
            # we already have it so if detected has more than one item changes again
            #passing a cell instead of the direction we already have
            # it would have kind of sense if we querry self.attacking instead of detected
            # to move to an attacked cell
            self.move(self.dir)
            if self.attacking:
                self.attack()
                self.status = 'attack'

class World:

    def __init__(self,size=(800,600), tipos = ['Blue','Red']):

        self.tipos = tipos
        self.size = size
        self.population=Poscells(self)
        # auxiliary data
        self.ticks=0; self.maxticks=10000; self.thinktick=1

    def populate(self, numcells=10, clean=True):

        '''Creates dictionary and populates it with #num cells, positioning
           them inside the world size boundaries, and chosing the type of
           cell randomly from the world tipos list. The keys have a tipo+int
           format(e.g "Blue12"). '''
        if clean:
            self.population=Poscells(self)
        num_ini=len(self.population)
        for num in range(num_ini,num_ini+numcells):
            tipo = random.choice(self.tipos)
            cell=Cell(self, tipo,tipo + str(num))
            fin=10 # only try to insert in a free space
            while self.population.inrange(cell.pos,CELL_W,exclude=cell)\
                  and fin:
                fin-=1
                cell.pos = V2d([random.random()*self.size[0],
                        random.random()*self.size[1]])
            if fin:
                self.population[cell.name] = cell
            # if not fin then no space for the cell, in future try to find
            # other way like first dividing al space in square of CELL_W, put
            # them on al scrambled list and pop the positions


    def actualizeWorld(self):

        new_borns = []
        self.ticks=(self.ticks+1) % self.maxticks
        for cell in self.population.values():
            if self.ticks%cell.ticks==cell.tick:
                cell.primitiveAI()
                son=cell.reproduce()
                if son:
                    new_borns.append(son)
        for cell in self.population.values():
            cell.primitiveIS()
        self.reproduction(new_borns)
        self.population.deleteByFunc(Cell.isDead)
        #self.population.refresh()

    def reproduction(self,new_borns):
        '''We receive a list with all the sons. Then we put them in population.
           finally we optimeze population'''

        for son in new_borns:
            fin=5
            while self.population.inrange(son.pos,CELL_W,exclude=son)\
                 and fin:
                fin-=1
                son.pos = V2d([random.random()*self.size[0],
                        random.random()*self.size[1]])
            if fin: # if found space
                self.population[son.name] = son
