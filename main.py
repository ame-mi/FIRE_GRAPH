import numpy as np
import pygame
import sys
import random

EMPTY = 0
FIRE = 1
EXT = 2
PLYR = 3
WALL = 5


class class_FIRE:
    def __init__(self, grid) -> None:
        (
            self.grid) = grid

    def Spread(self, grid) -> None:
        New_Fire = []
        for y in range(1, grid.shape[0] - 1):
            for x in range(1, grid.shape[1] - 1):
                if grid[y, x] == FIRE:
                    for dx, dy in routes:
                        nx, ny = x + dx, y + dy
                        if grid[ny, nx] == EMPTY and random.random() < 0.06:
                            New_Fire.append((nx, ny))
        for x, y in New_Fire:
            grid[y, x] = FIRE
        return grid


routes = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def grph(grid, strt):
    lines, clm = grid.shape
    last = set()
    queue = [strt]
    par = {}
    sx, sy = strt

    while queue:
        x, y = queue.pop(0)
        if grid[y, x] == EXT:
            Plan_route = []
            while (x, y) != (sx, sy):
                Plan_route.append((x, y))
                x, y = par[(x, y)]
            Plan_route.reverse()
            return Plan_route

        for dx, dy in routes:
            nx, ny = x + dx, y + dy
            if (0 <= nx < clm and 0 <= ny < lines and grid[ny, nx] != WALL and grid[ny, nx] != FIRE and (
                    nx, ny) not in last):
                last.add((nx, ny))
                queue.append((nx, ny))
                par[(nx, ny)] = (x, y)
    return []


def GenLab(lines, clm):
    labirint = np.full((lines * 2 + 1, clm * 2 + 1), WALL)

    def Ri(x, y):
        labirint[y][x] = EMPTY
        Route_To = routes.copy()
        random.shuffle(Route_To)
        for dx, dy in Route_To:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < clm * 2 + 1 and 0 <= ny < lines * 2 + 1 and labirint[ny][nx] == WALL:
                labirint[y + dy][x + dx] = EMPTY
                Ri(nx, ny)

    Ri(1, 1)

    labirint[lines * 2 - 1][clm * 2 - 1] = EXT

    for _ in range(lines):
        x, y = random.randint(1, clm * 2 - 1), random.randint(1, lines * 2 - 1)
        if labirint[y, x] == EMPTY:
            labirint[y, x] = FIRE

    return labirint


# def Spread_FIRE(grid):
#     New_Fire = []
#     for y in range(1, grid.shape[0] - 1):
#         for x in range(1, grid.shape[1] - 1):
#             if grid[y, x] == FIRE:
#                 for dx, dy in routes:
#                     nx, ny = x + dx, y + dy
#                     if grid[ny, nx] == EMPTY and random.random() < 0.06:
#                         New_Fire.append((nx, ny))
#     for x, y in New_Fire:
#         grid[y, x] = FIRE


def Viz_Get_Out(grid):
    Plan_route = []
    Prog_Alive = True
    Plyr_grid = False
    Route_length = 0
    Wait_step = 5
    Points = 0
    pygame.init()
    pygame.font.init()
    shrift = pygame.font.SysFont('Pixeloid Sans', 24)
    Table_size = 20
    lines, clm = grid.shape
    screen_pg = pygame.display.set_mode((clm * Table_size, lines * Table_size))
    clock_pg = pygame.time.Clock()

    # Загрузка изобр
    img_plyr = pygame.image.load('photo1.png')
    img_ext = pygame.image.load('photo2.png')
    img_fire = pygame.image.load('photo3.png')
    img_tree = pygame.image.load('photo4.png')
    img_tree = pygame.transform.scale(img_tree, (Table_size, Table_size))
    img_plyr = pygame.transform.scale(img_plyr, (Table_size, Table_size))
    img_ext = pygame.transform.scale(img_ext, (Table_size, Table_size))
    img_fire = pygame.transform.scale(img_fire, (Table_size, Table_size))

    colours_pg = {
        EMPTY: (255, 255, 255),
        WALL: (128, 128, 128)
    }

    Plan_route = []
    Prog_Alive = True
    Plyr_grid = False
    Route_length = 0
    Wait_step = 5
    no_exit_message = False
    message_timer = 0

    while Prog_Alive:
        for ivent_pg in pygame.event.get():
            if ivent_pg.type == pygame.QUIT:
                Prog_Alive = False

            elif ivent_pg.type == pygame.MOUSEBUTTONDOWN and not Plyr_grid:
                mysh_x, mysh_y = pygame.mouse.get_pos()
                grid_x, grid_y = mysh_x // Table_size, mysh_y // Table_size

                if grid[grid_y][grid_x] == EMPTY:
                    grid[grid_y][grid_x] = PLYR
                    start_xy = (grid_x, grid_y)
                    Plan_route = grph(grid, start_xy)

                    if not Plan_route:
                        no_exit_message = True
                        message_timer = 60  # Показывать сообщение 60 кадров
                    else:
                        Points = len(Plan_route)
                        Plyr_grid = True

            elif ivent_pg.type == pygame.KEYDOWN and ivent_pg.key == pygame.K_SPACE and Plyr_grid:
                Plan_route = grph(grid, start_xy)

        if Plan_route:
            Route_length += 1
            if Route_length >= Wait_step:
                Route_length = 0
                x, y = Plan_route.pop(0)

                if start_xy != (x, y):
                    px, py = start_xy
                    grid[py][px] = EMPTY  # Удалить игрока с предыдущей клетки
                start_xy = (x, y)
                if grid[y][x] == FIRE:
                    Points = 0
                    Prog_Alive = False
                    continue

                if grid[y][x] == EXT:
                    Points += 1
                    grid[y][x] = PLYR
                    Prog_Alive = False
                else:
                    grid[y][x] = PLYR

        screen_pg.fill((0, 0, 0))
        for r in range(lines):
            for c in range(clm):
                if grid[r, c] == WALL:
                    screen_pg.blit(img_tree, (c * Table_size, r * Table_size))
                elif grid[r, c] == EMPTY:
                    pygame.draw.rect(screen_pg, colours_pg[EMPTY],
                                     (c * Table_size, r * Table_size, Table_size, Table_size))
                elif grid[r, c] == PLYR:
                    screen_pg.blit(img_plyr, (c * Table_size, r * Table_size))
                elif grid[r, c] == EXT:
                    screen_pg.blit(img_ext, (c * Table_size, r * Table_size))
                elif grid[r, c] == FIRE:
                    screen_pg.blit(img_fire, (c * Table_size, r * Table_size))

        if Plyr_grid:
            Fiire = class_FIRE(grid)
            Fiire.Spread(grid)

        # Отображение сообщения об отсутствии выхода
        if no_exit_message and message_timer > 0:
            message = shrift.render("Выхода нет! Попробуйте другое место", True, (255, 0, 0))
            message_rect = message.get_rect(center=(screen_pg.get_width() // 2, 30))
            screen_pg.blit(message, message_rect)
            message_timer -= 1
            if message_timer <= 0:
                no_exit_message = False
                grid[grid_y][grid_x] = EMPTY  # Убираем персонажа, если выхода нет

        tekst = shrift.render(f'Очки: {Points}', True, (255, 255, 255))
        screen_pg.blit(tekst, (2, 2))

        pygame.display.flip()
        clock_pg.tick(10)

    pygame.quit()
    end_pg(Points)
    sys.exit()


def start_sc_pg():
    pygame.init()
    pygame.font.init()
    height, length = 600, 400
    screen_pg = pygame.display.set_mode((height, length))
    pygame.display.set_caption("Эвакуация из лабиринта")
    clock_pg = pygame.time.Clock()
    shrift = pygame.font.SysFont('Pixeloid Sans', 28)
    small_font = pygame.font.SysFont('Pixeloid Sans', 20)
    play_button = pygame.Rect(height // 2 - 90, length // 2 + 60, 160, 50)

    while True:
        screen_pg.fill((91, 64, 42))
        caption = shrift.render("Эвакуация из лабиринта", True, (255, 255, 255))
        rules = [
            "1. Кликните по пустой клетке, чтобы разместить человека.",
            "2. Персонаж найнет двигаться после размещения, если есть путь.",
            "3. Избегайте огня. Цель — добраться до выхода.",
            "4. Огонь начинает двигаться после размещения человека.",
            "5. Чем дальше персонаж от выхода, тем больше очков."
        ]

        screen_pg.blit(caption, (height // 2 - caption.get_width() // 2, 40))
        for i, stroka in enumerate(rules):
            tekst = small_font.render(stroka, True, (200, 200, 200))
            screen_pg.blit(tekst, (60, 90 + i * 30))

        pygame.draw.rect(screen_pg, (143, 201, 103), play_button)
        button_text = shrift.render("Играть", True, (255, 255, 255))
        screen_pg.blit(button_text, (play_button.x + 45, play_button.y + 15))

        for ivent_pg in pygame.event.get():
            if ivent_pg.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ivent_pg.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(pygame.mouse.get_pos()):
                    return

        pygame.display.flip()
        clock_pg.tick(60)


def end_pg(Points):
    pygame.init()
    screen_pg = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Игра окончена")
    shrift = pygame.font.SysFont('Pixeloid Sans', 36)
    small_font = pygame.font.SysFont('Pixeloid Sans', 24)
    clock_pg = pygame.time.Clock()

    button_again = pygame.Rect(60, 200, 130, 50)
    button_ext = pygame.Rect(210, 200, 130, 50)

    while True:
        screen_pg.fill((91, 64, 42))
        tekst1 = shrift.render("Игра окончена", True, (255, 255, 255))
        tekst2 = small_font.render(f"Очки: {Points}", True, (61, 107, 255))

        screen_pg.blit(tekst1, (200 - tekst1.get_width() // 2, 60))
        screen_pg.blit(tekst2, (200 - tekst2.get_width() // 2, 120))

        pygame.draw.rect(screen_pg, (143, 201, 103), button_again)
        button_text_snova = small_font.render("Сыграть снова", True, (255, 255, 255))
        screen_pg.blit(button_text_snova, (button_again.x + 5, button_again.y + 15))

        pygame.draw.rect(screen_pg, (143, 201, 103), button_ext)
        button_text_ext = small_font.render("Выйти", True, (255, 255, 255))
        screen_pg.blit(button_text_ext, (button_ext.x + 35, button_ext.y + 15))

        for ivent_pg in pygame.event.get():
            if ivent_pg.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ivent_pg.type == pygame.MOUSEBUTTONDOWN:
                if button_again.collidepoint(pygame.mouse.get_pos()):

                    lines, clm = 10, 10
                    Grid_GRPH = GenLab(lines, clm)
                    pygame.mixer.music.load("music.mp3")
                    pygame.mixer.music.play(-1)
                    Viz_Get_Out(Grid_GRPH)
                    return
                elif button_ext.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock_pg.tick(30)


start_sc_pg()
lines, clm = 10, 10
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
Grid_GRPH = GenLab(lines, clm)
Viz_Get_Out(Grid_GRPH)