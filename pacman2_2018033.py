#pacman2_2018033.py
#Date: 15-11-2018

#Name: DUSHYANT PANCHAL
#Roll No.: 2018033
#Section: A    Group: 1


import pygame
from pygame.locals import *
from numpy import loadtxt
import time

from random import randint

#Constants for the game
WIDTH, HEIGHT = (32, 32)
ENEMY_COLOR = pygame.Color(255, 0, 0, 255) #RED
#WALL_COLOR = pygame.Color(0, 0, 255, 255) 	# BLUE
#PACMAN_COLOR = pygame.Color(255, 0, 0, 255) # RED
#COIN_COLOR = pygame.Color(255, 255, 0, 255) # YELLOW
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
STOP = (0,0)

player=[pygame.image.load('pacU.png'),pygame.image.load('pacD.png'),pygame.image.load('pacL.png'),pygame.image.load('pacR.png'),pygame.image.load('pacR.png')]
#Player graphics for different directions
coin=pygame.image.load('coin.png')
#Coin graphics
wallimg=pygame.image.load('wall.png')
#Wall graphics

#Functions for displaying text
def text_objects(text,font,col):
	textSurface=font.render(text, True, col)
	return textSurface, textSurface.get_rect()

def message(text,loc,col,size):
	largeText = pygame.font.Font('freesansbold.ttf',size)
	TextSurf, TextRect = text_objects(text, largeText, col)
	TextRect.center = ((loc[0]),(loc[1]))
	screen.blit(TextSurf, TextRect)

	pygame.display.update()
	time.sleep(0.01)

#Displays game over, score and time when user collects all coins
def won(dur,score):
	message("GAME OVER",(320,320),(0,255,0),50)
	message("Your Time: "+str(dur)+"s",(320,400),(255,0,0),20)
	message("Your Score: "+str(score),(320,460),(0,0,255),20)
	message("Exiting in 5 seconds",(320,600),(255,255,255),15)
	time.sleep(5)
	exit()

#Draws a rectangle for the enemy
def draw_enemy(screen,pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, ENEMY_COLOR, [pixels, (WIDTH, HEIGHT)])

#Displays graphic for the wall
def draw_wall(screen, pos):
	screen.blit(wallimg,(WIDTH*pos[0],HEIGHT*pos[1]))
	#pixels = pixels_from_points(pos)
	#pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

#Displays graphic for the player
def draw_pacman(screen, pos, direc):
	screen.blit(player[direc],(WIDTH*pos[0],HEIGHT*pos[1]))
	#pixels = pixels_from_points(pos)
	#pygame.draw.rect(screen, PACMAN_COLOR, [pixels, (WIDTH, HEIGHT)])

#Displays graphic for the coin
def draw_coin(screen, pos):
	#pixels = pixels_from_points(pos)
	#pygame.draw.rect(screen, COIN_COLOR, [pixels, (WIDTH, HEIGHT)])
	screen.blit(coin,(WIDTH*pos[0],HEIGHT*pos[1]))

#Utility functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)


#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((640,640), 0, 32)
pygame.display.set_caption('PACMAN LEVEL 2')	#Game Window Title
background = pygame.surface.Surface((640,640)).convert()


#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (1,1)
background.fill((0,0,0))

move_direction = STOP
score=0	#To store the score

pose=[(1,18),(18,18),(18,1)]	#Initial positions of the enemies
ne=3	#No. of enemies

#print(pose)


#Main game loop 
while True:

	dur=pygame.time.get_ticks()/1000 #Get duration from start

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:	#Takes input from the user to update pacman moving direction.
			if event.key == pygame.K_LEFT:
				move_direction = LEFT
			elif event.key == pygame.K_RIGHT:
				move_direction = RIGHT
			elif event.key == pygame.K_UP:
				move_direction = TOP
			elif event.key == pygame.K_DOWN:
				move_direction = DOWN

	screen.blit(background, (0,0))

	directions=[TOP,DOWN,LEFT,RIGHT,STOP]

	k=add_to_pos(pacman_position, move_direction)

	for i in range(ne):
		ke=add_to_pos(pose[i],directions[randint(0,3)])
		if(layout[ke[1]][ke[0]] in '.c'):
			pose[i]=ke


	#Draw board from the 2d layout array.
 	#In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins
	for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)
			if value == 'w':
				draw_wall(screen, pos)
			elif value == 'c':
				draw_coin(screen, pos)
				if pacman_position == pos:	#Check if player ate any coin
					layout[row][col]='.'	#if so, remove coin from the screen
					score+=1
	

	for i in range(ne):	#If player collides with an enemy
		if pacman_position == pose[i]:
			score-=1

	

	if 'c' not in layout: #If all coins gone
		screen.blit(background, (0,0))
		won(dur,score)	#Player won
	else:
		dur=pygame.time.get_ticks()/1000 #Get duration from start
		draw_pacman(screen, pacman_position,directions.index(move_direction))	#Draw the player
		message("Score: "+str(score),(50,10),(255,0,0),20)	#Display current score
		message("Time: "+str(dur),(580,10),(255,0,0),20)	#Display time from start in seconds



	if(layout[k[1]][k[0]] in '.c'): #Ensure player is in empty space.
		pacman_position = k 	#Update player position based on movement.

	for i in range(ne):		#Draw the enemies
		draw_enemy(screen,pose[i])
	

	#Update the display
	pygame.display.update()

	#print(pacman_position)

	#Wait for a while, computers are very fast.
	time.sleep(0.27)