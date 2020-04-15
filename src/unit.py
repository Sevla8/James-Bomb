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
	PORTAL_HIDDEN = 8
	PORTAL = 9
	GROUND = 10
	FLAME_0 = 11
	FLAME_1 = 12
	FLAME_2 = 13
	FLAME_3 = 14
	FLAME_4 = 15
	BOMB_POWERUP = 16
	FLAME_POWERUP = 17
