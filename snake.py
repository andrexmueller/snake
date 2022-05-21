from turtle import st
import pygame
from classes import Apple, Snake, Game, Stats
from configs import *
import winsound



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

apple = Apple(screen)
snake = Snake(screen, apple)
game = Game(screen, snake, apple)
stats = Stats(screen, snake, game)
    

while True:

        
    game.game_loop()
    stats.display_stats("Points", stats.snake.points, 28, 28)
    stats.display_stats("Rounds", stats.game.rounds, 28, 56)
    stats.display_stats("Hi Score", stats.snake.highest, 200, 28)
    
    pygame.display.update()    
    screen.fill((0,0,0))
    for e in pygame.event.get():
        print(e)
        if e.type == pygame.QUIT:
            exit()
        if e.type == 768:
            #print(e.scancode)
            snake.change_direction(e.scancode)
        # if e.type == 771:
        #     game.pause_game()

    clock.tick(snake.veolcity)
 
    



