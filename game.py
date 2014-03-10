from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
import pygame
import cell as Celula

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (150,150,150)
DIM_WIN = (1000,800)
TYPES = {"red":RED,"blue":BLUE}
CELL_NUM = 200
FPS = 25

class Starter(PygameHelper):
    def __init__(self, dim=(800,800), types={'blue':(0,0,255)}, cell_num=100):
        self.w, self.h = dim
        self.tipos= types
        self.mundo = Celula.Mundo([self.w, self.h],\
                                    tipos=list(self.tipos.keys()))
        self.mundo.populate(cell_num)
        PygameHelper.__init__(self, size=(self.w, self.h), fill= WHITE)
        for tipo in self.tipos: # to speed up draw
            sprite_image = pygame.image.load("./sprites/"+tipo+".png")
            sprite_image.convert_alpha()
            color=self.tipos[tipo]
            self.tipos[tipo]=[sprite_image,color]

    def update(self):
        self.mundo.actualizarMundo()
        self.screen.fill(WHITE)
        # write number of cells by type
        ctp=[" "+type_+":"+str(len(self.mundo.popul_indexs[type_])) \
             for type_ in self.mundo.tipos]
        self.printText("Cells "+"".join(ctp))

    def keyUp(self, key):
        pass

    def mouseUp(self, button, pos):
        pass
    def mouseDown(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass

    def draw(self):
        for cell in self.mundo.population.values():

            sprite_image = self.tipos[cell.tipo][0]
            color=self.tipos[cell.tipo][1]

            # Paints health and energy bar
            pygame.draw.line(self.screen,RED,cell.pos-(25/2,15),
                             cell.pos+(25/2,-15),2)
            pygame.draw.line(self.screen,GREEN,cell.pos-(25/2,15),
                             cell.pos+(25*cell.hp/100-25/2,-15),2)
            pygame.draw.line(self.screen,BLUE,cell.pos-(25/2,17),
                             cell.pos+(25*cell.energy/100-25/2,-17),2)

            sprite_test = pygame.sprite.Sprite()
            sprite_test.image = sprite_image
            sprite_test.image = pygame.transform.rotate(sprite_image,
                                          -cell.dir.get_angle()+270)
            sprite_test.rect = sprite_test.image.get_rect(center=
                                                    (cell.pos.x ,cell.pos.y))

            # maybe storing data in cells and here only changing pos and blit
            self.screen.blit(sprite_test.image, sprite_test.rect)
            if cell.text:
                self.printText(cell.text,(ax,ay))

s = Starter(DIM_WIN,TYPES,CELL_NUM)
s.mainLoop(FPS)
