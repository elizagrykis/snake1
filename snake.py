
# SPACE SNAKE


import random
import pygame
import gui


class Screen(object):
    lines = 20
    a = 400

    def __init__(self, start, dirnx=1, dirny=0, color=(141, 237, 252)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.a // self.lines
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:                                                              # określenie pozycji kwadratu
            centre = dis // 2
            radius = 3
            CircleMiddle = (i * dis + centre - radius, j * dis + 8)
            CircleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), CircleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), CircleMiddle2, radius)


class Snake(object):
    body = []       # ustawienie ci ała węża jako
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Screen(pos)
        self.body.append(self.head) # cdodanie glowy węża
        self.dirnx = 0
        self.dirny = 1  # kierunek poruszania się węża

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # sprawdzenie zderzenia
                pygame.quit()

            keys = pygame.key.get_pressed() # sprawdzenie naciskanych klawiszy

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    print('Score: ', len(s.body))
                    s.reset((10, 10))
                    break
                elif c.dirnx == 1 and c.pos[0] >= c.lines - 1:
                    print('Score: ', len(s.body))
                    s.reset((10, 10))
                    break
                elif c.dirny == 1 and c.pos[1] >= c.lines - 1:
                    print('Score: ', len(s.body))
                    s.reset((10, 10))
                    break
                elif c.dirny == -1 and c.pos[1] <= 0:
                    print('Score: ', len(s.body))
                    s.reset((10, 10))
                    break
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        pygame.quit()
        quit()

    def addScreen(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Screen((tail.pos[0] - 1, tail.pos[1]))) # ustalenie po jakiej stronie ma zostac dodana kostka
        elif dx == -1 and dy == 0:
            self.body.append(Screen((tail.pos[0] + 1, tail.pos[1]))) # ustalenie kierunku poruszania, aby dodać kostkę
        elif dx == 0 and dy == 1:
            self.body.append(Screen((tail.pos[0], tail.pos[1] - 1))) #
        elif dx == 0 and dy == -1:
            self.body.append(Screen((tail.pos[0], tail.pos[1] + 1))) #

        self.body[-1].dirnx = dx   # ustawienie kieruneku kostek na kierunek węża.
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:                      # rysowanie oczu
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(a, lines, surface):
    sizeBtwn = a // lines

    x = 0
    y = 0
    for l in range(lines):
        x = x + sizeBtwn
        y = y + sizeBtwn


def redrawWindow(surface):
    global lines, width, s, snack # dodanie przekąski do danej lini
    my_image = pygame.image.load('kosmos_snake.jpeg') #dodanie grafiki jako tło do gry
    surface.blit(my_image, (0, 0))
    s.draw(surface)
    snack.draw(surface)
    pygame.display.flip()


def randomSnack(lines, item):
    positions = item.body

    while True: # generowanie nowych prawidłowych pozycji
        x = random.randrange(lines)
        y = random.randrange(lines)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0: # sprawdzenie czy pozycja jest zajęta przez węża
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = gui.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    try:
        root.destroy()
    except:
        pass


def main():
    global width, lines, s, snack
    width = 400
    lines = 20
    win = pygame.display.set_mode((width, width)) # tworzenie ekranu

    s = Snake((255, 0, 0), (10, 10)) # stworzenie wężą
    snack = Screen(randomSnack(lines, s), color=(205, 50, 252))
    flag = True
    # screen = pygame.display.set_mode((1200, 1000))

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        s.move()
        if s.body[0].pos == snack.pos: # sprawdzenie czy głowa zderza się z jedzonkiem
            s.addScreen() # dodanie nowej kostki do węża
            snack = Screen(randomSnack(lines, s), color=(205, 50, 252)) # tworzenie nowego jedzonka
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])): ## Sprawdzenie czy ciała się pokrywają
                print('Score: ', len(s.body))
                s.reset((10, 10))
                break

        redrawWindow(win)


main()
