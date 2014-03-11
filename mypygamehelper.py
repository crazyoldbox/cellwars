import pygame
from pygame.locals import *
# the following line is not needed if pgu is installed
#  ?? import sys; sys.path.insert(0, "..")
from pgu import gui
#colors
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (150,150,150)


class PygameHelper:
    def __init__(self, size=(640,480), fill=WHITE):
        #pygame
        self.gamengine=pygame
        self.gamengine.init()
        self.size = size
        self.screen = self.gamengine.display.set_mode(size)
        self.clock = self.gamengine.time.Clock() #to track FPS
        #GUI
        self.gui=gui; self.app=gui.App()
        self.container=gui.Container(align=-1,valign=-1)
        self.form = gui.Form() # permits fm[n] access to all named widgets
        self.add_widgets()
        self.app.init(self.container)
        #pygame inicialitzations
        self.screen.fill(fill)
        self.gamengine.display.flip()
        #game inicialitzations
        self.fps= 0
        self.window_running = False
        self.game_running = False

    def add_widgets(self):
        table=gui.Table()
        self.container.add(table,0,0)

    def handleEvents(self):
        for event in self.gamengine.event.get():
            if event.type == QUIT:
                self.window_running = False
            elif event.type == KEYUP and event.key == K_ESCAPE:
                self.window_running = False
            self.app.event(event)  # control to GUI

            '''
            elif event.type == MOUSEBUTTONUP:
                self.mouseUp(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouseMotion(event.buttons, event.pos, event.rel)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouseDown(event.button, event.pos)
            '''

    #enter the main loop, possibly setting max FPS
    def mainLoop(self, fps=0):
        self.window_running = True
        self.fps= fps

        while self.window_running:
            self.gamengine.display.set_caption("FPS: %i" % self.clock.get_fps())
            self.screen.fill(WHITE)
            if self.game_running:
                self.update()
            self.draw()
            self.gamengine.display.flip()
            self.handleEvents()
            self.clock.tick(self.fps)

        if not self.window_running:
            self.gamengine.quit()

    def update(self):
        pass

    def draw_gui(self):
        self.app.paint()

    def draw_objects(self):
        pass

    def draw(self):
        self.draw_objects()
        self.draw_gui()

    def printText(self, text, pos = (0,0), size = 24, color = BLACK):
        font = self.gamengine.font.Font(None, size)
        text_surf = font.render(text,0,color)
        self.screen.blit(text_surf,pos)

    def draw_object(self,_object,image=None):
        '''Does it best to draw an object
        considering the iterator attributes of pos ((x,y) and dir (dx,dy).
         If an image is given it will use it as sprite.'''

        if image and 'pos' in _object.__dict__: #hasattr not working??
            sprite = self.gamengine.sprite.Sprite() #() is default sprite group
            sprite.image=image
            if 'dir' in _object.__dict__:
                sprite.image = self.gamengine.transform.rotate(image,\
                                              -_object.dir.get_angle()+270)
            sprite.rect = sprite.image.get_rect(center=_object.pos)
            self.screen.blit(sprite.image,sprite.rect)
            if 'test' in _object.__dict__ and _object.text:
                self.printText(_object.text,_object.pos)
        elif 'pos' in _object.__dict__:
            self.gamengine.draw.rect(self.screen,BLACK,
                              (_object.pos[0],_object.pos[1],5,5),2)

    #wait until a key is pressed, then return
    def waitForKey(self):
        press=False
        while not press:
            for event in self.gamengine.event.get():
                if event.type == KEYUP:
                    press = True

    def keyDown(self, key):
        pass

    def keyUp(self, key):
        pass

    def mouseUp(self, button, pos):
        pass

    def mouseDown(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass


