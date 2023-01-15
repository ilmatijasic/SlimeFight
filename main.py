import pygame as pg
import os, sys
sys.path.insert(0, os.path.abspath(".."))
from settings import *
from player import Player
from mob import Mob
from player_bullet import PlayerBullet
from map import Map
from menu import Menu
import random



class Game:
    def __init__(self):
        pg.init()
        # pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW       )
        # pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.width, self.height = WIDTH, HEIGHT
        self.clock = pg.time.Clock()
        # pg.time.set_timer(self.global_event, 250)
        self.new_game()

    def remove_bullet(self, bullet):
        if bullet not in self.dead_bullets and bullet in self.bullets:
            self.dead_bullets.append(bullet)

    def remove_mob(self, mob):
        if mob not in self.dead_mobs and mob in self.mobs:
            self.dead_mobs.append(mob)

    def new_game(self):
        self.delta_time = 1
        self.resume = False
        self.reloaded = True
        self.global_event = pg.USEREVENT + 0
        self.mobs = []
        self.bullets = []
        self.dead_bullets = []
        self.dead_mobs = []
        self.timer = 0
        self.mouse_down = False
        self.diagonal_speed_reduction = True

        self.max_mobs = MAX_MOBS
        self.player_movement_x = True
        self.player_movement_y = True
        self.player = Player(*INIT_PLAYER_POS, self)
        self.spawn_mob()
        self.spawn_mob()
        self.spawn_mob()
        self.map = Map(self)
        self.menu = Menu(self)

    def update(self):

        self.player.update()
        self.map.update()
        for mob in self.mobs:
            mob.update()

        for bullet in self.bullets:
            bullet.update()


        for bullet in self.dead_bullets:
            self.bullets.remove(bullet)
        self.dead_bullets = []

        for mob in self.dead_mobs:
            self.player.score += mob.score
            self.mobs.remove(mob)
        self.dead_mobs = []

        spawn = random.randrange(1, 90)

        if spawn == 1 and len(self.mobs) < self.max_mobs:
            self.spawn_mob()



        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        # print(self.delta_time)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def spawn_mob(self):
        spawn_side = random.randrange(0, 3)
        if spawn_side == 0:     # left
            spawn_x = 200
            spawn_y = random.randrange(200, self.height - 200)
        if spawn_side == 1:     # top
            spawn_x = random.randrange(200, self.width) - 200
            spawn_y = 200
        if spawn_side == 2:     # right
            spawn_x = self.width - 200
            spawn_y = random.randrange(200, self.height - 200)
        if spawn_side == 3:     # bottom
            spawn_x = random.randrange(200, self.width) - 200
            spawn_y = self.height - 200
        self.mobs.append(Mob(spawn_x, spawn_y, self))

    def draw(self):
        self.screen.fill('black')
        # print(self.menu.active)

        # self.object_renderer.draw()
        # self.weapon.draw()
        self.map.draw()
        self.player.draw()

        for mob in self.mobs:
            mob.draw()

        for bullet in self.bullets:
            bullet.draw()

        self.menu.draw()




    def check_events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == self.global_event:
                self.reloaded = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self.player.health > 0:
                self.menu.active = not self.menu.active
                if self.menu.levelup:
                    self.menu.levelup = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.mouse_down:
                self.menu.click = True
                self.mouse_down = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse_down = False

        click = pg.mouse.get_pressed()

        if self.resume and not click[0]:
            self.resume = False
            return

        if click[0] and self.reloaded and not self.menu.active and not self.resume:
            self.reloaded = False
            self.bullets.append(PlayerBullet(self))
            pg.time.set_timer(self.global_event, self.player.time_between_shots)



    def run(self):
        while True:
            self.check_events()
            if not self.menu.active:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()