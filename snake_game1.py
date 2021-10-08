import os
import pygame
import random
from pygame import mixer

#Defining colours
white = (255, 255, 255)
red =  (255, 0, 0)
yellow = (255, 255, 0)
purple =  (148, 0, 211)
black = (0, 0, 0)
blue = (204, 204, 255)


pygame.init()

mixer.init()

#creating background image

#creating window for the game
gameWindow = pygame.display.set_mode((850, 600))
pygame.display.set_caption ("Snake Game")

bgimg = pygame.image.load("welcome.jpg")
bgimg = pygame.transform.scale(bgimg, (850, 600)).convert_alpha()

pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x ,y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake (gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():

    exit_game = False
    while not exit_game:
        
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mixer.music.load('game.mp3')
                            mixer.music.play()
                            gameloop()
        gameWindow.blit(bgimg, (0,0))
        text_screen ("Welcome to Snakes!", black, 220, 210)
        text_screen ("Press Space Bar to Play", black, 180, 270)
        pygame.display.update()
        clock.tick(60)


def gameloop():
    exit_game = False
    game_over = False
    snake_x = 55
    snake_y = 60
    snake_size = 10
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    food_x = random.randint(20, 600/2)
    food_y = random.randint(10, 850/2)
    food_size = 10
    fps = 30
    score = 0
    snk_list = []
    snk_length = 1
    bgimg = pygame.image.load("game.jpg")
    bgimg = pygame.transform.scale(bgimg, (850, 600)).convert_alpha()

    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
            
    with open ("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:

        if game_over:
            with open ("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            bgimg = pygame.image.load("game_over.jpg")
            bgimg = pygame.transform.scale(bgimg, (850, 600)).convert_alpha()
            gameWindow.blit(bgimg,(0,0))
            text_screen("GameOver ! Press Enter to Continue", purple, 100, 260)

            for event in pygame.event.get():         # Event handeling will be done in this for loop.
                    if event.type == pygame.QUIT:
                        exit_game = True
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            mixer.music.load('welcome.mp3')
                            mixer.music.play()
                            welcome()
        
        else:

            for event in pygame.event.get():         # Event handeling will be done in this for loop.
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)< 6: # this to make the snake eat the food and present new food
                score+= 10                                            # notice it's in while loop
                food_x = random.randint(20, 600/2)
                food_y = random.randint(10, 850/2)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            head = []
            head.append (snake_x)
            head.append (snake_y)
            snk_list.append(head)

            
            
            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                game_over = True
                mixer.music.load('crash.mp3')
                mixer.music.play()

            if snake_x <0 or snake_x > 850 or snake_y < 0 or snake_y> 600:
                game_over = True
                mixer.music.load('crash.mp3')
                mixer.music.play()

            
            gameWindow.blit(bgimg,(0,0))
            text_screen ("Score: " + str(score) + " High Score: " + str(hiscore), blue, 5, 5) # str is writtenn to make it use the int score as string
            plot_snake(gameWindow, red, snk_list, snake_size)
            pygame.draw.rect(gameWindow, yellow, (food_x, food_y, food_size, food_size))

        
        pygame.display.update() # updating the displayS
        clock.tick(fps)

    pygame.quit()
    quit

mixer.music.load('welcome.mp3')
mixer.music.play()
welcome()

