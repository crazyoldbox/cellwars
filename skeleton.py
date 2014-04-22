import pygame
from pygame.locals import *
# the following line is not needed if pgu is installed
#  ?? import sys; sys.path.insert(0, "..")
from pgu import gui
from constants import *
import utils
# also maybe as we are doing with the gui, and already done with the cells
# logic we could extract the objects drawing to a new file
# also would like to be able to dinamically (list,dict,..) add functions to be
# executed by each of the main methods of the mainloop
import time

class Skeleton(object):
    def __init__(self, size=(640,480), fill=WHITE,fps=24):
        #game inicialitzations
        self.window_running = False
        self.game_running = False
        self.volume=50
        #pygame
        self.gamengine=pygame
        self.gamengine.init()
        self.size = size
        self.fps= fps
        self.fill=fill
        self.screen = self.gamengine.display.set_mode(size)
        self.clock = self.gamengine.time.Clock() #to track FPS
        #pygame inicialitzations
        self.screen.fill(self.fill)
        self.gamengine.display.flip()
        #GUI
        self.gui=gui; self.app=gui.App()
        self.form = gui.Form() # permits form[name] access to all named widgets
        #GUI inicialitzations
        self.container=None
        #Event management
        self.handled_events=[]
        # World management
        self.collisions=True
        #Utils
        #### Adding an external function
        self.timeit=False
        self.bound_func=utils.bound_func

    def start(self,fps=None,collisions=False,timeit=False):
        self.add_events()
        self.startgui()
        self.collisions=collisions
        self.timeit=timeit
        self.mainLoop(fps=fps)

    def handle_event_quit(self,event):
        '''Example event handler, event has:.key,.button,.pos and
        .type (QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION,KEYDOWN,KEYUP '''
        self.window_running = False

    def add_events(self):
        events=[
            ('quit','event.type == QUIT',self.handle_event_quit)
            ]
        self.handled_events.extend(events)

    def startgui(self,func=None): #could use other to swap gui
        self.container = func(self) if func else self.create_widgets()
        self.app.init(self.container)

    def create_widgets(self):
        '''Return a container with all your gui widgets, override in subclass'''
        return self.gui.Container(align=-1,valign=-1)

    def handleEvents(self):
        for event in self.gamengine.event.get():
            for name, cond, func in self.handled_events:
                if eval(cond):
                    func(event)
            self.app.event(event)  # control to GUI

    def mainLoop(self,fps=None):
        if fps:
            self.fps=fps
        self.window_running = True

        while self.window_running:
            t1=time.perf_counter()
            self.gamengine.display.set_caption("FPS: %i" % self.clock.get_fps())
            self.screen.fill(self.fill)
            self.handleEvents()
            t2=time.perf_counter()
            self.update()
            t3=time.perf_counter()
            self.draw()
            t4=time.perf_counter()
            self.gamengine.display.flip()
            self.clock.tick(self.fps)
            t5=time.perf_counter()
            if self.timeit:
                print ('loop:ini{}update{}draw{}fin{}'.format(t2-t1,t3-t2,t4-t3,t5-t4))

        if not self.window_running:
            self.gamengine.quit()

    def update(self):
        t1=time.perf_counter()
        if self.game_running:
            self.update_objects()
        t2=time.perf_counter()
        self.update_gui()
        t3=time.perf_counter()
        if self.timeit:
            print ('update:obj{}gui{}'.format(t2-t1,t3-t2))

    def draw(self):
        t1=time.perf_counter()
        self.draw_objects()
        t2=time.perf_counter()
        self.draw_gui()
        t3=time.perf_counter()
        if self.timeit:
            print ('draw:objects{}gui{}'.format(t2-t1,t3-t2))

    def update_objects(self):
        pass

    def update_gui(self):
        pass

    def draw_gui(self):
        self.app.paint()

    def draw_objects(self):
        pass

    def printText(self, text, pos = (0,0), size = 24, color = BLACK):
        font = self.gamengine.font.Font(None, size)
        text_surf = font.render(text,0,color)
        self.screen.blit(text_surf,pos)

    def draw_object(self,_object,image=None):
        '''Does it best to draw an object
        considering the iterator attributes of pos ((x,y) and dir (dx,dy).
         If an image is given it will use it as sprite.'''

        if image and hasattr(_object,'pos'):
            sprite = self.gamengine.sprite.Sprite() #() is default sprite group
            sprite.image=image
            if hasattr(_object,'dir'):
                sprite.image = self.gamengine.transform.rotate(image,\
                                              -_object.dir.get_angle()+270)
            sprite.rect = sprite.image.get_rect(center=_object.pos)
            self.screen.blit(sprite.image,sprite.rect)
            if hasattr(_object,'text') and _object.text:
                self.printText(_object.text,_object.pos)
        elif hasattr(_object,'pos'):
            self.gamengine.draw.rect(self.screen,BLACK,
                              (_object.pos[0],_object.pos[1],5,5),2)

    #wait until a key is pressed, then return
    def waitForKey(self):
        press=False
        while not press:
            for event in self.gamengine.event.get():
                if event.type == KEYUP:
                    press = True

    def add_functions(self):
        '''adds external functions as bounded methods so dont need to add self
        in calls, example:
        self.myfunc=self.add_bound_func(self,externalfunc) '''
        pass


