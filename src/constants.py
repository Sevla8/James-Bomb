#!/usr/bin/python
# -*- coding: utf-8 -*-

DEFAULT_SIZE_UNIT = 40
WINDOW_SIZE = (DEFAULT_SIZE_UNIT*15, DEFAULT_SIZE_UNIT*15)
COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
BOMB_1 = "sprites/Bomb/Bomb_f01.png"
BOMB_2 = "sprites/Bomb/Bomb_f02.png"
BOMB_3 = "sprites/Bomb/Bomb_f03.png"
FLAME_0 = "sprites/Flame/Flame_f00.png"
FLAME_1 = "sprites/Flame/Flame_f01.png"
FLAME_2 = "sprites/Flame/Flame_f02.png"
FLAME_3 = "sprites/Flame/Flame_f03.png"
FLAME_4 = "sprites/Flame/Flame_f04.png"
BOMBERMAN_RIGHT_0 = "sprites/Bomberman/Right/Bman_R_f00.png"
BOMBERMAN_RIGHT_1 = "sprites/Bomberman/Right/Bman_R_f01.png"
BOMBERMAN_RIGHT_2 = "sprites/Bomberman/Right/Bman_R_f02.png"
BOMBERMAN_RIGHT_3 = "sprites/Bomberman/Right/Bman_R_f03.png"
BOMBERMAN_RIGHT_4 = "sprites/Bomberman/Right/Bman_R_f04.png"
BOMBERMAN_RIGHT_5 = "sprites/Bomberman/Right/Bman_R_f05.png"
BOMBERMAN_RIGHT_6 = "sprites/Bomberman/Right/Bman_R_f06.png"
BOMBERMAN_RIGHT_7 = "sprites/Bomberman/Right/Bman_R_f07.png"
BOMBERMAN_LEFT_0 = "sprites/Bomberman/Left/Bman_L_f00.png"
BOMBERMAN_LEFT_1 = "sprites/Bomberman/Left/Bman_L_f01.png"
BOMBERMAN_LEFT_2 = "sprites/Bomberman/Left/Bman_L_f02.png"
BOMBERMAN_LEFT_3 = "sprites/Bomberman/Left/Bman_L_f03.png"
BOMBERMAN_LEFT_4 = "sprites/Bomberman/Left/Bman_L_f04.png"
BOMBERMAN_LEFT_5 = "sprites/Bomberman/Left/Bman_L_f05.png"
BOMBERMAN_LEFT_6 = "sprites/Bomberman/Left/Bman_L_f06.png"
BOMBERMAN_LEFT_7 = "sprites/Bomberman/Left/Bman_L_f07.png"
BOMBERMAN_FRONT_0 = "sprites/Bomberman/Front/Bman_F_f00.png"
BOMBERMAN_FRONT_1 = "sprites/Bomberman/Front/Bman_F_f01.png"
BOMBERMAN_FRONT_2 = "sprites/Bomberman/Front/Bman_F_f02.png"
BOMBERMAN_FRONT_3 = "sprites/Bomberman/Front/Bman_F_f03.png"
BOMBERMAN_FRONT_4 = "sprites/Bomberman/Front/Bman_F_f04.png"
BOMBERMAN_FRONT_5 = "sprites/Bomberman/Front/Bman_F_f05.png"
BOMBERMAN_FRONT_6 = "sprites/Bomberman/Front/Bman_F_f06.png"
BOMBERMAN_FRONT_7 = "sprites/Bomberman/Front/Bman_F_f07.png"
BOMBERMAN_BACK_0 = "sprites/Bomberman/Back/Bman_B_f00.png"
BOMBERMAN_BACK_1 = "sprites/Bomberman/Back/Bman_B_f01.png"
BOMBERMAN_BACK_2 = "sprites/Bomberman/Back/Bman_B_f02.png"
BOMBERMAN_BACK_3 = "sprites/Bomberman/Back/Bman_B_f03.png"
BOMBERMAN_BACK_4 = "sprites/Bomberman/Back/Bman_B_f04.png"
BOMBERMAN_BACK_5 = "sprites/Bomberman/Back/Bman_B_f05.png"
BOMBERMAN_BACK_6 = "sprites/Bomberman/Back/Bman_B_f06.png"
BOMBERMAN_BACK_7 = "sprites/Bomberman/Back/Bman_B_f07.png"
BOMBERMAN_MOVE_MAX = 8
CREEP_RIGHT_0 = "sprites/Creep/Right/Creep_R_f00.png"
CREEP_RIGHT_1 = "sprites/Creep/Right/Creep_R_f01.png"
CREEP_RIGHT_2 = "sprites/Creep/Right/Creep_R_f02.png"
CREEP_RIGHT_3 = "sprites/Creep/Right/Creep_R_f03.png"
CREEP_RIGHT_4 = "sprites/Creep/Right/Creep_R_f04.png"
CREEP_RIGHT_5 = "sprites/Creep/Right/Creep_R_f05.png"
CREEP_LEFT_0 = "sprites/Creep/Left/Creep_L_f00.png"
CREEP_LEFT_1 = "sprites/Creep/Left/Creep_L_f01.png"
CREEP_LEFT_2 = "sprites/Creep/Left/Creep_L_f02.png"
CREEP_LEFT_3 = "sprites/Creep/Left/Creep_L_f03.png"
CREEP_LEFT_4 = "sprites/Creep/Left/Creep_L_f04.png"
CREEP_LEFT_5 = "sprites/Creep/Left/Creep_L_f05.png"
CREEP_FRONT_0 = "sprites/Creep/Front/Creep_F_f00.png"
CREEP_FRONT_1 = "sprites/Creep/Front/Creep_F_f01.png"
CREEP_FRONT_2 = "sprites/Creep/Front/Creep_F_f02.png"
CREEP_FRONT_3 = "sprites/Creep/Front/Creep_F_f03.png"
CREEP_FRONT_4 = "sprites/Creep/Front/Creep_F_f04.png"
CREEP_FRONT_5 = "sprites/Creep/Front/Creep_F_f05.png"
CREEP_BACK_0 = "sprites/Creep/Back/Creep_B_f00.png"
CREEP_BACK_1 = "sprites/Creep/Back/Creep_B_f01.png"
CREEP_BACK_2 = "sprites/Creep/Back/Creep_B_f02.png"
CREEP_BACK_3 = "sprites/Creep/Back/Creep_B_f03.png"
CREEP_BACK_4 = "sprites/Creep/Back/Creep_B_f04.png"
CREEP_BACK_5 = "sprites/Creep/Back/Creep_B_f05.png"
CREEP_MOVE_MAX = 5
UNIT_GROUND = "sprites/Blocks/BackgroundTile.png"
UNIT_BLOCK = "sprites/Blocks/SolidBlock.png"
UNIT_BOX = "sprites/Blocks/ExplodableBlock.png"
UNIT_PORTAL = "sprites/Blocks/Portal.png"
BOMB_POWERUP = "sprites/Powerups/BombPowerup.png"
FLAME_POWERUP = "sprites/Powerups/FlamePowerup.png"
X_MIN = 0
X_MAX = 15
Y_MIN = 0
Y_MAX = 15
BOMBERMAN_INITIAL_POSITION_X = 1
BOMBERMAN_INITIAL_POSITION_Y = 1
WINDOW_CAPTION = "James Bomb"
DEFAULT_HP_BOMBERMAN = 3
DEFAULT_XP_BOMBERMAN = 0
DEFAULT_HP_CREEP = 1
DEFAULT_XP_CREEP = 0
DEFAULT_BOMB_AMOUNT = 1
DEFAULT_BOMB_SCOPE = 1
MAX_BOMB_AMOUNT = 10
DEFAULT_CREEP_AMOUNT = 3
SECOND = 1000
HALF_SECOND = 500
TWENTIETH_SECOND = 50
EVENT_MOVE_CREEPS = 0
EVENT_BOMB_TIMEOUT = 1
EVENT_FLAME_BURN = 2
EVENT_BOMB_EXPLOSE_0 = -1
EVENT_BOMB_EXPLOSE_1 = -2
EVENT_BOMB_EXPLOSE_2 = -3
EVENT_BOMB_EXPLOSE_3 = -4
EVENT_BOMB_EXPLOSE_4 = -5
EVENT_BOMB_EXPLOSE_5 = -6
EVENT_BOMB_EXPLOSE_6 = -7
EVENT_BOMB_EXPLOSE_7 = -8
EVENT_BOMB_EXPLOSE_8 = -9
EVENT_BOMB_EXPLOSE_9 = -10
BOMB_UP = 1
FLAME_UP = 2
BATTLE_MODE = 1
ADVENTURE_MODE= 2
MULTIPLAYER_MODE = 3
EASY = 1
MEDIUM = 2
HARD = 3
MAXIMAL_BOMB_AMOUNT = 10
MAXIMAL_FLAME_SCOPE = 10
