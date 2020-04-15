#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from position import *

class Skill:
	def __init__(self):
		""" Construit un skill.
		"""
		self.bomb_amount = DEFAULT_BOMB_AMOUNT
		self.droped_bomb_amount = 0
		self.scope = DEFAULT_BOMB_SCOPE
