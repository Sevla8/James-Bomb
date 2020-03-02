#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
from constants import *
from unit import *
from direction import *

class Labyrinth:
	def __init__(self):
		self.ground = pygame.image.load(UNIT_GROUND)
		self.block = pygame.image.load(UNIT_BLOCK)
		self.box = pygame.image.load(UNIT_BOX)
		self.portal = pygame.image.load(UNIT_PORTAL)
		self.bomb = pygame.image.load(BOMB).convert_alpha()
		self.grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if j == Y_MIN or j == Y_MAX-1 or i == X_MIN or i == X_MAX-1 or j % 2 == 0 and i % 2 == 0:
					self.grid[j][i] = Unit.BLOCK

	def generate(self):
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] != Unit.BLOCK:
					if j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y+1 and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X+1:
						continue
					if (random.choice([True, True, False])):
						self.grid[j][i] = Unit.BOX

	def valid_move(self, position, direction):
		if direction == Direction.RIGHT:
			if self.grid[position.y][position.x+1] == Unit.GROUND:
				return True
		if direction == Direction.LEFT:
			if self.grid[position.y][position.x-1] == Unit.GROUND:
				return True
		if direction == Direction.UP:
			if self.grid[position.y-1][position.x] == Unit.GROUND:
				return True
		if direction == Direction.DOWN:
			if self.grid[position.y+1][position.x] == Unit.GROUND:
				return True
		return False

	def can_drop_bomb(self, position):
		return True if self.grid[position.y][position.x] == Unit.GROUND else False

	def drop_bomb(self, position):
		self.grid[position.y][position.x] = Unit.BOMB

	def print(self, window):
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.GROUND:
					window.blit(self.ground, (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BLOCK:
					window.blit(self.block, (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOX:
					window.blit(self.box, (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.PORTAL:
					window.blit(self.portal, (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOMB:
					window.blit(self.ground, (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(self.bomb, (i*SIZE_UNIT, j*SIZE_UNIT))
