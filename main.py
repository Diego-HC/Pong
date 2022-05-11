import pygame as pg
from random import choice
import sys

class Ball():
    def __init__(self, pos) -> None:
        self.pos = pos
        self.speed = [2, 2]
        self.width = self.height = 15
        self.rect = pg.Rect(self.pos[1], self.pos[0], self.width, self.height)

    def reset(self, pos):
        self.pos = pos
        self.speed = [2, 2]

    def checkWalls(self):
        if self.pos[0] + self.height >= 720:
            self.speed[0] = -self.speed[0]
        elif self.pos[0] <= 0:
            self.speed[0] = -self.speed[0]

    def checkReset(self):
        if self.pos[1] + self.width >= 1280:
            return 2
        elif self.pos[1] <= 0:
            return 1

    def checkPaddleLeft(self, paddle):
        if (self.pos[1] >= paddle.pos[1] + paddle.width - 1 and self.pos[1] <= paddle.pos[1] + paddle.width + 1) and (self.pos[0] >= paddle.pos[0] and self.pos[0] <= paddle.pos[0] + paddle.height):
            self.speed[1] = -self.speed[1] + 1
        
    def checkPaddleRight(self, paddle):
        if (self.pos[1] + self.width >= paddle.pos[1] - 1 and self.pos[1] + self.width >= paddle.pos[1] + 1) and (self.pos[0] >= paddle.pos[0] and self.pos[0] <= paddle.pos[0] + paddle.height):
            self.speed[1] = -self.speed[1] - 1

    def moveBall(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rect = pg.Rect(self.pos[1], self.pos[0], self.width, self.height)

    def drawBall(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect)
            
class Paddle():
    def __init__(self, pos, player) -> None:
        self.pos = pos
        self.player = player
        self.score = 0
        self.width = 20
        self.height = 100
        self.speed = 5
        self.rect = pg.Rect(self.pos[1], self.pos[0], self.width, self.height)

    def drawScore(self, screen):
        textScore = pg.font.SysFont('consolas', 100).render(
                        str(self.score), True, [255, 255, 255]
                    )
        textRect = textScore.get_rect()
        if self.player == 1:
            textRect.topleft = [1280/2 - 100 - textRect.width, 80]
            screen.blit(textScore, textRect)
        elif self.player == 2:
            textRect.topleft = [1280/2 + 100, 80]
            screen.blit(textScore, textRect)

    def upScore(self):
        self.score += 1

    def checkWalls(self, direction):
        if direction == 'down':
            if self.pos[0] + self.height >= 720:
                return False        
            else:
                return True
        elif direction == 'up':
            if self.pos[0] <= 0:
                return False        
            else:
                return True

    def movePaddle(self, direction):
        if direction == 'up' and self.checkWalls('up'):
            self.pos[0] -= self.speed
        elif direction == 'down' and self.checkWalls('down'):
            self.pos[0] += self.speed
        self.rect = pg.Rect(self.pos[1], self.pos[0], self.width, self.height)
        
    def drawPaddle(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect)
        
def dottedLine(screen):
    for rect in range(10):
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(1280/2 - 10, rect * 72, 20, 50))

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode([1280, 720])
    pg.display.set_caption('Pong')
    pg.display.set_icon(pg.image.load('PongIcon.jpg'))

    ball = Ball([400, choice([100 + 22, 1160-15])])
    player1 = Paddle([360, 100], 1)
    player2 = Paddle([360, 1160], 2)
    clock = pg.time.Clock()

    game = True
    started = False

    screen.fill([0, 0, 0])
    ball.drawBall(screen)
    player1.drawPaddle(screen)
    player2.drawPaddle(screen)
    dottedLine(screen)

    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            started = True

        if started:
            if keys[pg.K_UP]:
                player2.movePaddle('up')
            if keys[pg.K_DOWN]:
                player2.movePaddle('down')
            if keys[pg.K_w]:
                player1.movePaddle('up')
            if keys[pg.K_s]:
                player1.movePaddle('down')

            screen.fill([0, 0, 0])
            dottedLine(screen)
            ball.checkWalls()
            ball.checkPaddleLeft(player1)
            ball.checkPaddleRight(player2)

            if ball.checkReset() == 1:
                ball.reset([player1.pos[0] + player1.height/2, player1.pos[1] + player1.width + 3])
                player2.upScore()
                started = False
            elif ball.checkReset() == 2:
                ball.reset([player2.pos[0] + player2.height/2, player2.pos[1] - ball.width])
                player1.upScore()
                started = False

            ball.moveBall()
            ball.drawBall(screen)
            player1.drawPaddle(screen)
            player2.drawPaddle(screen)
            player1.drawScore(screen)
            player2.drawScore(screen)

        pg.display.flip()
        clock.tick(144)