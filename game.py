from mypygamehelper import *
from constants import *
import cell as Celula
import game_gui

class Starter(PygameHelper):
    def __init__(self, size=(800,800), types={'blue':BLUE},num_cells=10,fps=0):
        PygameHelper.__init__(self, size=size, fill= WHITE,fps=fps)
        self.tipos= types
        wrldsize=(size[0]-100-15,size[1]) #-right_GUI-sprite_width/2
        self.mundo = Celula.Mundo(wrldsize,tipos=list(self.tipos.keys()))
        self.mundo.gamengine=self
        self.mundo.populate(num_cells)
        self.preload_types()
        self.startgui()

    def preload_types(self):
        for tipo in self.tipos: # preload _type images to speed up draw
            sprite_image = self.gamengine.image.load(\
                                    IMGDIR+tipo+'.'+IMGTYPE).convert_alpha()
            color=self.tipos[tipo]
            self.tipos[tipo]=[sprite_image,color]

    def update_gui(self):
        game_gui.update_gui(self)

    def update_objects(self):
        self.mundo.actualizarMundo()

    def draw_objects(self):
        for cell in self.mundo.population.values():

            # Paints health and energy bar
            pygame.draw.line(self.screen,RED,cell.pos-(25/2,15),
                             cell.pos+(25/2,-15),2)
            pygame.draw.line(self.screen,GREEN,cell.pos-(25/2,15),
                             cell.pos+(25*cell.hp/100-25/2,-15),2)
            pygame.draw.line(self.screen,BLUE,cell.pos-(25/2,17),
                             cell.pos+(25*cell.energy/100-25/2,-17),2)
            #draws any object using its best of pos, dir arguments with
            self.draw_object(cell,self.tipos[cell.tipo][0])

    def create_widgets(self):
        return game_gui.create_widgets(self)

    def keyUp(self, key):
        pass
    def mouseUp(self, button, pos):
        pass
    def mouseDown(self, button, pos):
        game_gui.verify_mouse(self,button, pos)

    def mouseMotion(self, buttons, pos, rel):
        pass

s = Starter(DIM_WIN,TYPES,CELL_NUM,FPS)
s.mainLoop()
