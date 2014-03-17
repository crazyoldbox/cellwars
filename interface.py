# -*- coding: utf-8 -*-
from constants import *
from pgu import gui

class ShowInfo(gui.Container):
    ''' Quick Custom widget to show info and collaps it
    we should refine a lottt parameters and other stuff'''
    def __init__(self,**params):
        gui.Container.__init__(self,**params)
        self.data,self.button = None,None

    def text(self,text):
        if self.widgets!=[]:
            self.data.value=text

    def addinfo(self,title,text):
        self.widgets = []
        name=gui.Button(title)
        data=gui.TextArea(text,size=10,width=100,height=150,disabled=True)
        data.value=text
        self.data=data
        self.button=name.value
        table=gui.Table()
        table.tr();table.td(name);table.tr();table.td(data)
        name.connect(gui.CLICK,self.remove,table)
        self.add(table,0,0)

def update_interface(self):
    #write number of cells by type
    for tipo in self.world.tipos:
        self.form['num_'+tipo].value= \
                '{:>14}'.format(len(self.world.population._types[tipo]))
    #update info data on selected cell
    info=self.form['info']
    if info.widgets!=[] and info.button.value in self.world.population:
        text='';cell=self.world.population[info.button.value]
        for attr in ['status','armor','hp','dps','sons','energy']:
            text=text+attr+':'+str(getattr(cell,attr))+'\n'
        info.text(text)

def show_info(self,title,text):
    info=self.form['info']
    info.addinfo(title,text)

def create_widgets(self):
    '''creates and returns GUI structure a la DOM, that will be asigned to
    self.container from wich startgui can start its painting.'''

    g=self.gui # to abreviate the use
    def gui_speed(slider):
        self.fps=slider.value
        self.form['label_speed'].value='Speed:{:>4}'.format(self.fps)

    def gui_quantity(slider):
        self.form['label_qtty'].value='Qtty:{:>5}'.format(slider.value)

    def gui_run(_button):
        self.game_running= not self.game_running
        _button.value='Pause' if self.game_running else 'Start'

    def gui_collisions(_button):
        self.world.collisions= not self.world.collisions
        _button.value='No Collisions' if self.world.collisions else 'Collisions'

    def gui_restart(_button):
        self.world.population,self.world.deads = {},{}
        self.world.populate(self.form['quantity'].value)

    # in future try to be able to reescale the widgets
    table=g.Table(name='tabla')
    fg = BLACK

    table.tr()
    e=g.Button('Start', name='run',size=10)
    e.connect(g.CLICK, gui_run, e)
    table.td(e)

    table.tr()
    table.td(g.Label('Speed:{:>4}'.format(self.fps),color=fg, \
                       name='label_speed',size=10), align=-1)
    table.tr()
    e = g.HSlider(self.fps,1,50,size=10,width=100,height=16,name='speed')
    e.connect(g.CHANGE, gui_speed, e)
    table.td(e, align=-1)
    table.tr()
    table.td(g.Container(height=5,size=10))

    table.tr()
    e=g.Button('Restart', name='restart',size=10)
    e.connect(g.CLICK, gui_restart, e)
    table.td(e)

    table.tr()
    cant= len(self.world.population)
    table.td(g.Label('Qtty:{:>5}'.format(cant),color=fg,\
              name='label_qtty',size=10),align=-1)
    table.tr()
    e =g.HSlider(cant,1,999,size=10,width=100,height=16,name='quantity')
    e.connect(g.CHANGE, gui_quantity, e)
    table.td(e,align=-1)

    for tipo in self.tipos:
        table.tr()
        color=self.tipos[tipo][1]
        cant='{:>14}'.format(len(self.world.population._types[tipo]))
        table.td(g.Label(value=cant,color=color,name='num_'+tipo,\
                            size=10),align=-1)

    table.tr()
    e=g.Button('Collisions', name='collisions',size=10)
    e.connect(g.CLICK, gui_collisions, e)
    table.td(e)

    table.tr()
    info=ShowInfo(width=100,name='info')
    table.td(info)

    cont=g.Container(width=100,height=self.size[1],\
                       background=GREY,align=-1)
    cont.add(table,0,0)
    container=g.Container(align=-1,valign=-1)
    container.add(cont,self.size[0]-100,0)
    return container

