#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *
from character import *
from bomberman import *
from skill import *


class Mechant(Bomberman):
    
    def __init__(self, initial_position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y)):
        super(Mechant, self).__init__(initial_position)
        self.alive = True

    def touched(self,labyrinth):
        """
        Décrémente la vie de l'ennemie de 1 s'il lui en reste, sinon le déclare comme mort
        """
        if ( self.hp > 1):
            self.hp -= 1
            if ( self.hp == 2 ):
                self.position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y)
            else:
                 self.position = Position(BOMBERMAN_INITIAL_POSITION_X_2, BOMBERMAN_INITIAL_POSITION_Y_2)
        else:
            self.alive = False
            labyrinth.appear_portal(self.position)

    def get_alive(self):
        return self.alive