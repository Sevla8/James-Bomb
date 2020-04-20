#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
import random
import json
import pygame
from constants import *
from unit import *
from direction import *
from creep import *

class Labyrinth:
	def __init__(self, multiplayer = False):
		""" Construit un labyrinthe.
		"""
		self.ground = pygame.image.load(UNIT_GROUND)
		self.block = pygame.image.load(UNIT_BLOCK)
		self.box = pygame.image.load(UNIT_BOX)
		self.portal = pygame.image.load(UNIT_PORTAL).convert_alpha()
		self.bomb = [pygame.image.load(BOMB_1).convert_alpha(), pygame.image.load(BOMB_2).convert_alpha(), pygame.image.load(BOMB_3).convert_alpha()]
		self.flame = [pygame.image.load(FLAME_0).convert_alpha(), pygame.image.load(FLAME_1).convert_alpha(), pygame.image.load(FLAME_2).convert_alpha(), pygame.image.load(FLAME_3).convert_alpha(), pygame.image.load(FLAME_4).convert_alpha()]
		self.powerups = [pygame.image.load(BOMB_POWERUP), pygame.image.load(FLAME_POWERUP)]
		self.grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if j == Y_MIN or j == Y_MAX-1 or i == X_MIN or i == X_MAX-1 or j % 2 == 0 and i % 2 == 0:
					self.grid[j][i] = Unit.BLOCK
		self.creeps = []
		if not multiplayer:
			for i in range(DEFAULT_CREEP_AMOUNT):
				self.creeps.append(Creep())
		self.multiplayer = multiplayer

	def generate(self):
		""" Génére un labyrinthe dont les composants seront disposés de manière aléatoire. Certains composants ont cependant une disposition prédéfinie et constante.
		"""
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] != Unit.BLOCK:
					if j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y+1 and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X+1:
						continue
					if self.multiplayer and j == BOMBERMAN_INITIAL_POSITION_Y_2 and i == BOMBERMAN_INITIAL_POSITION_X_2 or j == BOMBERMAN_INITIAL_POSITION_Y_2-1 and i == BOMBERMAN_INITIAL_POSITION_X_2 or j == BOMBERMAN_INITIAL_POSITION_Y_2 and i == BOMBERMAN_INITIAL_POSITION_X_2-1:
						continue
					if random.choice([True, False]):
						if random.choice([True, False, False, False, False, False, False, False, False, False]):
							self.grid[j][i] = Unit.BOMB_POWERUP_HIDDEN
						elif random.choice([True, False, False, False, False, False, False, False, False]):
							self.grid[j][i] = Unit.FLAME_POWERUP_HIDDEN
						else:
							self.grid[j][i] = Unit.BOX
		if not self.multiplayer:
			portal_ok = False
			while not portal_ok:
				y = random.randint(Y_MIN, Y_MAX-1)
				x = random.randint(X_MIN, X_MAX-1)
				if self.grid[y][x] == Unit.BOX:
					self.grid[y][x] = Unit.PORTAL_HIDDEN
					portal_ok = True
		if not self.multiplayer:
			self.generate_creeps()

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
			query = "SELECT grid, creeps FROM Stages WHERE id_stage = %s"
			cursor.execute(query, (stage,))
			record = cursor.fetchone()
			cursor.close()

			json_grid = record[0]
			json_creeps = record[1]

			grid = json.loads(json_grid)
			for j in range(Y_MIN, Y_MAX):
				for i in range(X_MIN, X_MAX):
					self.grid[j][i] = Unit.GROUND if grid[j][i] == "ground" else Unit.BLOCK if grid[j][i] == "block" else Unit.BOX if grid[j][i] == "box" else Unit.PORTAL_HIDDEN if grid[j][i] == "portal_hidden" else Unit.FLAME_POWERUP_HIDDEN if grid[j][i] == "flame_powerup_hidden" else Unit.BOMB_POWERUP_HIDDEN

			creeps = json.loads(json_creeps)
			for k in range(0, len(creeps)):
				self.creeps[k].position.x = creeps[k][0]
				self.creeps[k].position.y = creeps[k][1]

		except mysql.connector.Error as e:
			print("Error while connecting to MySQL", e)

		finally:
			if (db.is_connected()):
				cursor.close()
				db.close()

	def save(self):
		""" Sauvegarde un labyrinthe. Pour le moment utilisé pour créer des labyrinthes dans la base de donnée. À terme servira à sauvegarder la progression du joueur.
		"""
		grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				grid[j][i] = "ground" if self.grid[j][i] == Unit.GROUND else "block" if self.grid[j][i] == Unit.BLOCK else "box" if self.grid[j][i] == Unit.BOX else "portal_hidden" if self.grid[j][i] == Unit.PORTAL_HIDDEN else "flame_powerup_hidden" if self.grid[j][i] == Unit.FLAME_POWERUP_HIDDEN else "bomb_powerup_hidden"
		json_grid = json.dumps(grid)

		ennemies = []
		for creep in self.creeps:
			ennemies.append([creep.position.x, creep.position.y])
		json_ennemies = json.dumps(ennemies)

		try:
			db = mysql.connector.connect(host='localhost',
										database='Bomberman',
										user='root',
										password='')

			cursor = db.cursor()
			query = "INSERT INTO Stages (id_stage, grid, creeps) VALUES (%s, %s, %s)"
			cursor.execute(query, (None, json_grid, json_ennemies))
			db.commit()
			cursor.close()

		except mysql.connector.Error as e:
			print("Error while connecting to MySQL", e)

		finally:
			if (db.is_connected()):
				cursor.close()
				db.close()

	def generate_creeps(self):
		""" Génère de manière aléatoire des creeps sur le labyrinthe.
		"""
		for creep in self.creeps:
			# On teste si la place est valide, non occupée et pas trop proche du joueur
			attempt = Position(random.randint(BOMBERMAN_INITIAL_POSITION_X+5, X_MAX-1), random.randint(BOMBERMAN_INITIAL_POSITION_Y+5, Y_MAX-1))
			while self.grid[attempt.y][attempt.x] != Unit.GROUND or self.invalid_creep_initial_position(attempt):
				attempt = Position(random.randint(BOMBERMAN_INITIAL_POSITION_X+5, X_MAX-1), random.randint(BOMBERMAN_INITIAL_POSITION_Y+5, Y_MAX-1))
			# On attribut la place au creep
			creep.position = attempt

	def invalid_creep_initial_position(self, position):
		""" Retourne vrai si un creep ne peu être positionné à la position caractérisée par 'position'. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la possible position du creep considéré dans le labyrinthe
			Valeur de retour:
				<booléen>
				vrai si la position est valide, faux sinon
		"""
		for creep in self.creeps:
			if creep.position.y == position.y and creep.position.x == position.x:
				return True
		return False

	def valid_move(self, position, direction):
		""" Retourne vrai si le mouvement caractérisé par 'position' et 'direction' est valide. Retourne faux sinon.
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
		# On peut marcher sur le sol, dans les flammes, sur le portal visible, sur les bonus visibles.
		if direction == Direction.RIGHT:
			if self.grid[position.y][position.x+1] >= Unit.PORTAL:
				return True
		if direction == Direction.LEFT:
			if self.grid[position.y][position.x-1] >= Unit.PORTAL:
				return True
		if direction == Direction.UP:
			if self.grid[position.y-1][position.x] >= Unit.PORTAL:
				return True
		if direction == Direction.DOWN:
			if self.grid[position.y+1][position.x] >= Unit.PORTAL:
				return True
		return False

	def creep_collision(self, position, direction):
		""" Retourne vrai si un creep caractérisé par 'position' et 'direction' peut rentrer en collision avec un autre.
			Paramètres:
				'position':
					<Position>
					la position du creep dans le labyrinthe
				'direction':
					<Direction>
					la direction courante du creep
			Valeur de retour:
				<booléen>
				vrai si collision possible, faux sinon
		"""
		for creep in self.creeps:
			if direction == Direction.RIGHT:
				if position.y == creep.position.y and position.x+1 == creep.position.x:
					return True
			if direction == Direction.LEFT:
				if position.y == creep.position.y and position.x-1 == creep.position.x:
					return True
			if direction == Direction.UP:
				if position.y-1 == creep.position.y and position.x == creep.position.x:
					return True
			if direction == Direction.DOWN:
				if position.y+1 == creep.position.y and position.x == creep.position.x:
					return True
		return False

	def move_creeps(self):
		""" Fait déplacer les creeps au seins du labyrinthe.
		"""
		for creep in self.creeps:
			# si le creep peut continuer tout droit alors il continue tout droit
			if self.valid_move(creep.position, creep.direction) and not self.creep_collision(creep.position, creep.direction):
				creep.move(creep.direction)
				if self.grid[creep.position.y][creep.position.x] == Unit.BOMB_POWERUP:
					self.grid[creep.position.y][creep.position.x] = Unit.GROUND
				elif self.grid[creep.position.y][creep.position.x] == Unit.FLAME_POWERUP:
					self.grid[creep.position.y][creep.position.x] = Unit.GROUND
			# sinon on cherche une autre direction au hasard
			else:
				dead_end = False
				if self.grid[creep.position.y+1][creep.position.x] <= Unit.PORTAL and self.grid[creep.position.y-1][creep.position.x] <= Unit.PORTAL and self.grid[creep.position.y][creep.position.x+1] <= Unit.PORTAL and self.grid[creep.position.y][creep.position.x-1] <= Unit.PORTAL:
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
						if self.grid[creep.position.y][creep.position.x] == Unit.BOMB_POWERUP:
							self.grid[creep.position.y][creep.position.x] = Unit.GROUND
						elif self.grid[creep.position.y][creep.position.x] == Unit.FLAME_POWERUP:
							self.grid[creep.position.y][creep.position.x] = Unit.GROUND

	def move_boss(self, boss):
		if not boss.get_alive:
			return
			
		if self.valid_move(boss.position, boss.direction):
			boss.move(boss.direction)
			if self.grid[boss.position.y][boss.position.x] == Unit.BOMB_POWERUP:
				self.grid[boss.position.y][boss.position.x] = Unit.GROUND
			elif self.grid[boss.position.y][boss.position.x] == Unit.FLAME_POWERUP:
				self.grid[boss.position.y][boss.position.x] = Unit.GROUND
        # sinon on cherche une autre direction au hasard
		else:
			dead_end = False
			if self.grid[boss.position.y+1][boss.position.x] <= Unit.PORTAL and self.grid[boss.position.y-1][boss.position.x] <= Unit.PORTAL and self.grid[boss.position.y][boss.position.x+1] <= Unit.PORTAL and self.grid[boss.position.y][boss.position.x-1] <= Unit.PORTAL:
				dead_end = True
			if not dead_end:
				next_direction = random.choice([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])
				while not self.valid_move(boss.position, next_direction):
					next_direction = random.choice([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])
                # si collision le creep ne fait que se tourner
				boss.turn(next_direction)
				boss.move(next_direction)

	

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

	def bomb_explose(self, scope):
		""" Fait exploser les bombes sur le labyrinthe avec une porté caractérisé par 'scope'.
			Paramètres:
				'scope':
					<nombre>
					la portée des bombes du bomberman
		"""
		#scope = bomberman.get_scope()
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.BOMB_1:
					self.grid[j][i] = Unit.BOMB_2
				elif self.grid[j][i] == Unit.BOMB_2:
					self.grid[j][i] = Unit.BOMB_3
				elif self.grid[j][i] == Unit.BOMB_3:
					self.grid[j][i] = Unit.FLAME_0
					for k in range(j, max(Y_MIN, j-scope-1), -1):
						if self.grid[k][i] == Unit.GROUND:
							self.grid[k][i] = Unit.FLAME_0
						if self.grid[k][i] == Unit.PORTAL:
							break
						if self.grid[k][i] == Unit.PORTAL_HIDDEN:
							self.grid[k][i] = Unit.PORTAL
							break
						if self.grid[k][i] == Unit.BOX:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] == Unit.BLOCK:
							break
						if self.grid[k][i] == Unit.BOMB_POWERUP_HIDDEN:
							self.grid[k][i] = Unit.BOMB_POWERUP
							break
						if self.grid[k][i] == Unit.BOMB_POWERUP:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] == Unit.FLAME_POWERUP_HIDDEN:
							self.grid[k][i] = Unit.FLAME_POWERUP
							break
						if self.grid[k][i] == Unit.FLAME_POWERUP:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] >= Unit.BOMB_1 and self.grid[k][i] <= Unit.BOMB_3:
							self.chain_reaction(Position(i, k), scope)
							break
					for k in range(j, min(Y_MAX, j+scope+1), 1):
						if self.grid[k][i] == Unit.GROUND:
							self.grid[k][i] = Unit.FLAME_0
						if self.grid[k][i] == Unit.PORTAL:
							break
						if self.grid[k][i] == Unit.PORTAL_HIDDEN:
							self.grid[k][i] = Unit.PORTAL
							break
						if self.grid[k][i] == Unit.BOX:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] == Unit.BLOCK:
							break
						if self.grid[k][i] == Unit.BOMB_POWERUP_HIDDEN:
							self.grid[k][i] = Unit.BOMB_POWERUP
							break
						if self.grid[k][i] == Unit.BOMB_POWERUP:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] == Unit.FLAME_POWERUP_HIDDEN:
							self.grid[k][i] = Unit.FLAME_POWERUP
							break
						if self.grid[k][i] == Unit.FLAME_POWERUP:
							self.grid[k][i] = Unit.FLAME_0
							break
						if self.grid[k][i] >= Unit.BOMB_1 and self.grid[k][i] <= Unit.BOMB_3:
							self.chain_reaction(Position(i, k), scope)
							break
					for k in range(i, max(X_MIN, i-scope-1), -1):
						if self.grid[j][k] == Unit.GROUND:
							self.grid[j][k] = Unit.FLAME_0
						if self.grid[j][k] == Unit.PORTAL:
							break
						if self.grid[j][k] == Unit.PORTAL_HIDDEN:
							self.grid[j][k] = Unit.PORTAL
							break
						if self.grid[j][k] == Unit.BOX:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] == Unit.BLOCK:
							break
						if self.grid[j][k] == Unit.BOMB_POWERUP_HIDDEN:
							self.grid[j][k] = Unit.BOMB_POWERUP
							break
						if self.grid[j][k] == Unit.BOMB_POWERUP:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] == Unit.FLAME_POWERUP_HIDDEN:
							self.grid[j][k] = Unit.FLAME_POWERUP
							break
						if self.grid[j][k] == Unit.FLAME_POWERUP:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] >= Unit.BOMB_1 and self.grid[j][k] <= Unit.BOMB_3:
							self.chain_reaction(Position(k, j), scope)
							break
					for k in range(i, min(X_MAX, i+scope+1), 1):
						if self.grid[j][k] == Unit.GROUND:
							self.grid[j][k] = Unit.FLAME_0
						if self.grid[j][k] == Unit.PORTAL:
							break
						if self.grid[j][k] == Unit.PORTAL_HIDDEN:
							self.grid[j][k] = Unit.PORTAL
							break
						if self.grid[j][k] == Unit.BOX:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] == Unit.BLOCK:
							break
						if self.grid[j][k] == Unit.BOMB_POWERUP_HIDDEN:
							self.grid[j][k] = Unit.BOMB_POWERUP
							break
						if self.grid[j][k] == Unit.BOMB_POWERUP:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] == Unit.FLAME_POWERUP_HIDDEN:
							self.grid[j][k] = Unit.FLAME_POWERUP
							break
						if self.grid[j][k] == Unit.FLAME_POWERUP:
							self.grid[j][k] = Unit.FLAME_0
							break
						if self.grid[j][k] >= Unit.BOMB_1 and self.grid[j][k] <= Unit.BOMB_3:
							self.chain_reaction(Position(k, j), scope)
							break

	def chain_reaction(self, position, scope):
		""" Fait exploser les bombes qui sont déclanchés par une explosion en chaîne sur le labyrinthe avec une porté caractérisé par 'scope'.
			Paramètres:
				'position':
					<Position>
					la position de la bombe entrainant la réaction en chaîne dans le labyrinthe
				'scope':
					<nombre>
					la portée des bombes du bomberman
		"""
		j = position.y
		i = position.x
		self.grid[j][i] = Unit.FLAME_0
		for k in range(j, max(Y_MIN, j-scope-1), -1):
			if self.grid[k][i] == Unit.GROUND:
				self.grid[k][i] = Unit.FLAME_0
			if self.grid[k][i] == Unit.PORTAL:
				break
			if self.grid[k][i] == Unit.PORTAL_HIDDEN:
				self.grid[k][i] = Unit.PORTAL
				break
			if self.grid[k][i] == Unit.BOX:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] == Unit.BLOCK:
				break
			if self.grid[k][i] == Unit.BOMB_POWERUP_HIDDEN:
				self.grid[k][i] = Unit.BOMB_POWERUP
				break
			if self.grid[k][i] == Unit.BOMB_POWERUP:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] == Unit.FLAME_POWERUP_HIDDEN:
				self.grid[k][i] = Unit.FLAME_POWERUP
				break
			if self.grid[k][i] == Unit.FLAME_POWERUP:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] >= Unit.BOMB_1 and self.grid[k][i] <= Unit.BOMB_3:
				self.chain_reaction(Position(i, k), scope)
				break
		for k in range(j, min(Y_MAX, j+scope+1), 1):
			if self.grid[k][i] == Unit.GROUND:
				self.grid[k][i] = Unit.FLAME_0
			if self.grid[k][i] == Unit.PORTAL:
				break
			if self.grid[k][i] == Unit.PORTAL_HIDDEN:
				self.grid[k][i] = Unit.PORTAL
				break
			if self.grid[k][i] == Unit.BOX:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] == Unit.BLOCK:
				break
			if self.grid[k][i] == Unit.BOMB_POWERUP_HIDDEN:
				self.grid[k][i] = Unit.BOMB_POWERUP
				break
			if self.grid[k][i] == Unit.BOMB_POWERUP:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] == Unit.FLAME_POWERUP_HIDDEN:
				self.grid[k][i] = Unit.FLAME_POWERUP
				break
			if self.grid[k][i] == Unit.FLAME_POWERUP:
				self.grid[k][i] = Unit.FLAME_0
				break
			if self.grid[k][i] >= Unit.BOMB_1 and self.grid[k][i] <= Unit.BOMB_3:
				self.chain_reaction(Position(i, k), scope)
				break
		for k in range(i, max(X_MIN, i-scope-1), -1):
			if self.grid[j][k] == Unit.GROUND:
				self.grid[j][k] = Unit.FLAME_0
			if self.grid[j][k] == Unit.PORTAL:
				break
			if self.grid[j][k] == Unit.PORTAL_HIDDEN:
				self.grid[j][k] = Unit.PORTAL
				break
			if self.grid[j][k] == Unit.BOX:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] == Unit.BLOCK:
				break
			if self.grid[j][k] == Unit.BOMB_POWERUP_HIDDEN:
				self.grid[j][k] = Unit.BOMB_POWERUP
				break
			if self.grid[j][k] == Unit.BOMB_POWERUP:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] == Unit.FLAME_POWERUP_HIDDEN:
				self.grid[j][k] = Unit.FLAME_POWERUP
				break
			if self.grid[j][k] == Unit.FLAME_POWERUP:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] >= Unit.BOMB_1 and self.grid[j][k] <= Unit.BOMB_3:
				self.chain_reaction(Position(k, j), scope)
				break
		for k in range(i, min(X_MAX, i+scope+1), 1):
			if self.grid[j][k] == Unit.GROUND:
				self.grid[j][k] = Unit.FLAME_0
			if self.grid[j][k] == Unit.PORTAL:
				break
			if self.grid[j][k] == Unit.PORTAL_HIDDEN:
				self.grid[j][k] = Unit.PORTAL
				break
			if self.grid[j][k] == Unit.BOX:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] == Unit.BLOCK:
				break
			if self.grid[j][k] == Unit.BOMB_POWERUP_HIDDEN:
				self.grid[j][k] = Unit.BOMB_POWERUP
				break
			if self.grid[j][k] == Unit.BOMB_POWERUP:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] == Unit.FLAME_POWERUP_HIDDEN:
				self.grid[j][k] = Unit.FLAME_POWERUP
				break
			if self.grid[j][k] == Unit.FLAME_POWERUP:
				self.grid[j][k] = Unit.FLAME_0
				break
			if self.grid[j][k] >= Unit.BOMB_1 and self.grid[j][k] <= Unit.BOMB_3:
				self.chain_reaction(Position(k, j), scope)
				break

	def bomberman_touched(self, position):
		""" Retourne vrai si le bomberman caractérisé par 'position' est touché. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la position du bomberman dans le labyrinthe
			Valeur de retour:
				<booléen>
				vrai si bomberman touché, faux sinon
		"""
		if (self.grid[position.y][position.x] >= Unit.FLAME_0 and self.grid[position.y][position.x] <= Unit.FLAME_4):
			return True
		for creep in self.creeps:
			if creep.position.y == position.y and creep.position.x == position.x:
				return True
		return False

	def burn(self, position):
		""" Fait bruler les flammes sur le labyrinthe.
			Retourne vrai si le bomberman caractérisé par 'position' est touché. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la position du bomberman dans le labyrinthe
			Valeur de retour:
				<booléen>
				vrai si bomberman touché, faux sinon
		"""
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
		for creep in self.creeps:
			if (self.grid[creep.position.y][creep.position.x] >= Unit.FLAME_0 and self.grid[creep.position.y][creep.position.x] <= Unit.FLAME_4):
				self.creeps.remove(creep)
		return self.bomberman_touched(position)

	def update_creeps_move_index(self):
		""" Met à jour la valeur de l'attribut 'move_index' dand le but de donner aux creeps une impression de marche lors de leurs déplacements.
		"""
		for creep in self.creeps:
			creep.update_move_index()

	def bomberman_on_portal(self, position):
		""" Retourne vrai si le bomberman caractérisé par 'position' se trouve sur le portail de sortie. Retourne faux sinon.
			Paramètres:
				'position':
					<Position>
					la position du bomberman dans le labyrinthe
			Valeur de retour:
				<booléen>
				vrai si bomberman  est sur le portail, faux sinon
		"""
		return self.grid[position.y][position.x] == Unit.PORTAL

	def appear_portal(self, position):
		""" Place un portal sur la position donnée en paramètre
		"""
		self.grid[position.y][position.x] = Unit.PORTAL		

	def check_powerups(self, position):
		""" Retourne un entier caractérisant le bonnus sur lequel le bomberman se trouve.
			Paramètres:
				'position':
					<Position>
					la position du bomberman dans le labyrinthe
			Valeur de retour:
				<entier>
				un entier caractérisant quel bonnus doit être augmenté
		"""
		if self.grid[position.y][position.x] == Unit.BOMB_POWERUP:
			self.grid[position.y][position.x] = Unit.GROUND
			return BOMB_UP
		if self.grid[position.y][position.x] == Unit.FLAME_POWERUP:
			self.grid[position.y][position.x] = Unit.GROUND
			return FLAME_UP

	def print(self, window, size_unit, stage = -1, username = None):
		""" Affiche le labyrinthe dans la fenêtre caractérisé par 'window'.
			Paramètres:
				'window':
					<pygame.Surface>
					la fenetre courante
				'size_unit':
					<nombre>
					la taille en pixel d'une unité de surface
		"""
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] == Unit.GROUND:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BLOCK:
					window.blit(pygame.transform.scale(self.block, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOX:
					window.blit(pygame.transform.scale(self.box, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.PORTAL:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.portal, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.PORTAL_HIDDEN:
						window.blit(pygame.transform.scale(self.box, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOMB_1:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.bomb[0], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOMB_2:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.bomb[1], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOMB_3:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.bomb[2], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_0:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.flame[0], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_1:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.flame[1], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_2:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.flame[2], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_3:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.flame[3], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_4:
					window.blit(pygame.transform.scale(self.ground, (size_unit, size_unit)), (i*size_unit, j*size_unit))
					window.blit(pygame.transform.scale(self.flame[4], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOMB_POWERUP_HIDDEN:
					window.blit(pygame.transform.scale(self.box, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.BOMB_POWERUP:
					window.blit(pygame.transform.scale(self.powerups[0], (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_POWERUP_HIDDEN:
					window.blit(pygame.transform.scale(self.box, (size_unit, size_unit)), (i*size_unit, j*size_unit))
				elif self.grid[j][i] == Unit.FLAME_POWERUP:
					window.blit(pygame.transform.scale(self.powerups[1], (size_unit, size_unit)), (i*size_unit, j*size_unit))
		for creep in self.creeps:
			creep.print(window, size_unit)
		if stage != -1:
			font = pygame.font.Font('freesansbold.ttf', 32)
			text = font.render(username+' | '+'Stage '+str(stage), True, (255, 255, 255))
			textRect = text.get_rect()
			textRect.topleft = (0, 0)
			window.blit(text, textRect)
