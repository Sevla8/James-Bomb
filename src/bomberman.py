#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

class Bomberman:
	def __init__(self):
		self.right = pygame.image.load(BOMBERMAN_RIGHT).convert_alpha()
		self.left = pygame.image.load(BOMBERMAN_LEFT).convert_alpha()
		self.front = pygame.image.load(BOMBERMAN_FRONT).convert_alpha()
		self.back = pygame.image.load(BOMBERMAN_BACK).convert_alpha()
		self.position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y);
		self.direction = Direction.DOWN

	def move(self, direction):
		if direction == Direction.RIGHT:
			self.position.x += 1
		if direction == Direction.LEFT:
			self.position.x -= 1
		if direction == Direction.UP:
			self.position.y -= 1
		if direction == Direction.DOWN:
			self.position.y += 1

	def change_position(self, direction):
		if direction == Direction.RIGHT:
			self.direction = Direction.RIGHT
		if direction == Direction.LEFT:
			self.direction = Direction.LEFT
		if direction == Direction.UP:
			self.direction = Direction.UP
		if direction == Direction.DOWN:
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
