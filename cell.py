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

class Cell:
    def __init__(self,world=None,tipo = 'Blue',name="Blue1"):
        # Identification of the cell
        self.world = world
        self.tipo, self.name = tipo,name
        # Relation of the cell with de world
        self.view_range,self.speed = 80,2
        self.pos = V2d([random.random()*world.map_dim[0],
                        random.random()*world.map_dim[1]])
        self.dir=V2d([self.speed,0]).rotated(random.randint(0,360))
        # Relation of the cell with other cells
        self.armor, self.hp,self.hp_max = 0,100,100              # defend
        self.attack_range,self.dps = 5,2                        # attack
        # repr_rate is per 1000
        self.sons,self.repr_rate,self.repr_cost = 0,1,50        # reproduction
        self.energy, self.energy_max = 100,100                  # energy
        # Relation of the cell with the engine
        self.ticks=12; self.tick=random.randint(0,self.ticks-1)  # refresh rate
        self.text=""                                           # representation
        self.detected,self.attacking=[],[]                     # auxiliary

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
            son.pos = self.pos + (0,20)
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
            self.pos+=data
        elif isinstance(data,Cell):
            distance=self.pos.get_distance(data.pos)
            self.dir=-(self.pos-data.pos).normalized()
            if self.speed<distance:
                self.pos+=self.dir*self.speed
            else:
                self.pos=V2d(data.pos)
        else:
            vdir=V2d([self.speed,0]).rotated(random.randint(0,360))
            self.pos+=vdir
        self.pos%=self.world.map_dim # correct if it goes past one side
        self.energyMod()


    def inrange(self,cell,rango):
        '''First we try to see if they are aprox in distance
           without using costly squared and roots if they are then
           we qet the exact distance'''

        return (abs(self.pos.x-cell.pos.x)<rango) and \
               (abs(self.pos.y-cell.pos.y)<rango) and \
               (self.pos.get_distance(cell.pos) < rango)

    def detect(self,rango,selective = False,first=False):

        '''Given a population(has to be a dictionary),and a range it will
           return a list of cells. We use selective to look only for different
           tipo cells, and first to return a maximum of 1.
           ??? Could we optimize for attacking to look only in detected??'''

        if selective:
            searchdict=self.world.popul_indexs["N"+self.tipo]
        else:
            searchdict=self.world.population
        for cell in searchdict.values():
            if self.inrange(cell,rango):
                    yield cell
                    if first:
                        break

    def attack(self):
        '''We first take away armor points and then go for HP. At the end
           we consume energy'''

        for cell in  self.attacking:
            if cell.armor > 0:
                cell.armor -= self.dps
            else:
                cell.hp -= self.dps
            self.energyMod(-1)

    def primitiveAI(self):

        ''' If some cell is detected in his view_range he goes towards it,
            if there's more than one cell will choose the fist one he detected
            (not the closest one) and then attack! If no cell was detected
            then it will move randomly'''
        # Thinking
        # were to move
        self.energyMod(10)
        if self.energyCheck():
            self.regenerate()
            self.detected = [x for x in \
                self.detect(self.view_range,selective = True,first=True)]
            if self.detected: #always after de cell even if its killed
                self.dir=(self.pos-self.detected[0].pos).normalized()*self.speed
            else:
                self.dir=V2d([self.speed,0]).rotated(random.randint(0,360))
            # who to attack
            self.attacking=list(self.detect(self.attack_range,
                                            selective=True,first=True))


    def primitiveIS(self):
        # Instincts
        if self.energyCheck():
            self.attack()
            self.move(self.detected[0]) if self.detected else self.move(self.dir)

class Mundo:

    def __init__(self,map_dim, tipos = ['Blue','Red']):

        self.map_dim = map_dim
        self.population={}
        # auxiliary data
        self.popul_indexs={}
        self.tipos = tipos
        self.dead,self.deads=[],{}
        self.ticks=0; self.maxticks=10000; self.thinktick=1

    def populate(self, numcells=10, clean=True):

        '''Creates dictionary and populates it with #num cells, positioning
           them inside the world map_dim boundaries, and chosing the type of
           cell randomly from the world tipos list. The keys have a tipo+int
           format(e.g "Blue12"). '''
        if clean:
            self.population,self.deads = {},{}
        num_ini=len(self.population)+len(self.deads)
        for num in range(num_ini,num_ini+numcells):
            tipo = random.choice(self.tipos)
            cell=Cell(self, tipo,tipo + str(num))
            self.population[cell.name] = cell
        # generate optimized dictionaries for each type
        self.optimize_population()

    def actualizarMundo(self):

        new_borns = []
        self.ticks=(self.ticks+1) % self.maxticks
        for cell in self.population.values():
            """think once more even if cell.isDead(): """
            if self.ticks%cell.ticks==cell.tick:
                cell.primitiveAI()
                new_borns.append(cell.reproduce())
        for cell in self.population.values():
            """act once more even if cell.isDead(): """
            cell.primitiveIS()

        self.delete_dead_cells()
        self.reproduction(new_borns)

    def reproduction(self,new_borns):
        '''We receive a list with all the sons. Then we put them in population.
           finally we optimeze population'''

        for son in new_borns:
            if son:
                self.population[son.name] = son
        self.optimize_population()


    def delete_dead_cells(self):

        self.dead=[name for name,cell in self.population.items()\
                   if cell.isDead()]
        for muerto in self.dead:
            self.deads[muerto]=self.population[muerto]
            del self.population[muerto]
            for index_ in self.popul_indexs.keys():
                self.popul_indexs[index_].pop(muerto,None)

    def optimize_population(self):
        '''Using the actual population generates the following new
           dictionaries for each type of cell:
               -ctpop[type]=dictionary with cells of this type
               -ctpop['N'+type]=dictionary of cells of other types
           '''
        for tipo in self.tipos:
            self.popul_indexs[tipo]={cell.name:cell for cell in \
                                  self.population.values() if cell.tipo==tipo}
            self.popul_indexs['N'+tipo]={cell.name:cell for cell in \
                                  self.population.values() if cell.tipo!=tipo}
