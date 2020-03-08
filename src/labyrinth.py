#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector # il semble que ce module doit etre importé en premier sinon risque de boucle infinie
import random
import json
import pygame
from constants import *
from unit import *
from direction import *
from creep import *

class Labyrinth:
	def __init__(self):
		""" Construit un labyrinthe.
		"""
		self.ground = pygame.image.load(UNIT_GROUND)
		self.block = pygame.image.load(UNIT_BLOCK)
		self.box = pygame.image.load(UNIT_BOX)
		self.portal = pygame.image.load(UNIT_PORTAL)
		self.bomb = [pygame.image.load(BOMB_1).convert_alpha(), pygame.image.load(BOMB_2).convert_alpha(), pygame.image.load(BOMB_3).convert_alpha()]
		self.flame = [pygame.image.load(FLAME_0).convert_alpha(), pygame.image.load(FLAME_1).convert_alpha(), pygame.image.load(FLAME_2).convert_alpha(), pygame.image.load(FLAME_3).convert_alpha(), pygame.image.load(FLAME_4).convert_alpha()]
		self.list_explosion = []
		self.grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if j == Y_MIN or j == Y_MAX-1 or i == X_MIN or i == X_MAX-1 or j % 2 == 0 and i % 2 == 0:
					self.grid[j][i] = Unit.BLOCK
		self.creeps = []
		for i in range(DEFAULT_CREEP_AMOUNT):
			self.creeps.append(Creep())

	def load(self, stage):
		""" Charger un labyrinthe en fonction de l'avancement dans le jeu (caractérisé par 'stage').
			Paramètres:
				'stage':
					<entier>
					caractérise un labyrinthe
		"""
		try:
			db = mysql.connector.connect(host='localhost',
										database='Bomberman',
										user='root',
										password='')
			cursor = db.cursor()
			query = "SELECT grid FROM Stages WHERE id_stage = %s"
			cursor.execute(query, (stage,))
			record = cursor.fetchone()[0]
			cursor.close()

			json_grid = record
			#json_grid = record.decode("utf-8")
			grid = json.loads(json_grid)
			for j in range(Y_MIN, Y_MAX):
				for i in range(X_MIN, X_MAX):
					self.grid[j][i] = Unit.GROUND if grid[j][i] == "ground" else Unit.BLOCK if grid[j][i] == "block" else Unit.BOX if grid[j][i] == "box" else Unit.PORTAL if grid[j][i] == "portal" else Unit.BOMB

		except mysql.connector.Error as e:
			print("Error while connecting to MySQL", e)

		finally:
			if (db.is_connected()):
				cursor.close()
				db.close()

	def generate_creeps(self):
		for creep in self.creeps:
			# On teste si la place est valide, non occupée et pas trop proche du joueur
			attempt = Position(random.randint(BOMBERMAN_INITIAL_POSITION_X+5, X_MAX-1), random.randint(BOMBERMAN_INITIAL_POSITION_Y+5, Y_MAX-1))
			while self.grid[attempt.y][attempt.x] != Unit.GROUND or self.invalid_creep_initial_position(attempt):
				attempt = Position(random.randint(BOMBERMAN_INITIAL_POSITION_X+5, X_MAX-1), random.randint(BOMBERMAN_INITIAL_POSITION_Y+5, Y_MAX-1))
			# On attribut la place au creep
			creep.position = attempt

	def invalid_creep_initial_position(self, position):
		for creep in self.creeps:
			if creep.position.y == position.y and creep.position.x == position.x:
				return True
		return False

	def generate(self):
		""" Génére un labyrinthe dont les composants seront disposés de manière aléatoire. Certains composants ont cependant une disposition prédéfinie et constante.
		"""
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] != Unit.BLOCK:
					if j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y+1 and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X+1:
						continue
					if (random.choice([True, False])):
						self.grid[j][i] = Unit.BOX
		self.generate_creeps()

	def save(self):
		""" Sauvegarde un labyrinthe. Pour le moment utilisé pour créer des labyrinthes dans la base de donnée. À terme servira à sauvegarder la progression du joueur.
		"""
		grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				grid[j][i] = "ground" if self.grid[j][i] == Unit.GROUND else "block" if self.grid[j][i] == Unit.BLOCK else "box" if self.grid[j][i] == Unit.BOX else "portal" if self.grid[j][i] == Unit.PORTAL else "bomb"
		json_grid = json.dumps(grid)

		try:
			db = mysql.connector.connect(host='localhost',
										database='Bomberman',
										user='root',
										password='')

			cursor = db.cursor()
			query = "INSERT INTO Stages (id_stage, grid) VALUES (%s, %s)"
			cursor.execute(query, (None, json_grid))
			db.commit()
			cursor.close()

		except mysql.connector.Error as e:
			print("Error while connecting to MySQL", e)

		finally:
			if (db.is_connected()):
				cursor.close()
				db.close()

	def valid_move(self, position, direction):
		""" Retourne vrai si le mouvement caractérisé par 'position' et 'direction est valide. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la position du personnage dans le labyrinthe
				'direction':
					<Direction>
					la direction courante du personnage
			Valeur de retour:
				<booléen>
				vrai si mouvement valide, faux sinon
		"""
		#On peut marcher sur le sol, dans les flammes, sur le portal
		if direction == Direction.RIGHT:
			if self.grid[position.y][position.x+1] >= Unit.GROUND or self.grid[position.y][position.x+1] == Unit.PORTAL :
				return True
		if direction == Direction.LEFT:
			if self.grid[position.y][position.x-1] >= Unit.GROUND or self.grid[position.y][position.x-1] == Unit.PORTAL :
				return True
		if direction == Direction.UP:
			if self.grid[position.y-1][position.x] >= Unit.GROUND or self.grid[position.y-1][position.x] == Unit.PORTAL :
				return True
		if direction == Direction.DOWN:
			if self.grid[position.y+1][position.x] >= Unit.GROUND or self.grid[position.y+1][position.x] == Unit.PORTAL :
				return True
		return False

	def creep_collision(self, position, direction):
		for creep in self.creeps:
			if direction == Direction.RIGHT:
				if creep.position.y == position.y and creep.position.x == position.x+1:
					return True
			if direction == Direction.LEFT:
				if creep.position.y == position.y and creep.position.x == position.x-1:
					return True
			if direction == Direction.UP:
				if creep.position.y-1 == position.y and creep.position.x == position.x:
					return True
			if direction == Direction.DOWN:
				if creep.position.y+1 == position.y and creep.position.x == position.x:
					return True
		return False

	def move_creeps(self):
		for creep in self.creeps:
			# si le creep peut continuer tout droit alors il continue tout droit
			if self.valid_move(creep.position, creep.direction) and not self.creep_collision(creep.position, creep.direction):
				creep.move(creep.direction)
			# sinon on cherche une autre direction au hasard
			else:
				dead_end = False
				if self.grid[creep.position.y+1][creep.position.x] != Unit.GROUND and self.grid[creep.position.y-1][creep.position.x] != Unit.GROUND and self.grid[creep.position.y][creep.position.x+1] != Unit.GROUND and self.grid[creep.position.y][creep.position.x-1] != Unit.GROUND:
					dead_end = True
				if not dead_end:
					next_direction = random.choice([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])
					while not self.valid_move(creep.position, next_direction):
						next_direction = random.choice([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])
					# si collision le creep ne fait que se tourner
					if self.creep_collision(creep.position, next_direction):
						creep.turn(next_direction)
					else:
						creep.turn(next_direction)
						creep.move(next_direction)

	def can_drop_bomb(self, position):
		""" Retourne vrai si une bombe peut être posée à l'emplacement caractérisé par 'position'. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la position du personnage dans le labyrinthe
			Valeur de retour:
				<booléen>
				vrai si une bombe peut être posée, faux sinon
		"""
		return True if self.grid[position.y][position.x] == Unit.GROUND else False

	def drop_bomb(self, position):
		""" Pose une bombe à l'emplacement caractérisé par 'position'.
			Paramètres:
				'position':
					<Position>
					la position du personnage dans le labyrinthe
		"""
		self.grid[position.y][position.x] = Unit.BOMB_1

	def bomb_explose(self,bomberman):
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.BOMB_1:
					self.grid[j][i] = Unit.BOMB_2
				elif self.grid[j][i] == Unit.BOMB_2:
					self.grid[j][i] = Unit.BOMB_3
				elif self.grid[j][i] == Unit.BOMB_3:
					self.grid[j][i] = Unit.GROUND
					self.explosion(i,j,bomberman)
					

	def explosion(self,x,y,bomberman):
		#  "  and self.grid[j][x] >= Unit.BOX ):   "
		#pas de block, portal ou autre bombe
		j = y
		no_box_destroy = True
		while ( j < min(Y_MAX,y+bomberman.get_scope()+1) and self.grid[j][x] >= Unit.BOX and no_box_destroy ):
			if ( self.grid[j][x] == Unit.BOX ):
				no_box_destroy = False
			self.grid[j][x] = Unit.FLAME_0
			j += 1

		j = y
		no_box_destroy = True
		while ( j > max(Y_MIN,y-bomberman.get_scope()-1) and self.grid[j][x] >= Unit.BOX and no_box_destroy ):
			if ( self.grid[j][x] == Unit.BOX ):
				no_box_destroy = False
			self.grid[j][x] = Unit.FLAME_0
			j -= 1

		i = x
		no_box_destroy = True
		while ( i < min(X_MAX,x+bomberman.get_scope()+1) and self.grid[y][i] >= Unit.BOX and no_box_destroy ):
			if ( self.grid[y][i] == Unit.BOX ):
				no_box_destroy = False
			self.grid[y][i] = Unit.FLAME_0
			i += 1

		i = x
		no_box_destroy = True
		while ( i > max(X_MIN,x-bomberman.get_scope()-1) and self.grid[y][i] >= Unit.BOX and no_box_destroy ):
			if ( self.grid[y][i] == Unit.BOX ):
				no_box_destroy = False
			self.grid[y][i] = Unit.FLAME_0
			i -= 1


		for creep in self.creeps:
			if (self.grid[creep.position.y][creep.position.x] >= Unit.FLAME_0 and self.grid[creep.position.y][creep.position.x] <= Unit.FLAME_4):
				self.creeps.remove(creep)

		#Bomberman touché
		if (self.grid[bomberman.position.y][bomberman.position.x] >= Unit.FLAME_0 and self.grid[bomberman.position.y][bomberman.position.x] <= Unit.FLAME_4):
			bomberman.position.y = Y_MIN + 1
			bomberman.position.x = X_MIN + 1

	def burning(self):
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.FLAME_0:
					self.grid[j][i] = Unit.FLAME_1
				elif self.grid[j][i] == Unit.FLAME_1:
					self.grid[j][i] = Unit.FLAME_2
				elif self.grid[j][i] == Unit.FLAME_2:
					self.grid[j][i] = Unit.FLAME_3
				elif self.grid[j][i] == Unit.FLAME_3:
					self.grid[j][i] = Unit.FLAME_4
				elif self.grid[j][i] == Unit.FLAME_4:
					self.grid[j][i] = Unit.GROUND


	def update_creeps_move_index(self):
		for creep in self.creeps:
			creep.update_move_index()

	def print(self, window):
		""" Affiche le labyrinthe dans la fenêtre caractérisé par 'window'.
			Paramètres:
				'window':
					<pygame.Surface>
					la fenetre courante
		"""
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.GROUND:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BLOCK:
					window.blit(pygame.transform.scale(self.block, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOX:
					window.blit(pygame.transform.scale(self.box, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.PORTAL:
					window.blit(pygame.transform.scale(self.portal, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOMB_1:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.bomb[0], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOMB_2:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.bomb[1], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.BOMB_3:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.bomb[2], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.FLAME_0:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.flame[0], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.FLAME_1:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.flame[1], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.FLAME_2:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.flame[2], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.FLAME_3:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.flame[3], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
				elif self.grid[j][i] == Unit.FLAME_4:
					window.blit(pygame.transform.scale(self.ground, (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(pygame.transform.scale(self.flame[4], (SIZE_UNIT, SIZE_UNIT)), (i*SIZE_UNIT, j*SIZE_UNIT))
		for creep in self.creeps:
			creep.print(window)
