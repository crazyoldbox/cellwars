# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from constants import *
import os


class Animate():

    def __init__(self, object_, tick=10, ani_speed=10):

        self.object = object_
        self.user = 'Cell'#str(type(self.object))
        self.image =None
        self.images = None
        self.len_images = 0
        self.image_pos = 0
        self.tick = tick
        self.ani_speed = ani_speed

        self.loc = IMGDIR+self.user +'/'+ self.object.tipo + '/'

    def extractImages(self):

        location = self.loc + self.object.event
        animation_list = os.listdir(location)
        animation_list.sort()
        self.images = animation_list
        self.len_images = len(animation_list)

    def selectImage(self):
        if self.tick%self.ani_speed == 0:
            self.image = self.images[self.image_pos]
            self.image_pos = (self.image_pos+1)%self.len_images
            location = self.loc+ self.object.event +'/'+ self.image
            return pygame.image.load(location).convert_alpha()


    def createSprite(self):
        self.extractImages()
        sprite = pygame.sprite.Sprite()
        sprite.image = self.selectImage()
        if hasattr(self.object,'dir'):
            sprite.image = pygame.transform.rotate(sprite.image,\
                               - self.object.dir.get_angle()+270)

        sprite.rect = sprite.image.get_rect(center=self.object.pos)

        return sprite

