import pygame
import random

from pygame import draw

from settings import *
from sprites import *

class Game:
    def __init__(self):
        self.running = True
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Dev Project - Concept Demo")
        self.clock = pygame.time.Clock()
        self.hitCW = False
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.levelComplete = False
        self.death = False
        self.coinsCollected = 0
    
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.crouchWalls = pygame.sprite.Group()
        self.wallBottoms = pygame.sprite.Group()
        self.exitDoors = pygame.sprite.Group()
        self.mobLeftRight = pygame.sprite.Group()
        self.mobUpDown = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for wall in WALL_LIST:
            w = Wall(*wall)
            self.all_sprites.add(w)
            self.walls.add(w)
        for cWall in CROUCH_WALL_LIST:
            cw = CrouchWall(*cWall)
            self.all_sprites.add(cw)
            self.crouchWalls.add(cw)
        for wallBot in WALL_BOTTOM_LIST:
            wb = WallBottom(*wallBot)
            self.all_sprites.add(wb)
            self.wallBottoms.add(wb)
        for exitDoor in EXIT_DOOR_LIST:
            ed = ExitDoor(*exitDoor)
            self.all_sprites.add(ed)
            self.exitDoors.add(ed)
        for leftRight in ENEMY_LEFT_AND_RIGHT_LIST:
            lr = MobLeftRight(*leftRight)
            self.all_sprites.add(lr)
            self.mobLeftRight.add(lr)
        for upDown in ENEMY_UP_AND_DOWN_LIST:
            ud = MobUpDown(*upDown)
            self.all_sprites.add(ud)
            self.mobUpDown.add(ud)
        for coin in COIN_LIST:
            cn = Coins(*coin)
            self.all_sprites.add(cn)
            self.coins.add(cn)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 00
        
        crouchWallHits = pygame.sprite.spritecollide(self.player, self.crouchWalls, False)
        for cwHit in crouchWallHits:
            if self.player.vel.x > 0:
                if not self.player.isCrouching:
                    self.player.pos.x = cwHit.rect.left - 25
                    self.player.vel.x = 00
                    self.hitCW = True 
                elif self.player.isCrouching:
                    self.player.underWall = True
            else:
                if not self.player.isCrouching:
                    self.player.pos.x = cwHit.rect.right + 25
                    self.player.vel.x = 00
                elif self.player.isCrouching:
                    self.player.underWall = True
            
        wallHits = pygame.sprite.spritecollide(self.player, self.walls, False)
        for wallHit in wallHits:
            if self.player.vel.x > 0:
                self.player.pos.x = wallHit.rect.left - 25
                self.player.vel.x = 00
            elif not self.hitCW:
                self.player.pos.x = wallHit.rect.right + 25
                self.player.vel.x = 00

        bottomHits = pygame.sprite.spritecollide(self.player, self.wallBottoms, False)
        for botHit in bottomHits:
            self.player.vel.y = 00

        exitHits = pygame.sprite.spritecollide(self.player, self.exitDoors, False)
        for exitHit in exitHits:
            if self.playing:
                self.coinsCollected = 0
                self.playing = False
                self.levelComplete = True
        
        mobLeftRightHits = pygame.sprite.spritecollide(self.player, self.mobLeftRight, False)
        for mobLeftRightHit in mobLeftRightHits:
            if self.playing:
                self.coinsCollected = 0
                self.playing = False
                self.death = True
        
        mobUpDownHits = pygame.sprite.spritecollide(self.player, self.mobUpDown, False)
        for mobUpDownHit in mobUpDownHits:
            if self.playing:
                self.coinsCollected = 0
                self.playing = False
                self.death = True


        if not crouchWallHits:
            self.player.underWall = False
            self.hitCW = False

        coinCollection = pygame.sprite.spritecollide(self.player, self.coins, False)
        for coinCollect in coinCollection:
            self.coinsCollected = self.coinsCollected + 1
            coinCollect.kill()

        if self.player.rect.right >= 2 * WIDTH / 3.2: 
            self.player.pos.x -= max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.right -= max(abs(self.player.vel.x),2)
            for wall in self.walls:
                wall.rect.right -= max(abs(self.player.vel.x),2)
            for cWall in self.crouchWalls:
                cWall.rect.right -= max(abs(self.player.vel.x),2)
            for wallBot in self.wallBottoms:
                wallBot.rect.right -= max(abs(self.player.vel.x),2)
            for door in self.exitDoors:
                door.rect.right -= max(abs(self.player.vel.x),2)
            for coin in self.coins:
                coin.rect.right -= max(abs(self.player.vel.x), 2)
            for mobLR in self.mobLeftRight:
                mobLR.rect.right -= (max(abs(self.player.vel.x), 2))
            for mobUD in self.mobUpDown:
                mobUD.rect.right -= (max(abs(self.player.vel.x), 2))

        if self.player.rect.top >= HEIGHT * 4:
            self.playing = False
            self.death = True
            self.coinsCollected = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def draw(self):
        self.screen.fill(LIGHTCYAN)
        self.all_sprites.draw(self.screen)
        self.draw_text("Coins Collected: " + str(self.coinsCollected) + "/3", 50, WHITE, 175, 20)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Game Dev Project - Concept Demo", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use the arrow keys to move, space to jump, and down on the arrow keys to crouch.", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to continue.", 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def show_win_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("LEVEL COMPLETE!", 64, GREEN, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        pygame.time.wait(1250)

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 64, RED, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        pygame.time.wait(1250)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    if game.levelComplete == True:
        game.show_win_screen()
        game.levelComplete = False
    if game.death == True:
        game.show_go_screen()
        game.death = False
