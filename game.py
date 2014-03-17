from skeleton import Skeleton
from constants import *
import cell as Objects
import interface

class Starter(Skeleton):
    def __init__(self, size=(800,800), types={'blue':BLUE},num_cells=10,fps=0):
        Skeleton.__init__(self, size=size, fill= WHITE,fps=fps)
        self.tipos= types
        wrldsize=(size[0]-100-CELL_W/2,size[1]) #-right_GUI-sprite_width/2
        self.world = Objects.World(wrldsize,tipos=list(self.tipos.keys()))
        self.world.gamengine=self
        self.world.collisions=True
        self.world.populate(num_cells)
        self.preload_types()
        self.add_functions()
        # asistant various data for user use
        self.values={}

    def add_events(self):
        events=[
            ('quit','event.type == QUIT',self.handle_event_quit),
            ('clickcell','event.type==MOUSEBUTTONDOWN',self.click_cell)
            ]
        self.handled_events.extend(events)

    def add_functions(self):
        '''adds external functions as bounded methods so dont need to add self
        in calls'''
        # add functions in interface
        for func in ['show_info','create_widgets','update_interface']:
            setattr(self,func,self.bound_func(self,getattr(interface,func)))

    def preload_types(self):
        for tipo in self.tipos: # preload _type images to speed up draw
            sprite_image = self.gamengine.image.load(\
                                    IMGDIR+tipo+'.'+IMGTYPE).convert_alpha()
            color=self.tipos[tipo]
            self.tipos[tipo]=[sprite_image,color]

    def update_gui(self):
        self.update_interface()  # uses the interface

    def update_objects(self):
        self.world.actualizeWorld()

    def draw_objects(self):
        for cell in self.world.population.cells:

            # Paints health and energy bar
            self.gamengine.draw.line(self.screen,RED,cell.pos-(CELL_W/2,15),
                             cell.pos+(CELL_W/2,-15),2)
            self.gamengine.draw.line(self.screen,GREEN,cell.pos-(CELL_W/2,15),
                             cell.pos+(CELL_W*cell.hp/100-CELL_W/2,-15),2)
            self.gamengine.draw.line(self.screen,BLUE,cell.pos-(CELL_W/2,17),
                             cell.pos+(CELL_W*cell.energy/100-CELL_W/2,-17),2)


            sprite = cell.animate.createSprite(self.world.ticks)
            self.screen.blit(sprite.image,sprite.rect)
            if hasattr(cell,'text') and cell.text:
                self.printText(cell.text,cell.pos)
            #draws any object using its best of pos, dir arguments with
            #self.draw_object(cell,self.tipos[cell.tipo][0])

    def click_cell(self, event):
        if event.button==1 and event.pos[0]<self.world.size[0]:
            foundcell=False
            for cell in self.world.population.cells:
                if cell.pos.get_distance(event.pos)<15:
                    foundcell=cell
                    break
            if foundcell:
                if 'infocell' in self.values and self.values['infocell'] \
                        in self.world.population.cells:
                    self.values['infocell'].text=''
                self.values['infocell']=foundcell
                foundcell.text='****'
                self.show_info(foundcell.name,'will update_interface')
                # or if isnt downloaded interface.show_info(self,title,text)
                #print([e.name for e in self.world.population.inrange(\
                #      foundcell.pos,foundcell.view_range)])

Starter(DIM_WIN,TYPES,CELL_NUM,FPS).start(collisions=False,timeit=False)
