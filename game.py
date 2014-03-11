from mypygamehelper import *
import cell as Celula

IMGDIR = "./data/sprites/"
IMGTYPE ="png"
DIM_WIN = (1000,800)
TYPES = {"red":RED,"blue":BLUE}
CELL_NUM = 200
FPS = 24

class Starter(PygameHelper):
    def __init__(self, dim=(800,800), types={'blue':BLUE},num_cells=10,fps=0):
        PygameHelper.__init__(self, size=dim, fill= WHITE)
        self.tipos= types
        self.num_cells=num_cells
        self.fps=fps
        self.wrldsize=list(dim)
        self.wrldsize[0]*=0.9
        self.mundo = Celula.Mundo(self.wrldsize,tipos=list(self.tipos.keys()))
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

    def update(self):
        self.mundo.actualizarMundo()
        # write number of cells by type in GUI
        self.form['label_qtty'].value= \
                                'Qtty:'+str(len(self.mundo.population))+' '
        for tipo in self.mundo.tipos:
            self.form['num_'+tipo].value= \
                                str(len(self.mundo.popul_indexs[tipo]))+' '

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
        def gui_speed(slider):
            self.fps=slider.value
            self.form['label_speed'].value='Speed:'+str(self.fps)

        def gui_quantity(slider):
            self.form['label_qtty'].value='Qtty:'+str(slider.value)+' '
        def gui_run(_button):
            self.game_running= not self.game_running
            _button.value='Pause' if self.game_running else 'Start'
        def gui_restart(_button):
            self.mundo.population={}
            self.mundo.populate(self.form['quantity'].value)
        def gui_nombre(_input):
            print ("Input ",_input.value)

        table=gui.Table()
        fg = BLACK

        table.tr()
        e=gui.Button("Start", name='run')
        e.connect(gui.CLICK, gui_run, e)
        table.td(e, align=-1,colspan=1)

        table.tr()
        table.td(gui.Label("Speed:"+str(self.fps)+" ",color=fg, \
                           name='label_speed'),size=10, align=-1)
        table.tr()
        e = gui.HSlider(self.fps,0,50,size=10,width=100,height=16,name='speed')
        e.connect(gui.CHANGE, gui_speed, e)
        table.td(e, align=-1)

        table.tr()
        table.td(gui.Container(height=5))

        table.tr()
        e=gui.Button("Restart", name='restart')
        e.connect(gui.CLICK, gui_restart, e)
        table.td(e, align=-1)

        table.tr()
        cant= len(self.mundo.population) if hasattr(self,'tipos') else 1
        table.td(gui.Label('Qtty:'+str(cant)+'  ',color=fg,name='label_qtty'),\
                 align=-1)
        table.tr()
        e =gui.HSlider(cant,1,999,size=10,width=100,height=16,name='quantity')
        e.connect(gui.CHANGE, gui_quantity, e)
        table.td(e,align=-1)
        if hasattr(self,'tipos'):
            for tipo in self.tipos:
                table.tr()
                color=self.tipos[tipo][1]
                cant=str(len(self.mundo.popul_indexs[tipo]))+' '
                table.td(gui.Label(value=cant,color=color,name='num_'+tipo),\
                         align=+1)

        table.tr()
        table.td(gui.Container(height=5))

        table.tr()
        table.td(gui.Label("Selected Cell"), align=-1)
        table.tr()
        e = gui.Input(value='cellname',size=10,name='cell_name', align=-1)
        e.connect(gui.ACTIVATE, gui_nombre,e)
        table.td(e)

        cont=gui.Container(width=self.size[0]*0.1,height=self.size[1])
        cont.add(table,0,0)
        container=gui.Container(align=-1,valign=-1)
        container.add(cont,self.size[0]*0.9,0)
        return container

    def keyUp(self, key):
        pass
    def mouseUp(self, button, pos):
        pass
    def mouseDown(self, button, pos):
        pass
    def mouseMotion(self, buttons, pos, rel):
        pass

s = Starter(DIM_WIN,TYPES,CELL_NUM,FPS)
s.mainLoop()
