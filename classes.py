from dataclasses import dataclass
from random import randint
import pygame
from configs import *




directions = {
    'up': (0, -SIZE), 
    'down': (0, SIZE), 
    'left': (-SIZE, 0), 
    'right': (SIZE, 0)
}


class Snake:
    def __init__(self, screen, apple, head_x=X0, head_y=Y0):
        self.screen = screen
        self.head_x = head_x
        self.head_y = head_y
        self.apple = apple
        self.veolcity = 5
        self.head = pygame.Rect(head_x, head_y, SIZE, SIZE)
        b1 = pygame.Rect(head_x, head_y + SIZE, SIZE, SIZE)
        b2 = pygame.Rect(head_x, head_y + 2 * SIZE, SIZE, SIZE)
        self.body = [b1, b2]
        self.direction = 'up'
        self.hit_something = False
        self.points = 0
        self.highest = 0
        # sound
        #self.sound =  pygame.mixer.Sound('click.ogg')

    def draw(self):
        pygame.draw.rect(self.screen, COLOR_SNAKE, self.head, 0, border_radius=5)
        for part in self.body:
            pygame.draw.rect(self.screen, COLOR_SNAKE, part, 0, border_radius=3)

    def move(self):
        if not self.hit_something:
            self.head_x = self.head_x + directions[self.direction][0]
            self.head_y = self.head_y + directions[self.direction][1]
            
            b1  = self.head
            self.head = pygame.Rect(self.head_x, self.head_y, SIZE, SIZE)
            # check autocollision
            if self.head.collidelist(self.body) >= 0:
                self.hit_something = True
            # check border collision
            if self.head_x <= SIZE - 1 or self.head_x >= WIDTH - SIZE - 1:
                self.hit_something = True
                self.head = b1
            if self.head_y >= HEIGHT - SIZE - 1 or self.head_y <= MARGIN_UP - 1:
                self.hit_something = True
                self.head = b1
            if not self.head.contains(self.apple.rect) and not self.hit_something:
                self.body.pop()
            #else:
            if self.head.contains(self.apple.rect) and not self.hit_something:
                self.apple.apple_spawn(self.body + [self.head])
                self.veolcity += 1            
                self.points += 1
                self.highest = max(self.points, self.highest)

            self.body.insert(0, b1)
        #self.sound.play()
        self.draw()

    def change_direction(self, key):
        dir = {82: 'up', 81: 'down', 80: 'left', 79: 'right'} #event keydown, scancode
        if key in dir.keys():
            dx, dy = directions[dir[key]]
        else:
            return
        if (self.head_x + dx, self.head_y + dy) == (self.body[0].x, self.body[0].y):
            return
        else:
            self.direction = dir[key]
        
    def reset(self):
        self.head_x = X0
        self.head_y = Y0
        self.veolcity = 5
        self.head = pygame.Rect(self.head_x, self.head_y, SIZE, SIZE)
        b1 = pygame.Rect(self.head_x, self.head_y + SIZE, SIZE, SIZE)
        b2 = pygame.Rect(self.head_x, self.head_y + 2 * SIZE, SIZE, SIZE)
        self.body = [b1, b2]
        self.direction = 'up'
        self.hit_something = False
        self.points = 0



class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.apple_spawn()

    def apple_spawn(self, snake_pos=None):
        self. x, self.y = SIZE * randint(SIZE, WIDTH//SIZE - 2), SIZE * randint(MARGIN_UP//SIZE, HEIGHT//SIZE - 2)
        self.rect = pygame.Rect(self.x, self.y, SIZE, SIZE)
        if snake_pos:
            while self.rect.collidelist(snake_pos) != -1:
                self. x, self.y = SIZE * randint(0, WIDTH//SIZE - 1), SIZE * randint(0, HEIGHT//SIZE - 1)
                self.rect = pygame.Rect(self.x, self.y, SIZE, SIZE)
        self.draw()
        
    def draw(self):      
        pygame.draw.circle(self.screen, RED, ((self.rect.x + SIZE // 2), (self.rect.y + SIZE // 2)), SIZE//2, 0)

    def get_apple_position(self):
        return self.x, self.y


class Game:
    def __init__(self, screen, snake, apple):
        self.screen = screen
        self.snake = snake
        self.apple = apple
        self.rounds = 1
        self.pause = True
        

    

    def game_over(self):
        msg1 = "Game Over!"
        msg2 = "Hit spacebar to continue"
        font1 = pygame.font.SysFont("arial", 52, bold=True)
        font2 = pygame.font.SysFont("arial", 26)
        text1 = font1.render(msg1, True, RED)
        text2 = font2.render(msg2, True, GREEN)
        px1 = (WIDTH - font1.size(msg1)[0]) // 2
        py1 = (HEIGHT - MARGIN_UP - font1.size(msg2)[1]) // 2 + MARGIN_UP
        px2 = (WIDTH - font2.size(msg2)[0]) // 2
        py2 = py1 + font2.size(msg2)[1] + 20
        self.screen.blit(text1, (px1, py1))
        self.screen.blit(text2, (px2, py2))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == 768:
                if e.scancode == 44:
                    self.snake.reset()
                    self.rounds += 1

    def pause_game(self):
        
        msg1 = "Snake Clone"
        msg2 = "Press a key to go"
        font1 = pygame.font.SysFont("arial", 52, bold=True)
        font2 = pygame.font.SysFont("arial", 26)
        text1 = font1.render(msg1, True, RED)
        text2 = font2.render(msg2, True, GREEN)
        px1 = (WIDTH - font1.size(msg1)[0]) // 2
        py1 = (HEIGHT - MARGIN_UP - font1.size(msg2)[1]) // 2 + MARGIN_UP
        px2 = (WIDTH - font2.size(msg2)[0]) // 2
        py2 = py1 + font2.size(msg2)[1] + 20
        self.screen.blit(text1, (px1, py1))
        self.screen.blit(text2, (px2, py2))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == 768:
                if e.scancode == 44:
                    self.pause = not self.pause


        
    def game_loop(self):
        if not self.pause:
            self.snake.move()
            self.apple.draw()
            pygame.draw.line(self.screen, GREY, (SIZE//2, MARGIN_UP), (SIZE//2, HEIGHT), SIZE)
            pygame.draw.line(self.screen, GREY, (WIDTH - SIZE//2, MARGIN_UP - SIZE//2), (WIDTH - SIZE//2, HEIGHT), SIZE)
            pygame.draw.line(self.screen, GREY, (0, HEIGHT - SIZE//2), (WIDTH - SIZE//2, HEIGHT - SIZE//2), SIZE)
            pygame.draw.line(self.screen, GREY, (0, MARGIN_UP - SIZE//2), (WIDTH, MARGIN_UP - SIZE//2), SIZE)        
            if self.snake.hit_something:
                self.game_over()
        else:
            self.pause_game()


class Stats:
    def __init__(self, screen, snake, game):
        self.screen = screen
        self.snake = snake
        self.game = game
        

    def display_stats(self, stat_name, stat, px, py):
        font = pygame.font.SysFont("arial", 28, bold=True)
        img = font.render(f'{stat_name}: {stat}', True, WHITE)
        self.screen.blit(img, (px, py))
                 

        


# class Text:
#     all_texts = []
#     def __init__(self, screen, text, size, px, py, color, bold=False, italic=False):
#         self.screen = screen
#         self.text = text
#         self.size = size
#         self.px, self.py = px, py
#         self.color = color
#         self.bold = bold
#         self.italic = italic
#         self.font = pygame.font.SysFont("arial", self.size, bold=self.bold, italic=self.italic)
#         self.img = self.font.render(self.text, True, self.color)
#         Text.all_texts.append(self)

#     def erase_text(self):
#         print(id(self))
#         print(self in Text.all_texts)
#         print(Text.all_texts)

#     @classmethod
#     def draw_text(cls):
#         for f in Text.all_texts:
#             f.screen.blit(f.img, (f.px, f.py))
