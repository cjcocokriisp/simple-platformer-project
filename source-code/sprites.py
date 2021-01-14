import pygame
from settings import *
import random

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((50, 50))   
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(230, 660)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.isCrouching = False
        self.underWall = False

    def jump(self):
        if not self.underWall:
            self.rect.x += 1
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 1
            if hits:
                self.vel.y = -20

    def crouch(self): 
        self.isCrouching = True
        if self.isCrouching:
            self.image = pygame.Surface((50, 25))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.acc.x = -PLAYER_ACC / 2
            if keys[pygame.K_RIGHT]:
                self.acc.x = PLAYER_ACC / 2

    def getUp(self):
        if not self.underWall:
            self.image = pygame.Surface((50, 50))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.isCrouching = False

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
                self.acc.x = PLAYER_ACC
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LEFT]:
            if not self.isCrouching:
                self.acc.x = -PLAYER_ACC * 3
        if keys[pygame.K_LSHIFT] and keys[pygame.K_RIGHT]:
            if not self.isCrouching:
                self.acc.x = PLAYER_ACC * 3
        if keys[pygame.K_DOWN]:
            self.crouch()
        else:
            self.getUp()

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x < 0:
            self.pos.x = 0


        self.rect.midbottom = self.pos


class MobLeftRight(pygame.sprite.Sprite):
    def __init__(self, x, y, area):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 6
        self.direction = 1
        self.moveCounter = 0
        self.moveLimitLeft = area
        self.moveLimitRight = area

    def update(self):
        
        if self.moveCounter == self.moveLimitLeft and self.direction == 1:
            self.moveCounter = 0 
            self.direction = 2

        if self.moveCounter == self.moveLimitRight and self.direction == 2:
            self.moveCounter = 0
            self.direction = 1

        if self.direction == 1:
            self.rect.x -= self.vx
            self.moveCounter += 1
        elif self.direction == 2:
            self.rect.x += self.vx
            self.moveCounter += 1

class MobUpDown(pygame.sprite.Sprite):
    def __init__(self, x, y, area):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = 6
        self.direction = 1
        self.moveCounter = 0
        self.moveLimitUp = area
        self.moveLimitDown = area

    def update(self):

        if self.moveCounter == self.moveLimitUp and self.direction == 1:
            self.moveCounter = 0 
            self.direction = 2

        if self.moveCounter == self.moveLimitDown and self.direction == 2:
            self.moveCounter = 0
            self.direction = 1

        if self.direction == 1:
            self.rect.y -= self.vy
            self.moveCounter += 1
        elif self.direction == 2:
            self.rect.y += self.vy
            self.moveCounter += 1


        
        
class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Walls that can be crouched under
class CrouchWall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class WallBottom(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ExitDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
