#! C:\Users\ishit\OneDrive\Desktop\Projects\Python_Projects\Dijkstra_Pathfinder\myvenv\Scripts\python.exe

from tkinter import messagebox, Tk
import pygame
import sys

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width,window_height))


columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

class Box:
    #initialising the position of the box
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    #helps us draw the box on the window
    def draw(self,win,color):
        pygame.draw.rect(win,color, (self.x*box_width, self.y*box_height, box_width-2, box_height-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y+1])

#create grid - creating box objects to create a grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

#Set neighbors - setting neighbors for every box in the grid
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()


start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)


def main():

    #Flag to trigger the algorithm- variable triggered by presseing key
    begin_search = False

    #we can't run the algorithm until this value is set as target box will be set manually
    target_box_set = False

    # flag to help us interrupt the algorithm when target is found
    searching = True

    #to store the box that we are going to reach
    target_box = None


    #main loop
    while True:

        #for events
        for event in pygame.event.get():

            #Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                #Draw Wall
                if event.buttons[0]: #left mouse button
                    #getting the no. of row and column using the mouse coordinates
                    i = x//box_width
                    j = y//box_height
                    grid[i][j].wall = True

                #Set Target
                if event.buttons[2] and not target_box_set: #right mouse button
                    #getting the no. of row and column using the mouse coordinates
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True

            #start algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
        
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:  #we revert back to previous boxes to get path
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution","There is no solution")
                    searching = False

        window.fill((0,0,0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50,50,50))
                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0,200,0))
                if box in path:
                    box.draw(window, (0,0,200))

                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (90,90,90))
                if box.target:
                    box.draw(window, (200,200,0))


        #updates display
        pygame.display.flip()

main()