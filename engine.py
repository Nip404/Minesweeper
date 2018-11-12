import pygame
import random
import time
import numpy
import sys

sys.setrecursionlimit(10000)

class Square:
    def __init__(self,state=0):
        self.state = state
        self.number = 1
        
        self.covered = True
        self.flagged = False

    def revealAll(self,grid,ref):
        if self.flagged:
            return

        self.covered = False
        neighbours = [i for i in [[ref[0]-1,ref[1]-1],[ref[0],ref[1]-1],[ref[0]+1,ref[1]-1],[ref[0]-1,ref[1]],[ref[0]+1,ref[1]],[ref[0]-1,ref[1]+1],[ref[0],ref[1]+1],[ref[0]+1,ref[1]+1]] if (i[0] >= 0 and i[1] >= 0 and i[0] < len(grid[0]) and i[1] < len(grid))]

        for n in neighbours:
            if not grid[n[1]][n[0]].number and grid[n[1]][n[0]].covered:
                grid[n[1]][n[0]].revealAll(grid,n)
            else:
                grid[n[1]][n[0]].covered = False

class Grid:
    colours = {1:(0,0,255),2:(50,205,50),3:(255,140,0),4:(255,0,0),5:(148,0,211),6:(220,20,60),7:(0,206,209),8:(255,105,180)}
    # min = 1, max = 1000, default = 8, lower = harder
    mine_distribution = 8
    
    def __init__(self,surf_size,square_size,blit_dest=[0,0]):
        self.surf = pygame.Surface(surf_size)
        self.resolution = [int(i/square_size) for i in self.surf.get_size()]
        
        self.size = square_size
        self.blit_dest = blit_dest
        
        self.isGenerated = False
        self.minesCount = int(numpy.prod(self.resolution)//self.mine_distribution)
        self.flags = self.minesCount

        self.grid = [[Square() for _ in range(self.resolution[0])] for _ in range(self.resolution[1])]
        self.font = pygame.font.SysFont("Garamond MS",self.size)
        
    def generate(self,pos):
        count = 0

        while count < self.minesCount:
            for p,i in enumerate(self.grid):
                for q,j in enumerate(i):
                    if random.randint(1,self.mine_distribution) == 1 and not [q,p] in [i for i in [pos,[pos[0]-1,pos[1]-1],[pos[0],pos[1]-1],[pos[0]+1,pos[1]-1],[pos[0]-1,pos[1]],[pos[0]+1,pos[1]],[pos[0]-1,pos[1]+1],[pos[0],pos[1]+1],[pos[0]+1,pos[1]+1]] if (i[0] >= 0 and i[1] >= 0 and i[0] < len(self.grid[0]) and i[1] < len(self.grid))] and not j.number == -1 and count < self.minesCount:
                        j.number = -1
                        count += 1

        for y,row in enumerate(self.grid):
            for x,sq in enumerate(row):
                surroundingMines = 0

                if sq.number == -1:
                    continue

                combinations = [[x-1,y-1],[x,y-1],[x+1,y-1],[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]]
                for combination in combinations:
                    if combination[0] >= 0 and combination[0] < len(self.grid[0]) and combination[1] >= 0 and combination[1] < len(self.grid):
                        if self.grid[combination[1]][combination[0]].number == -1:
                            surroundingMines += 1
                            
                sq.number = surroundingMines

        self.isGenerated = True

    def move(self,pos,button):
        gridRef = self.coords_to_gridRef(pos)
        
        if gridRef is None:
            return
        if not self.isGenerated:
            self.generate(gridRef)

        if button == 1 and not self.grid[gridRef[1]][gridRef[0]].flagged:
            if self.grid[gridRef[1]][gridRef[0]].number:
                self.grid[gridRef[1]][gridRef[0]].covered = False
            else:
                self.grid[gridRef[1]][gridRef[0]].revealAll(self.grid,gridRef)
        elif button == 3:
            if self.flags > 0 and not self.grid[gridRef[1]][gridRef[0]].flagged:
                self.grid[gridRef[1]][gridRef[0]].flagged = True
            elif self.grid[gridRef[1]][gridRef[0]].flagged:
                self.grid[gridRef[1]][gridRef[0]].flagged = False

            self.flags = self.minesCount - sum(sum(i.flagged for i in row) for row in self.grid)

    def coords_to_gridRef(self,pos):
        return [int((pos[i]-self.blit_dest[i])//self.size) for i in range(2)] if all(x < self.resolution[p] for p,x in enumerate([int((pos[i]-self.blit_dest[i])//self.size) for i in range(2)])) else None

    def draw(self,surf):
        for y,row in enumerate(self.grid):
            for x,square in enumerate(row):
                if not square.covered:
                    pygame.draw.rect(self.surf,(255,255,255),(x*self.size,y*self.size,self.size,self.size),0)

                    if square.number == -1:
                        pygame.draw.circle(self.surf,(255,0,0),[int(x*self.size+(self.size/2)),int(y*self.size+(self.size/2))],int(self.size/4),0)
                    elif square.number:
                        msg = self.font.render(str(square.number),True,self.colours[square.number])
                        self.surf.blit(msg,msg.get_rect(center=[x*self.size+(self.size/2),y*self.size+(self.size/2)]))
                else:
                    pygame.draw.rect(self.surf,(150,150,150),(x*self.size,y*self.size,self.size,self.size),0)

                    if square.flagged:
                        pygame.draw.polygon(self.surf,(255,0,0),[[x*self.size+(0.3*self.size),y*self.size+(0.2*self.size)],[x*self.size+(0.4*self.size),y*self.size+(0.2*self.size)],[x*self.size+(0.4*self.size),y*self.size+(0.22*self.size)],[x*self.size+(0.8*self.size),y*self.size+(0.4*self.size)],[x*self.size+(0.4*self.size),y*self.size+(0.6*self.size)],[x*self.size+(0.4*self.size),y*self.size+(0.8*self.size)],[x*self.size+(0.3*self.size),y*self.size+(0.8*self.size)]],0)

        for x in range(1,len(self.grid[0])):
            pygame.draw.line(self.surf,(0,0,0),[x*self.size,0],[x*self.size,surf.get_height()],1)
        for y in range(1,len(self.grid)):
            pygame.draw.line(self.surf,(0,0,0),[0,y*self.size],[surf.get_width(),y*self.size],1)

        surf.blit(self.surf,self.blit_dest)

    def check_game_status(self):
        return True if ((not any(any((s.flagged and not s.number == -1) or (not s.flagged and s.number == -1) for s in row_) for row_ in self.grid)) and all(all(not t.covered or (t.covered and t.flagged) for t in _row) for _row in self.grid)) else (False if any(any(g.number == -1 and not g.covered for g in row) for row in self.grid) else None) 

    def reset(self,square_size=None):
        if square_size is not None:
            self.resolution = [int(i/square_size) for i in self.surf.get_size()]
            self.size = square_size
            self.minesCount = int(numpy.prod(self.resolution)//self.mine_distribution)
            self.font = pygame.font.SysFont("Garamond MS",self.size)
        
        self.grid = [[Square() for _ in range(self.resolution[0])] for _ in range(self.resolution[1])]
        self.isGenerated = False
        self.flags = self.minesCount

class Banner:
    def __init__(self,surf_size,grid,blit_dest=[0,0]):
        self.grid = grid
        self.surf = pygame.Surface(surf_size)

        self.t0 = time.time()
        self.blit_dest = blit_dest
        self.h1 = pygame.font.SysFont("Garamond MS",50)
        self.h2 = pygame.font.SysFont("Garamond MS",30)

    def update(self):
        self.surf.fill((250,250,255))
        pygame.draw.line(self.surf,(0,0,0),[0,0],[0,self.surf.get_height()],4)
        
        head = self.h1.render("Minesweeper",False,(0,0,0))
        foot = self.h2.render("by NIP",False,(0,0,0))

        self.surf.blit(head,head.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()/12]))
        self.surf.blit(foot,foot.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()/7]))

        flg = self.h2.render(f"Flags Remaining: {self.grid.flags}/{self.grid.minesCount}",True,(0,0,0))
        self.surf.blit(flg,flg.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()/2 - 50]))

        tim = self.h2.render(f"Time Elapsed: {int(time.time()-self.t0)}",True,(0,0,0))
        self.surf.blit(tim,tim.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()/2]))

        difs = {100:"Easy",50:"Medium",25:"Hard",10:"Impossible"}
        dif = self.h2.render(f"Difficulty: {difs[self.grid.size]}",True,(0,0,0))
        self.surf.blit(dif,dif.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()/2 + 50]))

    def draw(self,surf):
        surf.blit(self.surf,self.blit_dest)

    def reset(self):
        self.t0 = time.time()
