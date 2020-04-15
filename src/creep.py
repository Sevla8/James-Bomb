#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *
from character import *

class Creep(Character):
	def __init__(self):
		""" Construit un Creep.
		"""
		self.right = [pygame.image.load(CREEP_RIGHT_0).convert_alpha(), pygame.image.load(CREEP_RIGHT_1).convert_alpha(), pygame.image.load(CREEP_RIGHT_2).convert_alpha(), pygame.image.load(CREEP_RIGHT_3).convert_alpha(), pygame.image.load(CREEP_RIGHT_4).convert_alpha(), pygame.image.load(CREEP_RIGHT_5).convert_alpha()]
		self.left = [pygame.image.load(CREEP_LEFT_0).convert_alpha(), pygame.image.load(CREEP_LEFT_1).convert_alpha(), pygame.image.load(CREEP_LEFT_2).convert_alpha(), pygame.image.load(CREEP_LEFT_3).convert_alpha(), pygame.image.load(CREEP_LEFT_4).convert_alpha(), pygame.image.load(CREEP_LEFT_5).convert_alpha()]
		self.front = [pygame.image.load(CREEP_FRONT_0).convert_alpha(), pygame.image.load(CREEP_FRONT_1).convert_alpha(), pygame.image.load(CREEP_FRONT_2).convert_alpha(), pygame.image.load(CREEP_FRONT_3).convert_alpha(), pygame.image.load(CREEP_FRONT_4).convert_alpha(), pygame.image.load(CREEP_FRONT_5).convert_alpha()]
		self.back = [pygame.image.load(CREEP_BACK_0).convert_alpha(), pygame.image.load(CREEP_BACK_1).convert_alpha(), pygame.image.load(CREEP_BACK_2).convert_alpha(), pygame.image.load(CREEP_BACK_3).convert_alpha(), pygame.image.load(CREEP_BACK_4).convert_alpha(), pygame.image.load(CREEP_BACK_5).convert_alpha()]
		self.move_index = 0
		self.move_max = CREEP_MOVE_MAX
		self.direction = Direction.DOWN
		self.position = Position()
		self.hp = DEFAULT_HP_CREEP
		self.xp = DEFAULT_XP_CREEP
