import pygame
import random
import sys
import time
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 400      # 屏幕宽度
SCREEN_HEIGHT = 380     # 屏幕高度
SIZE = 20               # 小方格大小
LINE_WIDTH = 0          # 网格线宽度
BGCOLOR = (40,40,60)    #
snake_color = (0, 255, 255)   # 🐍的颜色
FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]# 食物的分值及颜色
RED = (200, 30, 30)

# 游戏区域的坐标范围
SCOPE_X = (0, SCREEN_WIDTH // SIZE)
SCOPE_Y = (0, SCREEN_HEIGHT // SIZE)

'''游戏初始化'''
def initGame():
    # 初始化pygame, 设置展示窗口
    pygame.init()   # 初始化检查
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # 设置标题
    pygame.display.set_caption('Greedy_Snake!')
    return screen
'''初始化🐍'''
def init_snake():
    snake = deque() # 双向队列
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))
    return snake
'''创造食物'''
def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        # 如果食物出现在蛇身上，则重来
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y
'''食物样式'''
def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]
'''Gameover'''
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

#主函数
def main():
    screen = initGame()
    snake = init_snake()
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
    fwidth, fheight = font2.size('GAME OVER')
    pos = (1,0) #方向
    b = True
    game_over = True
    start = False
    kee_going = True
    speed = 0.5
    pause = False  # 暂停
    last_move_time = time.time()
    while kee_going:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    if b and not pos[1]:    # 这个判断是为了防止蛇向上移时按了向下键，导致直接 GAME OVER
                        pos = (0, -1)
                        b = False
                elif event.key in (K_s, K_DOWN):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (K_a, K_LEFT):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_d, K_RIGHT):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False
        screen.fill(BGCOLOR) #填充背景色，刷新画面
        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not  pause :
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        snake.appendleft(next_s)
                        food = create_food(snake)
                        food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop() # 移除列表最后一个元素
                        else:
                            game_over = True
        if not game_over:
            pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)
        # 绘制🐍
        for s in snake:
            pygame.draw.rect(screen,snake_color, (s[0] * SIZE, s[1] * SIZE + LINE_WIDTH,SIZE, SIZE), 0)
        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER',
                           RED)
        # 刷新屏幕
        pygame.display.update()
main()