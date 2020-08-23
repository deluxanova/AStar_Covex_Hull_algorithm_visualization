import pygame
import math

points = []
hullfinal = []

def Left_index(points): 
    minn = 0
    for i in range(1,len(points)): 
        if points[i][0] < points[minn][0]: 
            minn = i 
        elif points[i][0] == points[minn][0]: 
            if points[i][1] > points[minn][1]: 
                minn = i 
    return minn 
  

def orientation(p, q, r): 
    val = (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])
  
    if val == 0: 
        return 0
    elif val > 0: 
        return 1
    else: 
        return 2


def generateLines(screen, hull,points):

	o = [(hull[i],hull[i+1]) for i in range(0,len(hull)-1,1)]

	for i in hull:
		pygame.draw.circle(screen, (0,255,0),(i[1],i[0]),10)

	for i in o:
		p1 = i[0]
		p2 = i[1]
		pygame.draw.line(screen, (0, 0, 255), (p1[1],p1[0]), (p2[1],p2[0]))


def convexHull(points, n,screen): 
     
    if n < 3: 
        return
  
    l = Left_index(points) 
  
    hull = [] 
      
    p = l 
    q = 0
    while(True): 
            
        hull.append(p) 
 
        q = (p+1)%n 
  
        for i in range(n): 
            if(orientation(points[p],points[i], points[q]) == 2): 
                q = i 
        p = q 
  
        if(p == l): 
            break
  	
    for curr in hull: 
       hullfinal.append((points[curr][0],points[curr][1]))
    generateLines(screen,hullfinal,points)


def GUI():

	pygame.init()
	screen = pygame.display.set_mode((1280,720))
	pygame.display.set_caption("Convex Hull Algorithm Visualization")
	clock = pygame.time.Clock()
	 
	loop = True
	press = False
	while loop:
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	                loop = False
	    
	        px, py = pygame.mouse.get_pos()
	        if pygame.mouse.get_pressed() == (1,0,0):
	        	pos = pygame.mouse.get_pos()
	        	y,x = pos
	        	points.append((x, y)) 
	        	pygame.draw.circle(screen, (128,128,128),(pos[0],pos[1]),7)
	      
	        if event.type == pygame.MOUSEBUTTONUP:
	            press == False
	        pygame.display.update()
	        clock.tick(1000)

	        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
	        	dots = list(set(points))
	        	convexHull(dots,len(dots),screen) 

	        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
	        	pygame.quit()

	pygame.quit()


def main():
	GUI()

main()
