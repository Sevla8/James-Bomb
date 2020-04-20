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
from bomb import *
import random


class Boss(Bomberman):
    
    def __init__(self, change_direction = False , initial_position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y)):
        super(Boss, self).__init__(initial_position)
        self.alive = True
        if change_direction :
            self.direction = Direction.UP
        self.bombs = [Bomb(self)] * MAXIMAL_BOMB_AMOUNT

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

    def bombs_active(self,labyrinth):
        for bomb in list_bombs:
            if bomb.get_active():
                bomb.bomb_explose(labyrinth)

    def drop_bomb(self,labyrinth):
        if  self.alive and labyrinth.can_drop_bomb(self.position) and self.can_drop_bomb():
            bomb = self.bombs[self.skill.droped_bomb_amount]        
            bomb.droped(self.position,labyrinth)
            return