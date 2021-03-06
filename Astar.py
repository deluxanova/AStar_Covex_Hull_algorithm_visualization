import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')


RED = (255, 0, 0)
GREEN = (0, 204,102)
L_BLUE = (45,94,179)
YELLOW = (255, 255, 0)
DEF = (20,20,20)
CYAN = (0,255,255)
ORANGE = (255, 165 ,0)
GREY = (0,0,0)
WHITE = (128,128,128)


class Spot:
	def __init__(self,row,col,width,total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = DEF
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row,self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == L_BLUE

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == YELLOW

	def reset(self):
		self.color = DEF

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = L_BLUE

	def make_end(self):
		self.color = YELLOW

	def make_path(self):
		self.color = CYAN

	def draw(self,win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
	
	def update_neighbors(self,grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
			self.neighbors.append(grid[self.row][self.col - 1])



	def __lt__(self,other):		#less than
		return False


def h(p1,p2): #calculating the heuristics using manhattan distance
	x1,y1 = p1
	x2,y2 = p2
	return math.sqrt( abs(x1 - x2)*2 + abs(y1 - y2)*2 )

def reconstruct(came_from,current,draw): #to reconstruct the original path
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm(draw,grid,start,end): # the main algorithm
	count = 0
	open_set = PriorityQueue()
	open_set.put((0,count,start))
	came_from = {}
	
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(),end.get_pos())

	open_set_hash = {start} #to check for items in priority queue
	
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end: #make path
			reconstruct(came_from,end,draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current]+1
			
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] =  temp_g_score + h(neighbor.get_pos(),end.get_pos())
				if neighbor not in open_set_hash:
					count+=1
					open_set.put((f_score[neighbor],count,neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows,width): #creating grid
	grid = []
	gap = width // rows #width of each cube

	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i,j,gap,rows) 
			grid[i].append(spot)

	return grid

def draw_grid(win,rows,width): #creating grid
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win,WHITE,(0,i*gap),(width,i*gap))
		for j in range(rows):
			pygame.draw.line(win,WHITE,(j*gap,0),(j*gap,width))

def draw(win,grid,rows,width): #to draw the complete grid
	win.fill(DEF)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win,rows,width)
	pygame.display.update()

def get_clicked_pos(pos,rows,width): #get position of the cursor when clicked
	gap = width // rows
	y,x = pos

	row = y // gap
	col = x // gap

	return row,col

def main(win,width):
	ROWS = 50
	
	#generate grid and get 2d array of spots
	grid = make_grid(ROWS,width)

	start = None
	end = None
	run = True

	while run:
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: #left click
				pos = pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,ROWS,width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()
				elif not end and spot != start:
					end = spot
					end.make_end()
				elif spot != end and spot != start:
					spot.make_barrier()


			elif pygame.mouse.get_pressed()[2]: #right click
				pos = pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,ROWS,width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN,WIDTH) 
		
		


		
