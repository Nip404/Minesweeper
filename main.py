import engine
import pygame
import sys

# add custom resolution menu

s = [1000,700]
board_size = [700,s[1]]
banner_size = [s[0]-board_size[0],s[1]]

pygame.init()
screen = pygame.display.set_mode(s,0,32)
pygame.display.set_caption("Minesweeper by NIP")

h1 = pygame.font.SysFont("Garamond MS",40)
h2 = pygame.font.SysFont("Garamond MS",20)

def menu():
    standard = (100,255,100)
    onHover = (250,250,20)

    head = pygame.font.SysFont("Garamond MS",65).render("Minesweeper",True,(0,0,0))
    version = h2.render("version 1.0.0",True,(0,0,0))
    foot = h2.render("by NIP",True,(0,0,0))
    
    button1 = pygame.Rect(screen.get_width()/2 - 200,screen.get_height()/5,400,screen.get_height() * (3/20))
    button2 = pygame.Rect(screen.get_width()/2 - 200,screen.get_height() * (2/5),400,screen.get_height() * (3/20))
    button3 = pygame.Rect(screen.get_width()/2 - 200,screen.get_height() * (3/5),400,screen.get_height() * (3/20))
    button4 = pygame.Rect(screen.get_width()/2 - 200,screen.get_height() * (4/5),400,screen.get_height() * (3/20))

    b1 = h1.render("Easy",True,(40,150,20))
    b2 = h1.render("Medium",True,(255,128,0))
    b3 = h1.render("Hard",True,(255,0,0))
    b4 = h1.render("Impossible",True,(0,0,0))
    
    while True:
        mouse = pygame.Rect([i-1 for i in pygame.mouse.get_pos()],[2,2])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.colliderect(button1):
                    return 100
                elif mouse.colliderect(button2):
                    return 50
                elif mouse.colliderect(button3):
                    return 25
                elif mouse.colliderect(button4):
                    return 10
        
        screen.fill((255,255,255))
        pygame.draw.rect(screen,standard if not mouse.colliderect(button1) else onHover,button1,0)
        pygame.draw.rect(screen,standard if not mouse.colliderect(button2) else onHover,button2,0)
        pygame.draw.rect(screen,standard if not mouse.colliderect(button3) else onHover,button3,0)
        pygame.draw.rect(screen,standard if not mouse.colliderect(button4) else onHover,button4,0)
        
        pygame.draw.rect(screen,(0,0,0),button1,2)
        pygame.draw.rect(screen,(0,0,0),button2,2)
        pygame.draw.rect(screen,(0,0,0),button3,2)
        pygame.draw.rect(screen,(0,0,0),button4,2)

        screen.blit(head,head.get_rect(center=[screen.get_width()/2,screen.get_height()/10]))
        screen.blit(version,version.get_rect(center=[screen.get_width()/2,screen.get_height()/7]))
        screen.blit(foot,foot.get_rect(center=[screen.get_width()/2,screen.get_height()/6]))

        screen.blit(b1,b1.get_rect(center=button1.center))
        screen.blit(b2,b2.get_rect(center=button2.center))
        screen.blit(b3,b3.get_rect(center=button3.center))
        screen.blit(b4,b4.get_rect(center=button4.center))

        pygame.display.flip()

def result(grid,banner):
    cover = pygame.Surface(screen.get_size())
    cover.set_alpha(200)
    cover.fill((0,0,0))

    msg = h1.render(f"You {'Won' if grid.check_game_status() else 'Lost'}",True,(255,255,255))
    end = h2.render("Press any key to continue",True,(255,255,255))

    cover.blit(msg,msg.get_rect(center=[cover.get_width()/2,cover.get_height()/2.5]))
    cover.blit(end,end.get_rect(center=[cover.get_width()/2,cover.get_height()/2]))

    x,y,cycle,wave = 0,0,True,[[0,0]]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                return

        grid.draw(screen)
        banner.draw(screen)
        screen.blit(cover,(0,0))

        pygame.display.flip()

        if cycle:
            for i in wave:
                try:
                    grid.grid[i[1]][i[0]].covered = False
                except:
                    pass

            new = []
            for n in [e for e in [[i[0]+1,i[1]] for i in wave]+[[i[0],i[1]+1] for i in wave] if e[0] < len(grid.grid[0]) and e[1] < len(grid.grid)]:
                if not n in new:
                    new.append(n)
            wave = new[:]

            if not len(wave):
                cycle = False
                    
def main():
    square_size = menu()
    grid = engine.Grid(board_size,square_size)
    banner = engine.Banner(banner_size,grid,[grid.surf.get_width(),0])
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid.move(pygame.mouse.get_pos(),event.button)

        banner.update()

        grid.draw(screen)
        banner.draw(screen)

        pygame.display.flip()

        if grid.check_game_status() is not None:
            result(grid,banner)
            square_size = menu()
            grid.reset(square_size)
            banner.reset()
        
if __name__ == "__main__":
    main()
