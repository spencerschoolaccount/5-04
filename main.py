import pygame
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

displayWidth = 800
displayHeight = 600

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Slither')

icon = pygame.image.load('snakehead.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snakehead.png')
img2 = pygame.image.load('snaketail.png')
appleSprite = pygame.image.load('apple.png')

clock = pygame.time.Clock()

blockSize = 20
FPS = 15

direction = 'right'

smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)


font = pygame.font.SysFont(None, 25)

def pause():

	paused = True

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
		gameDisplay.fill(white)
		messagetoscreen("Paused", black, -25, 'large')
		messagetoscreen("press C to continue or Q to quit", black, 25,'small')

		pygame.display.update()
		clock.tick(8)

def score(score):
	text = smallfont.render("Score: " + str(score), True, black)
	gameDisplay.blit(text, [0,0])

def randApple():
	randAppleX = round(random.randrange(0,displayWidth-blockSize)/20)*20
	randAppleY = round(random.randrange(0,displayHeight-blockSize)/20)*20
	return randAppleX, randAppleY

def gameintro():

	intro = True

	while intro:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
		
		gameDisplay.fill(white)
		messagetoscreen("Welcome to Slither",
					   green,
					   -100,
					   'large')
		messagetoscreen('The objective of the game is to eat red apples', black, -30)
		messagetoscreen('The more apples you eat the longer you get', black)
		messagetoscreen('If you run into yourself or the edges, you die', black, 30)
		messagetoscreen('Press C to play, press Q to quit', green, 90)

		pygame.display.update()
		clock.tick(8)

def snake(blockSize, snakelist):

	if direction == 'right':
		head = pygame.transform.rotate(img, 270)
	elif direction == 'left':
		head = pygame.transform.rotate(img, 90)
	elif direction == 'up':
		head = img
	elif direction == 'down':
		head = pygame.transform.rotate(img, 180)

	if len(snakelist) >= 2:
		if snakelist[1][0] > snakelist[0][0]:
			tail = pygame.transform.rotate(img2, 270)
		elif snakelist[1][0] < snakelist[0][0]:
			tail = pygame.transform.rotate(img2, 90)
		elif snakelist[1][1] > snakelist[0][1]:
			tail = pygame.transform.rotate(img2, 180)
		elif snakelist[1][1] < snakelist[0][1]:
			tail = img2
		

	gameDisplay.blit(head, (snakelist[-1][0], (snakelist[-1][1])))
	if len(snakelist) >= 2:
		gameDisplay.blit(tail, (snakelist[0][0], (snakelist[0][1])))
	
	for XnY in snakelist[1:-1]:
		pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],blockSize,blockSize])

def textobjects(text,colour,size):
	if size == 'small':
		textSurface = smallfont.render(text, True, colour)
	elif size == 'medium':
		textSurface = medfont.render(text, True, colour)
	elif size == 'large':
		textSurface = largefont.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def messagetoscreen(msg,colour, yDisplace=0, size = "small"):
	textSurf, textRect = textobjects(msg, colour, size)
	textRect.center = (displayWidth / 2), (displayHeight / 2)+yDisplace
	gameDisplay.blit(textSurf,textRect)

def gameloop():
	global direction
	gameExit = False
	gameOver = False
	
	lead_x = displayWidth/2
	lead_y = displayHeight/2
	
	lead_x_change = 0
	lead_y_change = 0

	snakeList = []
	snakeLength = 1
	appleThickness = 20

	randAppleX, randAppleY = randApple()
	
	while not gameExit:

		while gameOver == True:
			gameDisplay.fill(white)
			messagetoscreen("Game Over", red, -25, 'large')
			messagetoscreen("press C to play again or Q to quit", black, 25,'small')
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameloop()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					lead_y_change = 0
					lead_x_change = -blockSize
					direction = 'left'
				elif event.key == pygame.K_RIGHT:
					lead_y_change = 0
					lead_x_change = blockSize
					direction = 'right'
				elif event.key == pygame.K_UP:
					lead_x_change = 0
					lead_y_change = -blockSize
					direction = 'up'
				elif event.key == pygame.K_DOWN:
					lead_x_change = 0
					lead_y_change = blockSize
					direction = 'down'
				elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
					pause()
			
		lead_x += lead_x_change
		lead_y += lead_y_change
	
		if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
			gameOver = True
	
		gameDisplay.fill(white)
	
		gameDisplay.blit(appleSprite, (randAppleX, randAppleY))
		
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)

		if len(snakeList) > snakeLength:
			del snakeList[0]

		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True
		
		snake(blockSize, snakeList)

		score(snakeLength-1)
		
		pygame.display.update()
		
		if (lead_x in range(randAppleX,randAppleX+appleThickness) or (lead_x + blockSize-1) in range(randAppleX,randAppleX+appleThickness)) and (lead_y in range(randAppleY,randAppleY+appleThickness) or (lead_y + blockSize-1) in range(randAppleY,randAppleY+appleThickness)):
			randAppleX, randAppleY = randApple()
			snakeLength += 1
		
		clock.tick(FPS)
gameintro()
gameloop()

pygame.quit()
quit()