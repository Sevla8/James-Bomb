#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *
from character import *

class Bomberman(Character):
	def __init__(self):
		self.right = pygame.image.load(BOMBERMAN_RIGHT).convert_alpha()
		self.left = pygame.image.load(BOMBERMAN_LEFT).convert_alpha()
		self.front = pygame.image.load(BOMBERMAN_FRONT).convert_alpha()
		self.back = pygame.image.load(BOMBERMAN_BACK).convert_alpha()
		self.position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y);
		self.direction = Direction.DOWN

	def print(self, window):
		if self.direction == Direction.RIGHT:
			window.blit(self.right, (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		elif self.direction == Direction.LEFT:
			window.blit(self.left, (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		elif self.direction == Direction.UP:
			window.blit(self.back, (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
		else:
			window.blit(self.front, (self.position.x*SIZE_UNIT, (self.position.y-1)*SIZE_UNIT))
