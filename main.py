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

clock = pygame.time.Clock()

blockSize = 20
FPS = 15

font = pygame.font.SysFont(None, 25)

def snake(blockSize, snakelist):
	for XnY in snakelist:
		pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],blockSize,blockSize])

def messagetoscreen(msg,colour):
	screenText = font.render(msg, True, colour)
	gameDisplay.blit(screenText, [displayWidth/2, displayHeight/2])

def gameloop():
	gameExit = False
	gameOver = False
	
	lead_x = displayWidth/2
	lead_y = displayHeight/2
	
	lead_x_change = 0
	lead_y_change = 0

	snakeList = []
	snakeLength = 1
	appleThickness = 30

	randAppleX = round(random.randrange(0,displayWidth-blockSize)/10)*10
	randAppleY = round(random.randrange(0,displayHeight-blockSize)/10)*10
	
	while not gameExit:

		while gameOver == True:
			gameDisplay.fill(white)
			messagetoscreen("Game over, press C to play again or Q to quit", red)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
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
				elif event.key == pygame.K_RIGHT:
					lead_y_change = 0
					lead_x_change = blockSize
				elif event.key == pygame.K_UP:
					lead_x_change = 0
					lead_y_change = -blockSize
				elif event.key == pygame.K_DOWN:
					lead_x_change = 0
					lead_y_change = blockSize
			
		lead_x += lead_x_change
		lead_y += lead_y_change
	
		if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
			gameOver = True
	
		gameDisplay.fill(white)
		
		pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleThickness, appleThickness])

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
		
		pygame.display.update()

		if lead_x in range(randAppleX,randAppleX+appleThickness) and lead_y in range(randAppleY,randAppleY+appleThickness):
			randAppleX = round(random.randrange(0,displayWidth-blockSize)/10)*10
			randAppleY = round(random.randrange(0,displayHeight-blockSize)/10)*10
			snakeLength += 1
		

		clock.tick(FPS)

gameloop()

pygame.quit()
quit()