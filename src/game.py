#!/usr/bin/python
# -*- coding: utf-8 -*-

from labyrinth import *
from constants import *
from bomberman import *
from direction import *
import pygame

pygame.init()

window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(WINDOW_CAPTION)
pygame.key.set_repeat(400, 30)

stage = 1

labyrinth = Labyrinth()
labyrinth.generate()
# labyrinth.load(stage)
bomberman = Bomberman()

pygame.time.set_timer(pygame.USEREVENT + EVENT_ONE_SECOND, SECOND)

loop = True
while loop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				bomberman.turn(Direction.RIGHT)
				if labyrinth.valid_move(bomberman.position, Direction.RIGHT):
					bomberman.move(Direction.RIGHT)
			elif event.key == pygame.K_LEFT:
				bomberman.turn(Direction.LEFT)
				if labyrinth.valid_move(bomberman.position, Direction.LEFT):
					bomberman.move(Direction.LEFT)
			elif event.key == pygame.K_UP:
				bomberman.turn(Direction.UP)
				if labyrinth.valid_move(bomberman.position, Direction.UP):
					bomberman.move(Direction.UP)
			elif event.key == pygame.K_DOWN:
				bomberman.turn(Direction.DOWN)
				if labyrinth.valid_move(bomberman.position, Direction.DOWN):
					bomberman.move(Direction.DOWN)
			elif event.key == pygame.K_SPACE:
				if labyrinth.can_drop_bomb(bomberman.position) and bomberman.can_drop_bomb():
					bomberman.drop_bomb()
					pygame.time.set_timer(pygame.USEREVENT + EVENT_BOMB_EXPLOSE, 3*SECOND)
					labyrinth.drop_bomb(bomberman.position)
		elif event.type >= pygame.NOEVENT and event.type <= pygame.NUMEVENTS:
			if event.type == pygame.USEREVENT + EVENT_ONE_SECOND:
				labyrinth.move_creeps()
			elif event.type == pygame.USEREVENT + EVENT_BOMB_EXPLOSE:
				labyrinth.bomb_explose()
				bomberman.bomb_explose()

	labyrinth.print(window)
	bomberman.print(window)
	pygame.display.flip()

pygame.quit()
