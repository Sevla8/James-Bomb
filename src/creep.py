#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

class Creep(Character):
	def __init__(self):
		self.right = pygame.image.load(BOMBERMAN_RIGHT).convert_alpha()
		self.left = pygame.image.load(BOMBERMAN_LEFT).convert_alpha()
		self.front = pygame.image.load(BOMBERMAN_FRONT).convert_alpha()
		self.back = pygame.image.load(BOMBERMAN_BACK).convert_alpha()
		# self.position = Position(, );
		# self.direction = Direction.DOWN
