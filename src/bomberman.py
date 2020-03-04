#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *
from character import *
from bomb import *

class Bomberman(Character):
	def __init__(self):
		self.right = pygame.image.load(BOMBERMAN_RIGHT).convert_alpha()
		self.left = pygame.image.load(BOMBERMAN_LEFT).convert_alpha()
		self.front = pygame.image.load(BOMBERMAN_FRONT).convert_alpha()
		self.back = pygame.image.load(BOMBERMAN_BACK).convert_alpha()
		self.position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y);
		self.direction = Direction.DOWN
		self.hp = DEFAULT_HP_BOMBERMAN
		self.xp = DEFAULT_XP_BOMBERMAN
		self.bombs = Bomb()

	def can_drop_bomb(self):
		return True if self.bombs.bomb_amount - self.bombs.droped_bomb_amount > 0 else False

	def drop_bomb(self):
		self.bombs.droped_bomb_amount += 1

	def print(self, window):
		if self.direction == Direction.RIGHT:
			window.blit(pygame.transform.scale(self.right, (SIZE_UNIT, 2*SIZE_UNIT)), (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		elif self.direction == Direction.LEFT:
			window.blit(pygame.transform.scale(self.left, (SIZE_UNIT, 2*SIZE_UNIT)), (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		elif self.direction == Direction.UP:
			window.blit(pygame.transform.scale(self.back, (SIZE_UNIT, 2*SIZE_UNIT)), (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		else:
			window.blit(pygame.transform.scale(self.front, (SIZE_UNIT, 2*SIZE_UNIT)), (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
