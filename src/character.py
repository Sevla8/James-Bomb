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
			window.blit(self.right, (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		elif self.direction == Direction.LEFT:
			window.blit(self.left, (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		elif self.direction == Direction.UP:
			window.blit(self.back, (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
		else:
			window.blit(self.front, (self.position.x*SIZE_UNIT, self.position.y*SIZE_UNIT))
