from settings import *
import pygame as pg
import math

class PlayerBullet:
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.game.player.rect.centerx, self.game.player.rect.centery
        self.speed = BULLET_SPEED
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        # print(self.x, self.mouse_x, self.y, self.mouse_y)
        self.angle = math.atan2(self.y - self.mouse_y, self.x-self.mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.rect = False
        self.damage = self.game.player.damage
        self.bounce_count = 0
        self.max_bounce_count = 2

    def draw(self):
        self.rect = pg.draw.circle(self.game.screen, (0, 255, 0), (self.x, self.y), 5)

    def movement(self):
        dx, dy = 0, 0
        dx -= self.x_vel * self.game.delta_time
        dy -= self.y_vel * self.game.delta_time

        speed = self.game.player.speed * self.game.delta_time

        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.game.player_movement_y:
            dy += speed
        if keys[pg.K_s] and self.game.player_movement_y:
            dy -= speed
        if keys[pg.K_a] and self.game.player_movement_x:
            dx += speed
        if keys[pg.K_d] and self.game.player_movement_x:
            dx -= speed

        if (keys[pg.K_w] or keys[pg.K_s]) and (keys[pg.K_a] or keys[pg.K_d]) and self.game.diagonal_speed_reduction:
            speed_reduction = PLAYER_DIAGONAL_SPEED_REDUCTION
            dx /= speed_reduction
            dy /= speed_reduction

        self.check_collision(dx, dy)

    def check_collision(self, dx, dy):
        if self.rect:
            for mob in self.game.mobs:
                if pg.Rect.colliderect(self.rect, mob.rect):
                    mob.health -= self.damage
                    if  not self.game.player.pierce:
                        self.game.remove_bullet(self)

                    if mob.health <= 0:
                        self.game.remove_mob(mob)

                    break

        if self.rect != False:
            remove = False
            if self.rect.x < 0 or self.rect.x > WIDTH:
                remove = True
                if (self.game.player.bounce and self.bounce_count < self.max_bounce_count):
                    remove = False
                    self.bounce_count += 1
                    self.x_vel = -1 * self.x_vel
                    dx = -1 * dx
            if self.rect.y < 0 or self.rect.y > HEIGHT:
                remove = True
                if (self.game.player.bounce and self.bounce_count < self.max_bounce_count):
                    remove = False
                    self.bounce_count += 1
                    self.y_vel = -1 * self.y_vel
                    dy = -1 * dy


            if remove:
                self.game.remove_bullet(self)

        self.x += dx
        self.y += dy

    def update(self):
        self.movement()
        self.damage = self.game.player.damage