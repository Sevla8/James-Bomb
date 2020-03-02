#!/usr/bin/python
# -*- coding: utf-8 -*-

from constants import *

class Bomb:
	def __init__(self):
		self.bomb_amount = DEFAULT_BOMB_AMOUNT
		self.droped_bombs = 0
		self.scope = DEFAULT_BOMB_SCOPE
