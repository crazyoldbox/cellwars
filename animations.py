# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from constants import *
import os


class Animate():

    cache = {} #To optimize pygame load

    def __init__(self, object_, ani_speed=3):

        self.object = object_
        self.user = 'Cell'#str(type(self.object))
        self.image_dir = None
        self.images = None
        self.len_images = 0
        self.image_pos = 0
        self.ani_speed = ani_speed
        self.loc = IMGDIR+self.user +'/'+ self.object.tipo + '/'
        self.status = None
        self.image = None
        self.sprite = pygame.sprite.Sprite()
        self.dir = None
        #Initialize
        self.createSprite(0)

    def extractImages(self):
        '''We extract the list of images from the location corresponding
           the actual status of the user and restes the position of the
           images to 0.'''

        location = self.loc + self.object.status
        animation_list = [a for a in os.listdir(location) if a.endswith('.png')]
        # or import glob; list=glob.glob(location+'/*.png')
        animation_list.sort()
        self.images = animation_list
        self.len_images = len(animation_list)
        self.image_pos = 0
        self.status = self.object.status

    def selectImage(self, ticks, force = False):
        '''Every ani_speed we change the image or if there was a change
           in status if not we use the image we already loaded previously'''
        if ticks%self.ani_speed == 0 or force:
            self.image_dir = self.images[self.image_pos]
            self.image_pos = (self.image_pos+1)%self.len_images
            location = self.loc+ self.object.status +'/'+ self.image_dir
            if location not in Animate.cache.keys():
                self.image = pygame.image.load(location).convert_alpha()
                Animate.cache[location] = self.image
            else: self.image = Animate.cache[location]

            self.sprite.image = self.image

        else:
            self.sprite.image = self.image

    def createSprite(self, ticks):
        '''We check if there was a change on status, if there was we
           update and force it to select a new image if there wasn`t we
           create the sprite rotate it and return it'''
        force = False
        if self.object.status != self.status:
            self.extractImages()
            force = True
        self.selectImage(ticks, force)

        if hasattr(self.object,'dir') :

            self.sprite.image = pygame.transform.rotate(self.sprite.image,\
                               - self.object.dir.get_angle()+270)

        self.sprite.rect = self.sprite.image.get_rect(center=self.object.pos)

        return self.sprite

