#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

class Character:
	def __init__(self):
		self.right
		self.left
		self.front
		self.back
		self.position
		self.direction
		self.hp
		self.xp

	def move(self, direction):
		if direction == Direction.RIGHT:
			self.position.x += 1
		if direction == Direction.LEFT:
			self.position.x -= 1
		if direction == Direction.UP:
			#move_animation(self,direction):
			self.position.y -= 1
		if direction == Direction.DOWN:
			self.position.y += 1

	def turn(self, direction):
		if direction == Direction.RIGHT:
			self.direction = Direction.RIGHT
		if direction == Direction.LEFT:
			self.direction = Direction.LEFT
		if direction == Direction.UP:
			self.direction = Direction.UP
		if direction == Direction.DOWN:
			self.direction = Direction.DOWN

	def move_animation(self,direction):
		pass

	def print(self, window):
		if self.direction == Direction.RIGHT:
			window.blit(pygame.transform.scale(self.right, (SIZE_UNIT, SIZE_UNIT)), (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		elif self.direction == Direction.LEFT:
			window.blit(pygame.transform.scale(self.left, (SIZE_UNIT, SIZE_UNIT)), (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		elif self.direction == Direction.UP:
			window.blit(pygame.transform.scale(self.back, (SIZE_UNIT, SIZE_UNIT)), (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		else:
			window.blit(pygame.transform.scale(self.front, (SIZE_UNIT, SIZE_UNIT)), (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
