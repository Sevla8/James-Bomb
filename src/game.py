#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from labyrinth import *
from constants import *
from bomberman import *
from direction import *
import pygame
import pygameMenu
import menu

pause_menu = None
window = None
username = None
stage = None

def load_progression(username):
	try:
		db = mysql.connector.connect(host='localhost',
									database='Bomberman',
									user='root',
									password='')
		cursor = db.cursor()
		query = "SELECT stage FROM Adventure WHERE username = %s"
		cursor.execute(query, (username,))
		data = cursor.fetchall()
		if cursor.rowcount == 0:
			stage = 0
		else:
			stage = data[0][0]
		cursor.close()

		return stage

	except mysql.connector.Error as e:
		print("Error while connecting to MySQL", e)

	finally:
		if (db.is_connected()):
			cursor.close()
			db.close()

def new_progression(username, stage):
	try:
		db = mysql.connector.connect(host='localhost',
									database='Bomberman',
									user='root',
									password='')

		cursor = db.cursor()
		query = "INSERT INTO Adventure (username, stage) VALUES (%s, %s)"
		cursor.execute(query, (username, stage))
		db.commit()
		cursor.close()

	except mysql.connector.Error as e:
		print("Error while connecting to MySQL", e)

	finally:
		if (db.is_connected()):
			cursor.close()
			db.close()

def save_progression(username, stage):
	try:
		db = mysql.connector.connect(host='localhost',
									database='Bomberman',
									user='root',
									password='')

		cursor = db.cursor()
		query = "UPDATE Adventure SET stage = %s WHERE username = %s"
		cursor.execute(query, (stage, username))
		db.commit()
		cursor.close()

	except mysql.connector.Error as e:
		print("Error while connecting to MySQL", e)

	finally:
		if (db.is_connected()):
			cursor.close()
			db.close()

def save_and_quit():
	global username
	global stage
	save_progression(username, stage)
	menu.principal_menu()

def pause_background():
	pass

def battle():
	global window
	global pause_menu

	window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
	pygame.display.set_caption(WINDOW_CAPTION)
	pygame.key.set_repeat(1, int(SECOND/3))
	size_unit = DEFAULT_SIZE_UNIT

	labyrinth = Labyrinth()
	labyrinth.generate()
	bomberman = Bomberman()

	pygame.time.set_timer(pygame.USEREVENT + EVENT_MOVE_CREEPS, SECOND)
	pygame.time.set_timer(pygame.USEREVENT + EVENT_BOMB_TIMEOUT, HALF_SECOND)
	pygame.time.set_timer(pygame.USEREVENT + EVENT_FLAME_BURN, TWENTIETH_SECOND)
	event_bomb_explose = [EVENT_BOMB_EXPLOSE_0, EVENT_BOMB_EXPLOSE_1, EVENT_BOMB_EXPLOSE_2, EVENT_BOMB_EXPLOSE_3, EVENT_BOMB_EXPLOSE_4, EVENT_BOMB_EXPLOSE_5, EVENT_BOMB_EXPLOSE_6, EVENT_BOMB_EXPLOSE_7, EVENT_BOMB_EXPLOSE_8, EVENT_BOMB_EXPLOSE_9]
	event_bomb_explose_active = [False] * 10
	current_bomb_index = 0

	# Main menu, pauses execution of the application
	pause_menu = pygameMenu.Menu(window,
								 back_box=False,
								 bgfun=pause_background,
								 enabled=False,
								 font=pygameMenu.font.FONT_BEBAS,
								 font_color=COLOR_BLACK,
								 menu_alpha=90,
								 menu_color=COLOR_BACKGROUND,
								 fps=FPS,
								 onclose=pygameMenu.events.CLOSE,
								 title='Pause Menu',
								 option_shadow=False,
								 title_offsety=5,
								 window_height=WINDOW_SIZE[1],
								 window_width=WINDOW_SIZE[0],
								 mouse_enabled=True,
								 mouse_visible=True)

	pause_menu.add_option('Resume', pygameMenu.events.CLOSE)
	pause_menu.add_option('Quit', menu.principal_menu)

	loop = True
	while loop:
		event = pygame.event.wait()
		# if event.type == pygame.VIDEORESIZE:	# bug
		# 	size_unit = min(int(event.w / 15), int(event.h / 15))
		# 	window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pause_menu.enable()
			elif event.key == pygame.K_RIGHT:
				bomberman.turn(Direction.RIGHT)
				bomberman.update_move_index()
				if labyrinth.valid_move(bomberman.position, Direction.RIGHT):
					bomberman.move(Direction.RIGHT)
					powerups = labyrinth.check_powerups(bomberman.get_position())
					bomberman.skill_up(powerups)
					loop = not labyrinth.bomberman_on_portal(bomberman.get_position())
			elif event.key == pygame.K_LEFT:
				bomberman.turn(Direction.LEFT)
				bomberman.update_move_index()
				if labyrinth.valid_move(bomberman.position, Direction.LEFT):
					bomberman.move(Direction.LEFT)
					powerups = labyrinth.check_powerups(bomberman.get_position())
					bomberman.skill_up(powerups)
					loop = not labyrinth.bomberman_on_portal(bomberman.get_position())
			elif event.key == pygame.K_UP:
				bomberman.turn(Direction.UP)
				bomberman.update_move_index()
				if labyrinth.valid_move(bomberman.position, Direction.UP):
					bomberman.move(Direction.UP)
					powerups = labyrinth.check_powerups(bomberman.get_position())
					bomberman.skill_up(powerups)
					loop = not labyrinth.bomberman_on_portal(bomberman.get_position())
			elif event.key == pygame.K_DOWN:
				bomberman.turn(Direction.DOWN)
				bomberman.update_move_index()
				if labyrinth.valid_move(bomberman.position, Direction.DOWN):
					bomberman.move(Direction.DOWN)
					powerups = labyrinth.check_powerups(bomberman.get_position())
					bomberman.skill_up(powerups)
					loop = not labyrinth.bomberman_on_portal(bomberman.get_position())
			elif event.key == pygame.K_SPACE:
				if labyrinth.can_drop_bomb(bomberman.position) and bomberman.can_drop_bomb():
					bomberman.drop_bomb()
					labyrinth.drop_bomb(bomberman.get_position())
					for k in range(0, MAX_BOMB_AMOUNT):
						if event_bomb_explose_active[k]:
							pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 0)
							pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 3*HALF_SECOND)
					pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[current_bomb_index], 3*HALF_SECOND)
					event_bomb_explose_active[current_bomb_index] = True
					current_bomb_index = (current_bomb_index + 1) % MAX_BOMB_AMOUNT
		elif event.type >= pygame.NOEVENT and event.type <= pygame.NUMEVENTS:
			if event.type == pygame.USEREVENT + EVENT_MOVE_CREEPS:
				labyrinth.move_creeps()
				labyrinth.update_creeps_move_index()
			if event.type == pygame.USEREVENT + EVENT_BOMB_TIMEOUT:
				labyrinth.bomb_explose(bomberman.get_scope())
			if event.type == pygame.USEREVENT + EVENT_FLAME_BURN:
				loop = not labyrinth.burn(bomberman.get_position())
			for k in range(0, MAX_BOMB_AMOUNT):	# bug
				if event.type == pygame.USEREVENT + event_bomb_explose[k]:
					pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 0)
					event_bomb_explose_active[k] = False
					bomberman.bomb_explose()
		labyrinth.print(window, size_unit)
		bomberman.print(window, size_unit)
		pause_menu.mainloop(event, disable_loop=False)
		pygame.display.flip()

def adventure(user_name):
	global window
	global pause_menu
	global username
	global stage

	username = user_name

	window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
	pygame.display.set_caption(WINDOW_CAPTION)
	pygame.key.set_repeat(1, int(SECOND/3))
	size_unit = DEFAULT_SIZE_UNIT

	stage = load_progression(username)
	if stage == 0:
		# afficher cinématique
		stage += 1
		new_progression(username, stage)

	while stage != 2:

		labyrinth = Labyrinth()
		labyrinth.load(stage)
		bomberman = Bomberman()

		pygame.time.set_timer(pygame.USEREVENT + EVENT_MOVE_CREEPS, SECOND)
		pygame.time.set_timer(pygame.USEREVENT + EVENT_BOMB_TIMEOUT, HALF_SECOND)
		pygame.time.set_timer(pygame.USEREVENT + EVENT_FLAME_BURN, TWENTIETH_SECOND)
		event_bomb_explose = [EVENT_BOMB_EXPLOSE_0, EVENT_BOMB_EXPLOSE_1, EVENT_BOMB_EXPLOSE_2, EVENT_BOMB_EXPLOSE_3, EVENT_BOMB_EXPLOSE_4, EVENT_BOMB_EXPLOSE_5, EVENT_BOMB_EXPLOSE_6, EVENT_BOMB_EXPLOSE_7, EVENT_BOMB_EXPLOSE_8, EVENT_BOMB_EXPLOSE_9]
		event_bomb_explose_active = [False] * 10
		current_bomb_index = 0

		# Main menu, pauses execution of the application
		pause_menu = pygameMenu.Menu(window,
									back_box=False,
									bgfun=pause_background,
									enabled=False,
									font=pygameMenu.font.FONT_BEBAS,
									font_color=COLOR_BLACK,
									menu_alpha=90,
									menu_color=COLOR_BACKGROUND,
									fps=FPS,
									onclose=pygameMenu.events.CLOSE,
									title='Pause Menu',
									option_shadow=False,
									title_offsety=5,
									window_height=WINDOW_SIZE[1],
									window_width=WINDOW_SIZE[0],
									mouse_enabled=True,
									mouse_visible=True)

		pause_menu.add_option('Resume', pygameMenu.events.CLOSE)
		pause_menu.add_option('Save & Quit', save_and_quit)

		loop = True
		while loop:
			event = pygame.event.wait()
			# if event.type == pygame.VIDEORESIZE:	# bug
			# 	size_unit = min(int(event.w / 15), int(event.h / 15))
			# 	window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause_menu.enable()
				elif event.key == pygame.K_RIGHT:
					bomberman.turn(Direction.RIGHT)
					bomberman.update_move_index()
					if labyrinth.valid_move(bomberman.position, Direction.RIGHT):
						bomberman.move(Direction.RIGHT)
						powerups = labyrinth.check_powerups(bomberman.get_position())
						bomberman.skill_up(powerups)
						if labyrinth.bomberman_on_portal(bomberman.get_position()):
							loop = False
							stage += 1
							save_progression(username, stage)
				elif event.key == pygame.K_LEFT:
					bomberman.turn(Direction.LEFT)
					bomberman.update_move_index()
					if labyrinth.valid_move(bomberman.position, Direction.LEFT):
						bomberman.move(Direction.LEFT)
						powerups = labyrinth.check_powerups(bomberman.get_position())
						bomberman.skill_up(powerups)
						if labyrinth.bomberman_on_portal(bomberman.get_position()):
							loop = False
							stage += 1
							save_progression(username, stage)
				elif event.key == pygame.K_UP:
					bomberman.turn(Direction.UP)
					bomberman.update_move_index()
					if labyrinth.valid_move(bomberman.position, Direction.UP):
						bomberman.move(Direction.UP)
						powerups = labyrinth.check_powerups(bomberman.get_position())
						bomberman.skill_up(powerups)
						if labyrinth.bomberman_on_portal(bomberman.get_position()):
							loop = False
							stage += 1
							save_progression(username, stage)
				elif event.key == pygame.K_DOWN:
					bomberman.turn(Direction.DOWN)
					bomberman.update_move_index()
					if labyrinth.valid_move(bomberman.position, Direction.DOWN):
						bomberman.move(Direction.DOWN)
						powerups = labyrinth.check_powerups(bomberman.get_position())
						bomberman.skill_up(powerups)
						if labyrinth.bomberman_on_portal(bomberman.get_position()):
							loop = False
							stage += 1
							save_progression(username, stage)
				elif event.key == pygame.K_SPACE:
					if labyrinth.can_drop_bomb(bomberman.position) and bomberman.can_drop_bomb():
						bomberman.drop_bomb()
						labyrinth.drop_bomb(bomberman.get_position())
						for k in range(0, MAX_BOMB_AMOUNT):
							if event_bomb_explose_active[k]:
								pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 0)
								pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 3*HALF_SECOND)
						pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[current_bomb_index], 3*HALF_SECOND)
						event_bomb_explose_active[current_bomb_index] = True
						current_bomb_index = (current_bomb_index + 1) % MAX_BOMB_AMOUNT
			elif event.type >= pygame.NOEVENT and event.type <= pygame.NUMEVENTS:
				if event.type == pygame.USEREVENT + EVENT_MOVE_CREEPS:
					labyrinth.move_creeps()
					labyrinth.update_creeps_move_index()
				if event.type == pygame.USEREVENT + EVENT_BOMB_TIMEOUT:
					labyrinth.bomb_explose(bomberman.get_scope())
				if event.type == pygame.USEREVENT + EVENT_FLAME_BURN:
					loop = not labyrinth.burn(bomberman.get_position())
				for k in range(0, MAX_BOMB_AMOUNT):	# bug
					if event.type == pygame.USEREVENT + event_bomb_explose[k]:
						pygame.time.set_timer(pygame.USEREVENT + event_bomb_explose[k], 0)
						event_bomb_explose_active[k] = False
						bomberman.bomb_explose()
			labyrinth.print(window, size_unit)
			bomberman.print(window, size_unit)
			pause_menu.mainloop(event, disable_loop=False)
			pygame.display.flip()

def multiplayer():
	pass
