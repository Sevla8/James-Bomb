#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class OrderedEnum(Enum):
	def __ge__(self, other):
		if self.__class__ is other.__class__:
			return self.value >= other.value
		return NotImplemented
	def __gt__(self, other):
		if self.__class__ is other.__class__:
			return self.value > other.value
		return NotImplemented
	def __le__(self, other):
		if self.__class__ is other.__class__:
			return self.value <= other.value
		return NotImplemented
	def __lt__(self, other):
		if self.__class__ is other.__class__:
			return self.value < other.value
		return NotImplemented

class Unit(OrderedEnum):
	BLOCK = 1
	BOMB_1 = 2
	BOMB_2 = 3
	BOMB_3 = 4
	BOX = 5
	FLAME_POWERUP_HIDDEN = 6
	BOMB_POWERUP_HIDDEN = 7
	PORTAL = 8
	GROUND = 9
	FLAME_0 = 10
	FLAME_1 = 11
	FLAME_2 = 12
	FLAME_3 = 13
	FLAME_4 = 14
	BOMB_POWERUP = 15
	FLAME_POWERUP = 16
