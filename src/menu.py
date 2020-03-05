import sys
import os
from random import randrange
import pygame
import pygameMenu
import game
from constants import *

clock = None
main_menu = None
surface = None

def main_background():
	global surface
	surface.fill(COLOR_BACKGROUND)

def principal_menu() :
	global clock
	global main_menu
	global surface

	pygame.init()
	#os.environ['SDL_VIDEO_CENTERED'] = '1'

	surface = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption('James Bomb')
	clock = pygame.time.Clock()

	adventure_option = pygameMenu.Menu(surface,
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
										title='Option	 d\'aventure',
										window_height=WINDOW_SIZE[1],
										window_width=WINDOW_SIZE[0],
										mouse_enabled=True,
										mouse_visible=True,
										title_offsetx=50
										)

	adventure_option.add_option('Play', game.adventure)
	adventure_option.add_option('Back', pygameMenu.events.BACK)

	play_adventure_menu = pygameMenu.Menu(surface,
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
											title='Mode Aventure',
											window_height=WINDOW_SIZE[1],
											window_width=WINDOW_SIZE[0],
											mouse_enabled=True,
											mouse_visible=True,
											title_offsetx=50
											)

	play_adventure_menu.add_option('1 Player', adventure_option)
	play_adventure_menu.add_option('2 Player', adventure_option)
	play_adventure_menu.add_option('Back', pygameMenu.events.BACK)

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
								option_margin=25,
								option_shadow=False,
								title='Menu Principal',
								window_height=WINDOW_SIZE[1],
								window_width=WINDOW_SIZE[0],
								mouse_enabled=True,
								mouse_visible=True,
								title_offsetx=130,
								title_offsety=-50
								)

	main_menu.add_option('Play Local', play_adventure_menu)
	main_menu.add_option('Option', play_adventure_menu)
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
