import random
import numpy as np
from PIL import Image
import pygame,sys
from pygame.locals import * 
import time

height = 300
width = 500

white = (255, 255, 255)
black = (0, 0, 0)

populationsize = 10
mut = 0.01


def createPopulation(x):
	population = [[[ 0 for k in xrange(populationsize)] for j in xrange(x.shape[1])] for i in xrange(x.shape[0])]

	for i in xrange(x.shape[0]):
		for j in xrange(x.shape[1]):
			for k in xrange(populationsize):
				parent = [random.randint(0,255), random.randint(0,255), random.randint(0,255) ]
				population[i][j][k] = (parent,fitness(parent, x[i][j]))
	return population	

def fitness(a,b):
	ans = 0
	ans+= abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
	return ans 

def sortPoupulation(population, x):
	for i in range(x.shape[0]):
		for j in range(x.shape[1]):
			population[i][j].sort(key = lambda x: x[1])

def makeImage(population, bw):
	ans = np.zeros(bw.shape,dtype = np.uint8)
	for i in range(bw.shape[0]):
		for j in range(bw.shape[1]):
			ans[i][j][0] = np.uint8(population[i][j][0][0][0])
			ans[i][j][1] = np.uint8(population[i][j][0][0][1])
			ans[i][j][2] = np.uint8(population[i][j][0][0][2])
	return ans		

def crossover(a,b):
	c = []
	for i in range(len(a)):
		if random.random()<=0.5:
			c.append(a[i])
		else:
			c.append(b[i])

		if random.random() <= mut:
			c[i] = random.randint(0,255)
	return c		

def selection(city):
	pc = 0.2
	total = 1 - pc
	prob = random.random()
	for i in range(populationsize):
		if prob<=total:
			return city[i][0]
		total = total*pc	
	return city[populationsize-1][0]
		
def geneticAlgo(city, bw):
	population = []
	for i in range(populationsize):
		child = crossover(selection(city),selection(city))
		population.append((child, fitness(child, bw)))
	return population	
		

def solve(name):
	global screen

	img = Image.open(name)	
	x,y = img.size
	width, height = x*2+300,y*2+50
	bw = np.array(img)
	print bw.shape

	pygame.init()
	screen = pygame.display.set_mode((width,height))
	screen.fill((200,200,200))
	
	screen.fill((200,200,200))
	screen.blit(pygame.image.load(name),(30,20))
	pygame.display.update()

	population = createPopulation(bw)
	generation = 0

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		screen.fill((200,200,200))

		generation+=1
		print generation
		best_candidate = makeImage(population, bw)
		new_img = Image.fromarray(best_candidate)
		new_img.save('test.jpg')
		screen.blit(pygame.image.load('test.jpg'),(width/2,20))
		screen.blit(pygame.image.load(name),(30,20))
		showText(generation)
		pygame.display.update()
		time.sleep(0.5)
		for i in range(bw.shape[0]):
			for j in range(bw.shape[1]):
				population[i][j] = geneticAlgo(population[i][j], bw[i][j])

		sortPoupulation(population, bw)		

def showText(score):
	text= 'Content'
	fontObj = pygame.font.Font('freesansbold.ttf', 15)
	textSurfaceObj = fontObj.render(text, True, (0,0,0), (200,200,200))
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (30,10)
	screen.blit(textSurfaceObj, textRectObj)
	text= 'Generations: '+str(score)
	fontObj = pygame.font.Font('freesansbold.ttf', 15)
	textSurfaceObj = fontObj.render(text, True, (0,0,0), (200,200,200))
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (width/2,10)
	screen.blit(textSurfaceObj, textRectObj)


solve('taj.jpg')	
