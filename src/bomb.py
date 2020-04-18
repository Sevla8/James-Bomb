#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

list_bombs = []

class Bomb:
    def __init__(self, holder = None, initial_position = Position()):
        self.position = Position(initial_position.x, initial_position.y)
        #self.holder.skill.scope = scope
        self.active = False
        self.holder = holder

        global list_bombs
        list_bombs.append(self)

    @staticmethod
    def find_bomb(position):
        global list_bombs
        for bomb in list_bombs:
            if ( bomb.position.x == position.x and bomb.position.y == position.y ):
                return bomb

    def set_active(self,value):
        if value:
            self.holder.skill.droped_bomb_amount += 1
        else:
            self.holder.skill.droped_bomb_amount -= 1

        self.active = value
    
    def get_active(self):
        return self.active

    def droped(self, position,labyrinth):
        self.position = Position(position.x,position.y)
        labyrinth.grid[self.position.y][self.position.x] = Unit.BOMB_1
        self.set_active(True)

    def bomb_explose(self,labyrinth):
        if (not self.active):
            return
        
        if labyrinth.grid[self.position.y][self.position.x] == Unit.BOMB_1:
            labyrinth.grid[self.position.y][self.position.x] = Unit.BOMB_2
        elif labyrinth.grid[self.position.y][self.position.x] == Unit.BOMB_2:
            labyrinth.grid[self.position.y][self.position.x] = Unit.BOMB_3
        elif labyrinth.grid[self.position.y][self.position.x] == Unit.BOMB_3:
            labyrinth.grid[self.position.y][self.position.x] = Unit.FLAME_0
            self.set_active(False)
            for k in range(self.position.y, max(Y_MIN, self.position.y-self.holder.skill.scope-1), -1):
                if labyrinth.grid[k][self.position.x] == Unit.GROUND:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                if labyrinth.grid[k][self.position.x] == Unit.PORTAL:
                    break
                if labyrinth.grid[k][self.position.x] == Unit.PORTAL_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.PORTAL
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOX:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BLOCK:
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOMB_POWERUP_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.BOMB_POWERUP
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOMB_POWERUP:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] == Unit.FLAME_POWERUP_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_POWERUP
                    break
                if labyrinth.grid[k][self.position.x] == Unit.FLAME_POWERUP:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] >= Unit.BOMB_1 and labyrinth.grid[k][self.position.x] <= Unit.BOMB_3:
                    #labyrinth.chain_reaction(Position(i, k), self.holder.skill.scope)
                    bomb = Bomb.find_bomb(Position(self.position.x,k))
                    self.bomb_explose(bomb)
                    break
            for k in range(self.position.y, min(Y_MAX, self.position.y+self.holder.skill.scope+1), 1):
                if labyrinth.grid[k][self.position.x] == Unit.GROUND:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                if labyrinth.grid[k][self.position.x] == Unit.PORTAL:
                    break
                if labyrinth.grid[k][self.position.x] == Unit.PORTAL_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.PORTAL
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOX:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BLOCK:
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOMB_POWERUP_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.BOMB_POWERUP
                    break
                if labyrinth.grid[k][self.position.x] == Unit.BOMB_POWERUP:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] == Unit.FLAME_POWERUP_HIDDEN:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_POWERUP
                    break
                if labyrinth.grid[k][self.position.x] == Unit.FLAME_POWERUP:
                    labyrinth.grid[k][self.position.x] = Unit.FLAME_0
                    break
                if labyrinth.grid[k][self.position.x] >= Unit.BOMB_1 and labyrinth.grid[k][self.position.x] <= Unit.BOMB_3:
                    #labyrinth.chain_reaction(Position(i, k), self.holder.skill.scope)
                    bomb = Bomb.find_bomb(Position(self.position.x,k))
                    self.bomb_explose(bomb)
                    break
            for k in range(self.position.x, max(X_MIN, self.position.x-self.holder.skill.scope-1), -1):
                if labyrinth.grid[self.position.y][k] == Unit.GROUND:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                if labyrinth.grid[self.position.y][k] == Unit.PORTAL:
                    break
                if labyrinth.grid[self.position.y][k] == Unit.PORTAL_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.PORTAL
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOX:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BLOCK:
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOMB_POWERUP_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.BOMB_POWERUP
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOMB_POWERUP:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] == Unit.FLAME_POWERUP_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_POWERUP
                    break
                if labyrinth.grid[self.position.y][k] == Unit.FLAME_POWERUP:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] >= Unit.BOMB_1 and labyrinth.grid[self.position.y][k] <= Unit.BOMB_3:
                    #labyrinth.chain_reaction(Position(k, j), self.holder.skill.scope)
                    bomb = Bomb.find_bomb(Position(k,self.position.y))
                    self.bomb_explose(bomb)
                    break
            for k in range(self.position.x, min(X_MAX, self.position.x+self.holder.skill.scope+1), 1):
                if labyrinth.grid[self.position.y][k] == Unit.GROUND:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                if labyrinth.grid[self.position.y][k] == Unit.PORTAL:
                    break
                if labyrinth.grid[self.position.y][k] == Unit.PORTAL_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.PORTAL
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOX:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BLOCK:
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOMB_POWERUP_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.BOMB_POWERUP
                    break
                if labyrinth.grid[self.position.y][k] == Unit.BOMB_POWERUP:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] == Unit.FLAME_POWERUP_HIDDEN:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_POWERUP
                    break
                if labyrinth.grid[self.position.y][k] == Unit.FLAME_POWERUP:
                    labyrinth.grid[self.position.y][k] = Unit.FLAME_0
                    break
                if labyrinth.grid[self.position.y][k] >= Unit.BOMB_1 and labyrinth.grid[self.position.y][k] <= Unit.BOMB_3:
                    #labyrinth.chain_reaction(Position(k, j), self.holder.skill.scope)
                    bomb = Bomb.find_bomb(Position(k,self.position.y))
                    self.bomb_explose(bomb)
                    break