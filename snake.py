import sys
from os.path import join, dirname
from random import randint

import pygame

BOARD_WIDTH, BOARD_HEIGHT, SIZE = 40, 25, 20

# Color Configuration
colors = {
    'BLACK': (0, 0, 0),
    'DARK_GRAY': (40, 40, 40),
    'DARK_GREEN': (0, 155, 0),
    'BLUE': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'WHITE': (255, 255, 255)
}
DIRT = {
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP': (0, -1),
    'DOWN': (0, 1)
}


class Menu(object):
    def __init__(self):
        self.choice = 0


class Snake(object):
    def __init__(self):
        self.item = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2), (BOARD_WIDTH // 2 - 1, BOARD_HEIGHT // 2)]
        self.dirt = (1, 0)
        self.AI = False  # Low AI
        self.ate = False
        self.speed = 180  # initial speed
        self.score = 0

    def draw(self, screen):
        for pos in self.item[1:]:
            pygame.draw.rect(screen, colors['DARK_GREEN'], ((pos[0] * SIZE, pos[1] * SIZE), (SIZE, SIZE)))
            pygame.draw.rect(screen, colors['GREEN'], ((pos[0] * SIZE + 3, pos[1] * SIZE + 3), (SIZE - 6, SIZE - 6)))
        pygame.draw.rect(screen, colors['GREEN'], ((self.item[0][0] * SIZE, self.item[0][1] * SIZE), (SIZE, SIZE)))
        pygame.draw.rect(screen, colors['DARK_GREEN'],
                         ((self.item[0][0] * SIZE + 3, self.item[0][1] * SIZE + 3), (SIZE - 6, SIZE - 6)))

    def move(self, ate):
        if not ate:
            self.item.pop()
        head = (self.item[0][0] + self.dirt[0], self.item[0][1] + self.dirt[1])
        if head in self.item or head[0] < 0 or head[1] < 0 or head[0] >= BOARD_WIDTH or head[1] >= BOARD_HEIGHT:
            return False
        self.item.insert(0, head)
        return True

    def eat(self, food):
        if self.item[0] == food.item:
            return True
        else:
            return False


class Food(object):
    def __init__(self):
        self.item = (randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1))
        while self.item in [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2), (BOARD_WIDTH // 2 - 1, BOARD_HEIGHT // 2)]:
            self.item = (randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1))

    def draw(self, screen):
        pygame.draw.rect(screen, colors['BLUE'], ((self.item[0] * SIZE, self.item[1] * SIZE), (SIZE, SIZE)))
        pygame.draw.rect(screen, colors['RED'],
                         ((self.item[0] * SIZE + 3, self.item[1] * SIZE + 3), (SIZE - 6, SIZE - 6)))

    def update(self, screen, ate, snake):
        if ate:
            self.item = (randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1))
            while self.item in snake.item:
                self.item = (randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1))
            self.draw(screen)
        else:
            self.draw(screen)


def init_game():
    pygame.init()
    pygame.display.set_icon(pygame.image.load(app_path('image/icon.png')))
    pygame.display.set_caption('贪吃蛇')
    screen = pygame.display.set_mode((BOARD_WIDTH * SIZE, BOARD_HEIGHT * SIZE))
    return screen


def game(screen):
    menu = Menu()
    snake = Snake()
    food = Food()
    select(screen, menu)
    snake.speed -= menu.choice * 35
    update(screen)
    food.update(screen, snake.ate, snake)
    snake.draw(screen)
    pygame.display.update()
    ttl, accelerate = 2, 0
    while True:
        if accelerate:
            accelerate -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if snake.dirt == DIRT['UP']:
                        accelerate += ttl
                    elif not snake.dirt == DIRT['DOWN']:
                        snake.dirt = DIRT['UP']
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snake.dirt == DIRT['DOWN']:
                        accelerate += ttl
                    elif not snake.dirt == DIRT['UP']:
                        snake.dirt = DIRT['DOWN']
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snake.dirt == DIRT['LEFT']:
                        accelerate += ttl
                    elif not snake.dirt == DIRT['RIGHT']:
                        snake.dirt = DIRT['LEFT']
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snake.dirt == DIRT['RIGHT']:
                        accelerate += ttl
                    elif not snake.dirt == DIRT['LEFT']:
                        snake.dirt = DIRT['RIGHT']
                elif event.key == pygame.K_SPACE:
                    message_display(screen, 'PAUSE', 50, (BOARD_WIDTH * SIZE // 2, BOARD_HEIGHT * SIZE // 2),
                                    colors['WHITE'])
                    pause()
                break
        if snake.AI:
            zqr_ai(snake, food)
        update(screen)
        food.update(screen, snake.ate, snake)
        snake.draw(screen)
        message_display(screen, 'Score: %3d' % snake.score, 30,
                        (BOARD_WIDTH * SIZE // 10 * 9, BOARD_HEIGHT * SIZE // 15), colors['WHITE'])
        if not snake.move(snake.ate):
            game_over(screen, menu, snake, food)
            accelerate = 0
        if snake.eat(food):
            snake.speed += 1  # Speed Change Logic
            snake.score += 1  # Score Change Logic
            snake.ate = True
        else:
            snake.ate = False
        pygame.display.update()
        pygame.time.wait(40 if accelerate else snake.speed)


def select(screen, menu):
    background = pygame.image.load(app_path('image/bg.png'))
    title = pygame.image.load(app_path('image/title.png'))
    choice = pygame.image.load(app_path('image/choice.png'))
    decision = pygame.image.load(app_path('image/decision.png'))
    while True:
        screen.blit(background, (0, 0))
        screen.blit(title, (BOARD_WIDTH * SIZE // 2 - 150, BOARD_HEIGHT * SIZE // 2 - 180))
        screen.blit(choice, (BOARD_WIDTH * SIZE // 2 - 200, BOARD_HEIGHT * SIZE // 2))
        screen.blit(decision, (BOARD_WIDTH * SIZE // 2 - 202 + menu.choice * 115, BOARD_HEIGHT * SIZE // 2 - 5))
        message_display(screen, 'SPACE TO START/PAUSE', 20, (BOARD_WIDTH * SIZE // 2, BOARD_HEIGHT * SIZE // 8 * 7),
                        colors['WHITE'])
        message_display(screen, 'By todest', 20, (BOARD_WIDTH * SIZE - 50, BOARD_HEIGHT * SIZE - 30),
                        colors['BLACK'])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    menu.choice = (menu.choice + 3) % 4
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    menu.choice = (menu.choice + 1) % 4
        pygame.time.wait(100)


def update(screen):
    screen.fill(colors['BLACK'])
    for i in range(BOARD_WIDTH):
        pygame.draw.line(screen, colors['DARK_GRAY'], (i * SIZE, 0), (i * SIZE, BOARD_HEIGHT * SIZE))
    for i in range(BOARD_HEIGHT):
        pygame.draw.line(screen, colors['DARK_GRAY'], (0, i * SIZE), (BOARD_WIDTH * SIZE, i * SIZE))


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def game_over(screen, menu, snake, food):
    message_display(screen, 'GAME OVER', 115, (BOARD_WIDTH * SIZE // 2, BOARD_HEIGHT * SIZE // 2), colors['WHITE'])
    pause()
    snake.__init__()
    food.__init__()
    snake.speed -= menu.choice * 35


def message_display(screen, text, size, pos, color):
    font = pygame.font.SysFont('arial', size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = pos
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def app_path(file):
    if hasattr(sys, 'frozen'):
        return join(dirname(sys.path[0]), file)
    return join(dirname(__file__), file)


def zqr_ai(snack, food):
    x, y = snack.item[0]
    if y == 0:
        if x & 1:
            snack.dirt = DIRT['DOWN']
        else:
            snack.dirt = DIRT['RIGHT']
    elif y == BOARD_HEIGHT - 2:
        if x == BOARD_WIDTH - 1:
            snack.dirt = DIRT['DOWN']
        elif x & 1:
            snack.dirt = DIRT['RIGHT']
        else:
            snack.dirt = DIRT['UP']
    elif y == BOARD_HEIGHT - 1:
        if x == 0:
            snack.dirt = DIRT['UP']
        else:
            snack.dirt = DIRT['LEFT']
    else:
        if x & 1:
            snack.dirt = DIRT['DOWN']
        else:
            snack.dirt = DIRT['UP']


def main():
    screen = init_game()
    game(screen)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pygame.quit()
        sys.exit()
