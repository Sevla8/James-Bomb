#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from constants import *
from labyrinth import *
from bomberman import *
from direction import *

pygame.init()

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAPTION)
pygame.key.set_repeat(400, 30)

labyrinth = Labyrinth()
labyrinth.generate()
bomberman = Bomberman()

loop = True
while loop:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				bomberman.change_position(Direction.RIGHT)
				if labyrinth.valid_move(bomberman.position, Direction.RIGHT):
					bomberman.move(Direction.RIGHT)
			elif event.key == pygame.K_LEFT:
				bomberman.change_position(Direction.LEFT)
				if labyrinth.valid_move(bomberman.position, Direction.LEFT):
					bomberman.move(Direction.LEFT)
			elif event.key == pygame.K_UP:
				bomberman.change_position(Direction.UP)
				if labyrinth.valid_move(bomberman.position, Direction.UP):
					bomberman.move(Direction.UP)
			elif event.key == pygame.K_DOWN:
				bomberman.change_position(Direction.DOWN)
				if labyrinth.valid_move(bomberman.position, Direction.DOWN):
					bomberman.move(Direction.DOWN)
		elif event.type == pygame.QUIT:
			loop = False

	labyrinth.print(window)
	bomberman.print(window)
	pygame.display.flip()

pygame.quit()
