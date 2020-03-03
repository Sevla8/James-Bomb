#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

class Creep(Character):
	def __init__(self):
		self.right = pygame.image.load(CREEP_RIGHT).convert_alpha()
		self.left = pygame.image.load(CREEP_LEFT).convert_alpha()
		self.front = pygame.image.load(CREEP_FRONT).convert_alpha()
		self.back = pygame.image.load(CREEP_BACK).convert_alpha()
		self.hp = DEFAULT_HP_CREEP
		self.xp = DEFAULT_XP_CREEP
