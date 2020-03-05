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
		self.bomb = pygame.image.load(BOMB).convert_alpha()
		self.grid = [[Unit.GROUND] * Y_MAX for k in range(X_MAX)]
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if j == Y_MIN or j == Y_MAX-1 or i == X_MIN or i == X_MAX-1 or j % 2 == 0 and i % 2 == 0:
					self.grid[j][i] = Unit.BLOCK
		"""Si j'écris :
		self.creeps = [Creep()]*NUMBER_CREEPS
		Les objets créés pointeront dans la même zone mémoire, ce qui revient à 1 ennemie"""
		self.creeps = []
		for i in range(NUMBER_CREEPS):
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

			#json_grid = record.decode("utf-8") # bizarrement 'record' est de type <byte>, on le decode donc
			json_grid = record

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

	"""Non généré par base de données encore"""
	def generate_ennemies(self):
		"""Générer les CREEPS"""
		positions_occupees = []
		for creep in self.creeps:
			new_position = Position(0,0)
			place_occupee = False

			"""On test si la place est valide, non occupée et pas trop proche du joueur"""
			while self.grid[new_position.y][new_position.x] != Unit.GROUND or new_position.y < BOMBERMAN_INITIAL_POSITION_Y + 5 and new_position.x < BOMBERMAN_INITIAL_POSITION_X + 5  or place_occupee:
				place_occupee = False
				new_position = Position(random.randint(X_MIN+1,X_MAX-2),random.randint(Y_MIN+1,Y_MAX-2))
				"""On vérifie si la place est libre"""
				for place in positions_occupees:
					if ( new_position == place ):
						place_occupee = True
						break
			
			"""On sauvegarde la place comme étant occupée, et on l'attribut à un ennemie """
			positions_occupees.append(new_position)
			creep.position = new_position


	def generate(self):
		"""Générer les BOX"""
		""" Génére un labyrinthe dont les composants seront disposés de manière aléatoire. Certains composants ont cependant une disposition prédéfinie et constante.
		"""
		for j in range(Y_MIN, Y_MAX):
			for i in range(X_MIN, X_MAX):
				if self.grid[j][i] != Unit.BLOCK:
					if j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y+1 and i == BOMBERMAN_INITIAL_POSITION_X or j == BOMBERMAN_INITIAL_POSITION_Y and i == BOMBERMAN_INITIAL_POSITION_X+1:
						continue
					if (random.choice([True, True, False])):
						self.grid[j][i] = Unit.BOX

		"""Générer les CREEPS"""
		positions_occupees = []
		for creep in self.creeps:
			new_position = Position(0,0)
			place_occupee = False

			"""On test si la place est valide, non occupée et pas trop proche du joueur"""
			while self.grid[new_position.y][new_position.x] != Unit.GROUND or new_position.y < BOMBERMAN_INITIAL_POSITION_Y + 5 and new_position.x < BOMBERMAN_INITIAL_POSITION_X + 5  or place_occupee:
				place_occupee = False
				new_position = Position(random.randint(X_MIN+1,X_MAX-2),random.randint(Y_MIN+1,Y_MAX-2))
				"""On vérifie si la place est libre"""
				for place in positions_occupees:
					if ( new_position == place ):
						place_occupee = True
						break
			
			"""On sauvegarde la place comme étant occupée, et on l'attribut à un ennemie """
			positions_occupees.append(new_position)
			creep.position = new_position

		
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
		if direction == Direction.RIGHT:
			if self.grid[position.y][position.x+1] == Unit.GROUND:
				return True
		if direction == Direction.LEFT:
			if self.grid[position.y][position.x-1] == Unit.GROUND:
				return True
		if direction == Direction.UP:
			if self.grid[position.y-1][position.x] == Unit.GROUND:
				return True
		if direction == Direction.DOWN:
			if self.grid[position.y+1][position.x] == Unit.GROUND:
				return True
		return False

	def move_enemies(self):
		#print("ok")
		for creep in self.creeps:
			for i in range(5):
				next_move = random.choice([Direction.UP,Direction.LEFT,Direction.RIGHT,Direction.DOWN])
				if ( next_move == Direction.UP and self.valid_move(creep.position, Direction.UP)):
					creep.turn(Direction.UP)
					creep.move(Direction.UP)
					break
				elif ( next_move == Direction.LEFT and self.valid_move(creep.position, Direction.LEFT)):
					creep.turn(Direction.LEFT)
					creep.move(Direction.LEFT)
					break
				elif ( next_move == Direction.RIGHT and self.valid_move(creep.position, Direction.RIGHT)):
					creep.turn(Direction.RIGHT)
					creep.move(Direction.RIGHT)
					break
				elif ( next_move == Direction.DOWN and self.valid_move(creep.position, Direction.DOWN)):
					creep.turn(Direction.DOWN)
					creep.move(Direction.DOWN)
					break
				

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
		self.grid[position.y][position.x] = Unit.BOMB

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
				elif self.grid[j][i] == Unit.BOMB:
					window.blit(self.ground, (i*SIZE_UNIT, j*SIZE_UNIT))
					window.blit(self.bomb, (i*SIZE_UNIT, j*SIZE_UNIT))

		"""On affiche les ennemies"""	
		for creep in self.creeps:
			creep.print(window)
