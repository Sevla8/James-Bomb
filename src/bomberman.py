#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from direction import *
from unit import *
from position import *
from character import *
from skill import *

class Bomberman(Character):
	def __init__(self):
		""" Construit un Bomberman.
		"""
		self.right = [pygame.image.load(BOMBERMAN_RIGHT_0).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_1).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_2).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_3).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_4).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_5).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_6).convert_alpha(), pygame.image.load(BOMBERMAN_RIGHT_7).convert_alpha()]
		self.left = [pygame.image.load(BOMBERMAN_LEFT_0).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_1).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_2).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_3).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_4).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_5).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_6).convert_alpha(), pygame.image.load(BOMBERMAN_LEFT_7).convert_alpha()]
		self.front = [pygame.image.load(BOMBERMAN_FRONT_0).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_1).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_2).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_3).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_4).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_5).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_6).convert_alpha(), pygame.image.load(BOMBERMAN_FRONT_7).convert_alpha()]
		self.back = [pygame.image.load(BOMBERMAN_BACK_0).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_1).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_2).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_3).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_4).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_5).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_6).convert_alpha(), pygame.image.load(BOMBERMAN_BACK_7).convert_alpha()]
		self.move_index = 0
		self.move_max = BOMBERMAN_MOVE_MAX
		self.position = Position(BOMBERMAN_INITIAL_POSITION_X, BOMBERMAN_INITIAL_POSITION_Y);
		self.direction = Direction.DOWN
		self.hp = DEFAULT_HP_BOMBERMAN
		self.xp = DEFAULT_XP_BOMBERMAN
		self.skill = Skill()

	def can_drop_bomb(self):
		""" Retourne vrai si le joueur peu poser une nombe. Retourne faux sinon.
			Valeur de retour:
				<booléen>
				vrai si une bombe peut être posée, faux sinon
		"""
		return True if self.skill.bomb_amount - self.skill.droped_bomb_amount > 0 else False

	def drop_bomb(self):
		""" Augmente d'une unité le nombre de bombes posée par le joueur.
		"""
		self.skill.droped_bomb_amount += 1

	def bomb_explose(self):
		""" Diminue d'une unité le nombre de bombes posée par le joueur.
		"""
		self.skill.droped_bomb_amount -= 1

	def get_scope(self):
		""" Retourne la portée d'explosion des bombes du joueur.
			Valeur de retour:
				<nombre>
				la portée d'explosion des bombes du joueur
		"""
		return self.skill.scope

	def get_position(self):
		""" Retourne la position du joueur.
			Valeur de retour:
				<nombre>
				la position du joueur
		"""
		return self.position

	def print(self, window, size_unit):
		""" Affiche le bomberman dans la fenêtre caractérisé par 'window'.
			Paramètres:
				'window':
					<pygame.Surface>
					la fenetre courante
		"""
		if self.direction == Direction.RIGHT:
			window.blit(pygame.transform.scale(self.right[self.move_index], (size_unit, 2*size_unit)), (self.position.x*size_unit, (self.position.y-1)*size_unit))
		elif self.direction == Direction.LEFT:
			window.blit(pygame.transform.scale(self.left[self.move_index], (size_unit, 2*size_unit)), (self.position.x*size_unit, (self.position.y-1)*size_unit))
		elif self.direction == Direction.UP:
			window.blit(pygame.transform.scale(self.back[self.move_index], (size_unit, 2*size_unit)), (self.position.x*size_unit, (self.position.y-1)*size_unit))
		else:
			window.blit(pygame.transform.scale(self.front[self.move_index], (size_unit, 2*size_unit)), (self.position.x*size_unit, (self.position.y-1)*size_unit))
