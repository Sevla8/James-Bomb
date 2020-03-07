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
	PORTAL = 5
	BOX = 6
	GROUND = 7
	FLAME_0 = 8
	FLAME_1 = 9
	FLAME_2 = 10
	FLAME_3 = 11
	FLAME_4 = 12
