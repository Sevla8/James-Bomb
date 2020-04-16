#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from random import randrange
import pygame
import pygameMenu
import game
import multigame
from constants import *

clock = None
main_menu = None
surface = None

difficulty = MEDIUM

def main_background():
	global surface
	surface.fill(COLOR_BACKGROUND)

def change_difficulty(value, difficulty_level):
	global difficulty
	difficulty = difficulty_level

def principal_menu() :
	global clock
	global main_menu
	global surface

	pygame.init()
	#os.environ['SDL_VIDEO_CENTERED'] = '1'

	surface = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption('James Bomb')
	clock = pygame.time.Clock()

	play_menu = pygameMenu.Menu(surface,
								back_box=False,
								bgfun=main_background,
								color_selected=COLOR_WHITE,
								font=pygameMenu.font.FONT_BEBAS,
								font_color=COLOR_BLACK,
								font_size=30,
								font_size_title=40,
								menu_alpha=100,
								menu_color=COLOR_BACKGROUND,
								menu_color_title=COLOR_BACKGROUND,
								menu_height=int(WINDOW_SIZE[1] * 0.7),
								menu_width=int(WINDOW_SIZE[0] * 0.7),
								onclose=pygameMenu.events.DISABLE_CLOSE,
								option_shadow=False,
								title='Play Menu',
								window_height=WINDOW_SIZE[1],
								window_width=WINDOW_SIZE[0],
								mouse_enabled=True,
								mouse_visible=True,
								# title_offsetx=50
								)

	play_menu.add_option('Battle', game.battle)
	play_menu.add_option('Adventure', game.adventure)
	play_menu.add_option('Multiplayer', game.multiplayer)
	play_menu.add_button('Back', pygameMenu.events.BACK)

	option_menu = pygameMenu.Menu(surface,
								  back_box=False,
								  bgfun=main_background,
								  color_selected=COLOR_WHITE,
								  font=pygameMenu.font.FONT_BEBAS,
								  font_color=COLOR_BLACK,
								  font_size=30,
								  font_size_title=40,
								  menu_alpha=100,
								  menu_color=COLOR_BACKGROUND,
								  menu_color_title=COLOR_BACKGROUND,
								  menu_height=int(WINDOW_SIZE[1] * 0.7),
								  menu_width=int(WINDOW_SIZE[0] * 0.7),
								  onclose=pygameMenu.events.DISABLE_CLOSE,
								  option_shadow=False,
								  title='Option Menu',
								  window_height=WINDOW_SIZE[1],
								  window_width=WINDOW_SIZE[0],
								  mouse_enabled=True,
								  mouse_visible=True,
								  # title_offsetx=50
								  )

	option_menu.add_selector('Select       difficulty       ',
							 [('Easy', EASY), ('Medium', MEDIUM), ('Hard', HARD)],
							 onchange=change_difficulty,
							 selector_id='select_difficulty')
	option_menu.add_button('Back', pygameMenu.events.BACK)

	help_menu = pygameMenu.TextMenu(surface,
								back_box=False,
								bgfun=main_background,
								color_selected=COLOR_WHITE,
								font=pygameMenu.font.FONT_BEBAS,
								font_color=COLOR_BLACK,
								font_size=30,
								menu_alpha=100,
								menu_color=COLOR_BACKGROUND,
								menu_color_title=COLOR_BACKGROUND,
								menu_height=int(WINDOW_SIZE[1] * 0.7),
								menu_width=int(WINDOW_SIZE[0] * 0.7),
								onclose=pygameMenu.events.DISABLE_CLOSE,
								option_shadow=False,
								title='Help Menu',
								window_height=WINDOW_SIZE[1],
								window_width=WINDOW_SIZE[0],
								mouse_enabled=True,
								mouse_visible=True,
								# title_offsetx=50
								)

	help_menu.add_line('Rightwards       Arrow       :       Move       Right')
	help_menu.add_line('Leftwards       Arrow       :       Move       Left')
	help_menu.add_line('Upwards       Arrow       :       Move       Up')
	help_menu.add_line('Downwards       Arrow       :       Move       Down')
	help_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
	help_menu.add_line('Space       :       Drop       Bomb')
	help_menu.add_line('Escape       :       Pause       Menu')
	help_menu.add_button('Back', pygameMenu.events.BACK)

	main_menu = pygameMenu.Menu(surface,
								back_box=False,
								bgfun=main_background,
								color_selected=COLOR_WHITE,
								draw_region_x=80,
								font=pygameMenu.font.FONT_BEBAS,
								font_color=COLOR_BLACK,
								font_size=30,
								menu_alpha=100,
								menu_color=COLOR_BACKGROUND,
								menu_color_title=COLOR_BACKGROUND,
								menu_height=int(WINDOW_SIZE[1] * 0.6),
								menu_width=int(WINDOW_SIZE[0] * 0.6),
								onclose=pygameMenu.events.DISABLE_CLOSE,
								# option_margin=25,
								option_shadow=False,
								title='Main Menu',
								window_height=WINDOW_SIZE[1],
								window_width=WINDOW_SIZE[0],
								mouse_enabled=True,
								mouse_visible=True,
								# title_offsetx=130,
								# title_offsety=-50
								)

	main_menu.add_option('Play', play_menu)
	main_menu.add_option('Option', option_menu)
	main_menu.add_option('Help', help_menu)
	main_menu.add_option('Quit', pygameMenu.events.EXIT)

	main_menu.set_fps(FPS)

	while True:

		clock.tick(FPS)
		main_background()

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT :
				exit()

		main_menu.mainloop(events, disable_loop=False)

		pygame.display.flip()
