import sys
import random
import numpy
import pygame
import copy
import math

class cell(object): 
	def __init__(self, x, y, f=0, g=0, h=0, parentX=0, parentY=0):
		self.x = x
		self.y = y

def generateGrid(rows, cols):
	#grid = [[0 for x in range(cols)] for x in range(rows)]
	grid = numpy.zeros((rows,cols))
	#h = [[0 for x in range(cols)] for x in range(rows)]
	
	return grid

def generateObstacles(grid):
	blockLength = int(min(int(len(grid)/2), int(len(grid[1])/2)))
	blockDirection = random.randint(0,1)
	rand_x = random.randint(1, rows-blockLength)
	rand_y = random.randint(1, cols-blockLength)
	
	for i in range(blockLength):
		grid[rand_x+i][rand_y] = 1 #random wall
		grid[8+i][6] = 1 #sationary wall

#yields a tuple with (x,y) of newCell
def valid_Neigbors(currCell, rows, cols): 
	for checkRow in [-1,0,1]: 
		for checkCol in [-1,0,1]: 
			newCell = (currCell.x + checkRow, currCell.y + checkCol)
			if newCell[0] >= 0 and newCell[0] < rows and newCell[1] >= 0 and newCell[1] < cols and (newCell != (currCell.x, currCell.y)):
				yield newCell 

#check if incoming cell is a wall
def is_Wall(nextCell):
	if grid[nextCell[0], nextCell[1]] == 1:
		return True
	else:
		return False

#return index of cell in openList with minimum value
def searchMinF(openList, F):
	minimumF = F [openList[0][0]] [openList[0][1]]
	for x in range(len(openList)): 
		if F [openList[x][0]] [openList[x][1]] <= minimumF:
			minimumF = F [openList[x][0]] [openList[x][1]]
			minimumIndex = x
	return minimumIndex

def A_star(currentPoint, goalPoint, comparisonList, openList, closedList, F, G, H, parent):
	
	minimumF = 1.0
	nextDestination = [currentPoint.x, currentPoint.y]
	
	#find the lowest F in comparison list, add new cells to openList, evaluate old cells for new parent
	for n in range(len(comparisonList)):
		cellToEval = comparisonList[n] 
		i = cellToEval[0]
		j = cellToEval[1]

		H[i][j] = abs(cellToEval[0] - goalPoint.x) + abs(cellToEval[1]-goalPoint.y)
		G[i][j] = G[currentPoint.x][currentPoint.y] + int(math.sqrt((currentPoint.x - i)**2 + (currentPoint.y - j)**2))
		F[i][j] = H[i][j] + G[i][j]
		
		if n == 0:
			minimumF = F[i][j]

		if F[i][j] <= minimumF:
			minimumF = F[i][j]
			nextDestination =  [i,j]

		if [i,j] not in closedList and [i,j] not in openList:
			openList.append([i,j])
			parent[i][j] = [currentPoint.x, currentPoint.y]		

		else: #if adjacent cell is previously explored, check if new path is better
			if n == 0:
				minimumF = F[i][j]
			if (G[currentPoint.x][currentPoint.y] + int(math.sqrt((currentPoint.x - i)**2 + (currentPoint.y - j)**2))) < G[i][j]:  
				
				parent[i][j] = [currentPoint.x, currentPoint.y]

				H[i][j] = abs(cellToEval[0] - goalPoint.x) + abs(cellToEval[1]-goalPoint.y)
				G[i][j] = G[currentPoint.x][currentPoint.y] + int(math.sqrt((currentPoint.x - i)**2 + (currentPoint.y - j)**2))
				F[i][j] = H[i][j] + G[i][j]
			else: 
				pass

	n = searchMinF(openList, F)
	currentPoint.x, currentPoint.y = openList[n][0], openList[n][1]
	openList.remove([currentPoint.x,currentPoint.y])
	closedList.append([currentPoint.x,currentPoint.y])			

#Resolve path from goal to startpoint
def resolvePath(currentPoint,startPoint, parent, path):
	currentPoint.x, currentPoint.y = goalPoint.x, goalPoint.y 
	while [startPoint.x, startPoint.y] not in path:
		tracer = [parent[currentPoint.x][currentPoint.y][0], parent[currentPoint.x][currentPoint.y][1]] #x, y of parent cell
		path.append(tracer)
		currentPoint.x, currentPoint.y = tracer[0], tracer[1]


#----------Main Program-----------
rows = 15
cols = 25
startPoint = cell(13,0)
goalPoint = cell(rows-1,cols-1)
obstacles = 3

currentPoint = copy.copy(startPoint)
grid = generateGrid(rows, cols)

for x in range(obstacles): 
	generateObstacles(grid)
	

F = [[0 for x in range(cols)] for x in range(rows)]
G = [[0 for x in range(cols)] for x in range(rows)]
H = [[0 for x in range(cols)] for x in range(rows)]

openList = [[currentPoint.x, currentPoint.y]]
closedList = []
comparisonList = []
parent = [[0 for x in range(cols)] for x in range(rows)]

#----------Start Exploring--------
while [goalPoint.x, goalPoint.y] not in closedList:

	
	
	# print "current: (%d, %d) G%d H%d F%d" % (currentPoint.x ,currentPoint.y, 
	# 										G[currentPoint.x][currentPoint.y],
	# 										H[currentPoint.x][currentPoint.y],
	# 										F[currentPoint.x][currentPoint.y])

	#start checking surrounding cells
	for nextCell in valid_Neigbors(currentPoint, rows, cols): #pass in only non-border cells
		if not is_Wall(nextCell): #if the cell is not a wall
			comparisonList.append(nextCell)

	A_star(currentPoint, goalPoint, comparisonList, openList, closedList, F, G, H, parent)

	#reset lists
	comparisonList = []

	#stop if there is no path to goal
	if len(openList) == 0:
		print ("No path to goal.")
		break

#-----------Decide final path to goal------------
path = []
resolvePath(currentPoint,startPoint, parent, path)

# -------- Draw Results -----------
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 25
HEIGHT = 25
 
# This sets the margin between each cell
MARGIN = 5

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [cols*(HEIGHT+MARGIN)+2*MARGIN, rows*(WIDTH+MARGIN)+2*MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()

while not done:
    # for event in pygame.event.get():  # User did something
    #     if event.type == pygame.QUIT:  # If user clicked close
    #         done = True  # Flag that we are done so we exit this loop
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         # User clicks the mouse. Get the position
    #         pos = pygame.mouse.get_pos()
    #         # Change the x/y screen coordinates to grid coordinates
    #         column = pos[0] // (WIDTH + MARGIN)
    #         row = pos[1] // (HEIGHT + MARGIN)
    #         # Set that location to zero
    #         grid[row][column] = 1
    #         print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for i in range(rows):
        for j in range(cols):
            color = WHITE
            if grid[i][j] == 1:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * j + MARGIN,
                              (MARGIN + HEIGHT) * i + MARGIN,
                              WIDTH,
                              HEIGHT])

	
	
    #draw closeList
 	for n in closedList: 
 		pygame.draw.rect(screen, ORANGE, [(MARGIN + WIDTH) * n[1]+ MARGIN, (MARGIN + HEIGHT) * n[0] + MARGIN, WIDTH, HEIGHT])
	
 	#draw path
 	for n in path: 
 		pygame.draw.rect(screen, (i, 127, 127), [(MARGIN + WIDTH) * n[1]+ MARGIN, (MARGIN + HEIGHT) * n[0] + MARGIN, WIDTH, HEIGHT])
	

	#Draw path
 	j = 0
 	colorIncrement = float(200/len(closedList))
 	prev = ((MARGIN + WIDTH) * 5 + MARGIN, (MARGIN + HEIGHT) * 5 + MARGIN)
	for n in closedList: 
 		j += colorIncrement
 		i = int(j)
 		new = ((MARGIN + WIDTH) * n[1]+ MARGIN, (MARGIN + HEIGHT) * n[0] + MARGIN)
		pygame.draw.line(screen, (255, i, 255), prev, new, 2)
		prev = [(MARGIN + WIDTH) * n[1]+ MARGIN, (MARGIN + HEIGHT) * n[0] + MARGIN]
	
	#Draw start and goal			
 	pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * startPoint.y + MARGIN, (MARGIN + HEIGHT) * startPoint.x + MARGIN, WIDTH, HEIGHT])
 	pygame.draw.rect(screen, RED, [(MARGIN + WIDTH) * goalPoint.y + MARGIN, (MARGIN + HEIGHT) * goalPoint.x + MARGIN, WIDTH, HEIGHT])
	
	#Draw legend
	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	fontsize = 20
	myfont = pygame.font.SysFont("monospace", 20)

	# render text
	v = 10
	s = fontsize + 5
	closed_text = myfont.render("Closed Cells", 1, ORANGE)
	path_text = myfont.render("Path", 1, (50,127,127))
	start_text = myfont.render("Start", 1, GREEN)
	goal_text = myfont.render("Goal", 1, RED)
	screen.blit(closed_text, (10, v))
	screen.blit(path_text, (10, v+s))
	screen.blit(start_text, (10, 2*v+s))
	screen.blit(goal_text, (10, 3*v+s))
 	
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		done = True

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

