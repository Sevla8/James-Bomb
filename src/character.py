#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *

class Character:
	def __init__(self):
		""" Construit un personnage.
		"""
		self.right
		self.left
		self.front
		self.back
		self.move_index
		self.move_max
		self.position
		self.direction
		self.hp
		self.xp

	def move(self, direction):
		""" Fait se déplacer un personnage dans la direction caractérisé par 'direction'.
			Paramètres:
				'direction':
					<Direction>
					la direction courante du personnage
		"""
		if direction == Direction.RIGHT:
			self.position.x += 1
		if direction == Direction.LEFT:
			self.position.x -= 1
		if direction == Direction.UP:
			self.position.y -= 1
		if direction == Direction.DOWN:
			self.position.y += 1

	def turn(self, direction):
		""" Fait tourner un personnage vers la direction caractérisé par 'direction'.
			Paramètres:
				'direction':
					<Direction>
					la direction courante du personnage
		"""
		if direction == Direction.RIGHT:
			self.direction = Direction.RIGHT
		if direction == Direction.LEFT:
			self.direction = Direction.LEFT
		if direction == Direction.UP:
			self.direction = Direction.UP
		if direction == Direction.DOWN:
			self.direction = Direction.DOWN

	def update_move_index(self):
		""" Met à jour la valeur de l'attribut 'move_index' dand le but de donner au personnage une impression de marche lors de ses déplacements.
		"""
		self.move_index = (self.move_index + 1) % self.move_max

	def print(self, window, size_unit):
		""" Affiche le personnage dans la fenêtre caractérisé par 'window'.
			Paramètres:
				'window':
					<pygame.Surface>
					la fenetre courante
				'size_unit':
					<nombre>
					la taille en pixel d'une unité de surface
		"""
		if self.direction == Direction.RIGHT:
			window.blit(pygame.transform.scale(self.right[self.move_index], (size_unit, size_unit)), (self.position.x*size_unit, self.position.y*size_unit))
		elif self.direction == Direction.LEFT:
			window.blit(pygame.transform.scale(self.left[self.move_index], (size_unit, size_unit)), (self.position.x*size_unit, self.position.y*size_unit))
		elif self.direction == Direction.UP:
			window.blit(pygame.transform.scale(self.back[self.move_index], (size_unit, size_unit)), (self.position.x*size_unit, self.position.y*size_unit))
		else:
			window.blit(pygame.transform.scale(self.front[self.move_index], (size_unit, size_unit)), (self.position.x*size_unit, self.position.y*size_unit))
