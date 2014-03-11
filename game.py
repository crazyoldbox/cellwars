from mypygamehelper import *
import cell as Celula

IMGDIR = "./data/sprites/"
IMGTYPE ="png"
DIM_WIN = (1000,800)
TYPES = {"red":RED,"blue":BLUE}
CELL_NUM = 200
FPS = 24

class Starter(PygameHelper):
    def __init__(self, dim=(800,800), types={'blue':BLUE}, num_cells=100):
        PygameHelper.__init__(self, size=dim, fill= WHITE)
        self.tipos= types
        self.num_cells=num_cells
        self.wrldsize=list(dim)
        self.wrldsize[0]*=0.9
        self.mundo = Celula.Mundo(self.wrldsize,tipos=list(self.tipos.keys()))
        self.mundo.gamengine=self
        self.mundo.populate(num_cells)
        self.preload_types()

    def preload_types(self):
        for tipo in self.tipos: # preload _type images to speed up draw
            sprite_image = self.gamengine.image.load(\
                                    IMGDIR+tipo+'.'+IMGTYPE).convert_alpha()
            color=self.tipos[tipo]
            self.tipos[tipo]=[sprite_image,color]

    def update(self):
        self.mundo.actualizarMundo()
        # write number of cells by type
        ctp=[" "+type_+":"+str(len(self.mundo.popul_indexs[type_])) \
             for type_ in self.mundo.tipos]
        self.printText("Cells "+"".join(ctp))

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

    def add_widgets(self):
        def gui_speed(slider):
            self.fps=slider.value
        def gui_quantity(slider):
            print ("val quantity",slider.value)
        def gui_run(_button):
            self.game_running= not self.game_running
            _button.value='Pause' if self.game_running else 'Start'
        def gui_restart(_button):
            self.mundo.populate(self.num_cells)
        def gui_nombre(_input):
            print ("Input ",_input.value)

        table=gui.Table()
        fg = BLACK

        table.tr()
        e=gui.Button("Start", name='run')
        e.connect(gui.CLICK, gui_run, e)
        table.td(e, align=-1,colspan=1)

        table.tr()
        e=gui.Button("Restart", name='restart')
        e.connect(gui.CLICK, gui_restart, e)
        table.td(e, align=-1)

        table.tr()
        table.td(gui.Label("Speed:",color=fg),size=10, align=-1)
        table.tr()
        e = gui.HSlider(FPS,0,50,size=10,width=100,height=16,name='speed')
        e.connect(gui.CHANGE, gui_speed, e)
        table.td(e)

        table.tr()
        table.td(gui.Label("Size: ",color=fg), align=-1)
        table.tr()
        e = gui.HSlider(30,5,50,size=20,width=100,height=16,name='size')
        table.td(e)

        table.tr()
        table.td(gui.Label("Quantity: ",color=fg),align=-1)
        table.tr()
        e = gui.HSlider(100,1,1000,size=20,width=100,height=16,name='quantity')
        e.connect(gui.CHANGE, gui_quantity, e)
        table.td(e)
        table.tr()
        table.td(gui.Label("Input"), align=-1)
        table.tr()
        e = gui.Input(value='Cuzco',size=8,name='nombre')
        e.connect(gui.ACTIVATE, gui_nombre,e)
        table.td(e)

        cont=gui.Container(width=self.size[0]*0.1,height=self.size[1])
        cont.add(table,0,0)
        self.container.add(cont,self.size[0]*0.9,0)
        #self.container.add(table,int(self.size[0]*0.8),0)

    def keyUp(self, key):
        pass
    def mouseUp(self, button, pos):
        pass
    def mouseDown(self, button, pos):
        pass
    def mouseMotion(self, buttons, pos, rel):
        pass

s = Starter(DIM_WIN,TYPES,CELL_NUM)
s.mainLoop(FPS)
