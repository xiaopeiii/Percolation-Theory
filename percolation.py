from publish import *

# # Computational Mathematics
# ## Project C
# ## 2024-02-13
# ## Te Pei (<te.pei@st-hughs.ox.ac.uk>)
# ## St. Hugh's College

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

#
# ***
# ### C.1
#

# Idea: np.random will give output randomly in [0,1), then the probability of this random number smaller than p is exactly p.
# Then, use np.random.rand(n,n) to generate a grid with size n*n, with each site True with probability p.
def make_grid(n,p):
    return np.random.rand(n,n) < p #From [0,1) randomly choose n*n numbers, if < p then True

# Example: Generate a grid of size 8*8, each site being True with probability 0.6
A=make_grid(8,0.6)
print(A)

# In order to test the empirical probability: generating 100 matrixs, as B, of size 10*10, each site True with probability 0.3; By using np.mean() to calculate the total mean of B
B=[make_grid(10,0.3) for _ in range(100)]
print(np.mean(B))
# The results shows that the empirical probability approximately equals to p=0.3

#
# ***
# ### C.2
#

# Idea: Using matplotlib to draw a visualise grid. 
def visualise_grid(grid):
    # Draw a grid with colormap=gray, which means coloring "True" sites to be white and "False" sites to be black.
    plt.imshow(grid, cmap='gray') 

    # Shift the x,y ticks, to make sure they align with the borders of each site.
    # Use plt.xticks to set x labels; from -0.5 to the length of the grid, with each step=1; use "" to hide the numbers.
    plt.xticks(np.arange(-0.5,len(grid),1), "") 
    plt.yticks(np.arange(-0.5,len(grid),1), "")

    # Add x,y axes to the grid; set color to be black; set linewidth=2 to be clear enough
    plt.grid(axis="both", color="black", linewidth=2) 

    # Show the final graph
    plt.show()

# Sample1: visualise the grid in part C.1 (A=make_grid(8,0.6))
visualise_grid(A)
# Sample2: visualise make_grid(6,0.4)
visualise_grid(make_grid(6, 0.4))

#
# ***
# ### C.3
#

# Idea: Consider the each site of the input grids: "grid", "fill status".
# 1.If a site is False in grid, which means it's closed, colored in black.
# 2.If a site is True in grid and True in fill status, which means it's open filled, colored in blue
# 3.If a site is True in grid and False in fill status, which means it's open unfilled, colored in white
def visualise_fill(grid, fill_status):
    # Set up: create color_map as a matrix with all entries zero, with the same size with "grid".
    color_map=np.zeros_like(grid, dtype=int) 

    # Set color_map with different values(0 means black, 1 means white, 2 means blue)
    color_map[grid == False] = 0  # Set closed entries be 0
    color_map[(grid == True)&(fill_status == True)] = 1  # Set open filled entries be 1
    color_map[(grid == True)&(fill_status == False)] = 2  # Set open unfilled entries be 2
    
    # Set "ccamp":the color map of each site. Each site of color_map with a correspond color.
    ccmap=matplotlib.colors.ListedColormap(['black','blue','white']) # Create a color map in color lists
    plt.imshow(color_map, cmap=ccmap) #Coloring "color_map", with colormap=ccmap
    
    # Coloring gridlines and set the borders of each square to black, similiarly to C.2
    plt.xticks(np.arange(-0.5,len(grid),1),"")
    plt.yticks(np.arange(-0.5,len(grid),1),"")
    plt.grid(axis='both', color='black', linewidth=2)

    # Show the final graph
    plt.show()

#Test a 3*3 matrix
Grid = np.array([[1,0,1],[0,0,1],[1,1,0]])
Fill_status = np.array([[1,0,1],[0,0,1],[0,0,0]])
visualise_fill(Grid, Fill_status)

#Test a 3*3 matrix if fill_status all false
Grid = np.array([[0,0,0],[1,0,1],[1,1,1]])
Fill_status = np.array([[0,0,0],[0,0,0],[0,0,0]])
visualise_fill(Grid, Fill_status)

#
# ***
# ### C.4
#

#Idea: First generate a "fill_status" grid with same size as testing grid, initialized to False.
#Then, Checking from each site of the first row of the testing grid: if the site is open then set fill_status grid be True.
#Define an recursive function(ffill): From each open site found, recursively visits the neighboring sites(i.e left, right, up, down), set them to be True if they are open.
#Also, set boundary conditions: 1.left, right, upper, lower bounds 2.meet some site already filled 3.meet closed site. 
#Those conditions is to make sure that the recursion step will end at some point.
def compute_fill(grid):
    fill_status=np.zeros_like(grid, dtype=bool) #Generate the fill_status matrix, initialized to False
    grid_rows, grid_columns = grid.shape #Find the size of testing grid, in order to set the boundary conditions.

    def ffill(row,col): #The recusive function start from the top
        #1. left, right, upper, lower boundaries
        if row < 0 or row >= grid_rows or col < 0 or col >= grid_columns:
            return
        
        #2. meet already filled site
        if fill_status[row,col] == True:
            return
        
        #3. meet closed site
        if grid[row,col] == False:
            return
        
        #If didn't reach boundary conditions, set this site to be True and check the neighbours around that site.
        else: 
            fill_status[row,col] = True #Set this site to be True
            ffill(row+1,col) #Go down
            ffill(row,col+1) #Go right
            ffill(row-1,col) #Go up
            ffill(row,col-1) #Go right

    #From the open sites in the top row        
    for col in range(grid_columns):
        if grid[0,col] == True:
            ffill(0,col) #For each open site in the top row, applying recursive function
    return(fill_status)

#Example
A = make_grid(10,0.5)
visualise_fill(A, compute_fill(A))

#
# ***
# ### C.5
#

#Idea: test whether the last row of "fill_status" have any "True" site.
def percolates(grid):
    grid_rows, grid_columns = grid.shape #Get the number of rows in order to know which row should be tested.(where is the last row)
    percolates = False
    for col in range(grid_columns):
        if compute_fill(grid)[grid_rows-1,col] == True: #Generate the fill_status of the testing grid and test the last row one by one
            percolates = True
            break #if exist a True site, break and return "True"
    return(percolates) #if no "True" site, clearly return "False"

#Test 10 20*20 grids with p = 0.6
for _ in range (10):
    A = make_grid(20,0.6)
    plt.title(percolates(A)) #Generate title
    visualise_fill(A, compute_fill(A)) 

#
# ***
# ### C.6
#

#Idea: Split [0.4,0.7] into 31 points, at each point p, generate 1000 grid(20,p), verify whether they are percolate and calculate the empirical probability of being percolate.
N = 1000
P = np.linspace(0.4, 0.7, 31) #Chose 31 points evenly in P

#Let C_p be a list, with each element correpond to a 'p'
C_p = [] 

for p in P: #Take different probability in P
    count_p = 0 #Count the number of percolate grids
    for _ in range (N):
        count_p += percolates(make_grid(20,p)) #"+1" if percolate, "+0" if not percolate
    C_p.append(count_p/N) #add percolation probability at p to the end of C_p

#Plot the grid, C_p-P function, x,y labels
plt.grid()
plt.plot(P, C_p)
plt.xlabel("Vacancy Probability p")
plt.ylabel("Percolation Probability C(p)")
plt.show()

publish()
