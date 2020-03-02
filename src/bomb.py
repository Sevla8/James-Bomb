#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from position import *

class Bomb:
	def __init__(self):
		self.bomb_amount = DEFAULT_BOMB_AMOUNT
		self.droped_bomb_amount = 0
		self.scope = DEFAULT_BOMB_SCOPE
