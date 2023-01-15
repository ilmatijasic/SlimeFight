from settings import *
import pygame as pg
import math
from player import Player
import random


class Mob(Player):

    def __init__(self, x, y, game, score = 5):
        super().__init__(x, y, game, scale = SLIME_SIZE_SCALE, path = "Assets/mobs/slime_animation_{}.png", health=SLIME_MAX_HEALTH, max_health = SLIME_MAX_HEALTH)
        # self.scale_image = lambda image: pg.transform.scale(image, (image.get_width()*self.scale, image.get_height()*self.scale))
        # self.object_walk_img = [self.scale_image(pg.image.load()) for i in range(4)]
        self.speed = SLIME_SPEED
        self.animation_speed = SLIME_ANIMATION_SPEED

        self.offset_reset = SLIME_OFFSET_RESET
        self.offset_reset_time = random.randrange(self.offset_reset, self.offset_reset+30)

        self.offset = SLIME_OFFSET
        self.offset_x = random.randrange(-self.offset, self.offset)
        self.offset_y = random.randrange(-self.offset, self.offset)
        # print("Mob:", self.current_img)

        self.angle = 0
        self.x_vel = 0
        self.y_vel = 0

        self.distance_from_player = 0

        self.damage = SLIME_DAMAGE

        self.health_bar_padding = PLAYER_HEALTH_BAR_PADDING
        # self.health_bar_x = PLAYER_HEALTH_BAR_X,
        # self.health_bar_y = PLAYER_HEALTH_BAR_Y,
        # self.health_bar_width = PLAYER_HEALTH_BAR_WIDTH,
        # self.health_bar_height = PLAYER_HEALTH_BAR_HEIGHT,
        self.rect = self.current_img.get_rect()
        self.rect.move_ip(self.x, self.y)

        self.score = score





    def draw_health_bar(self):
        pad = self.health_bar_padding
        health_bar_x = self.rect.x - self.rect.width/2
        health_bar_y = self.rect.y - 30
        health_bar_width = self.rect.width*2
        health_bar_height = 20

        pg.draw.rect(self.game.screen, (255, 255, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), width=1)
        pg.draw.rect(self.game.screen, (255, 0, 0), (health_bar_x + pad,
                                                     health_bar_y + pad,
                                                     (self.health/self.max_health)*(health_bar_width - 2*pad),
                                                     health_bar_height - 2*pad))

    @staticmethod
    def euclidian_distance(x, y):
        return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

    def calculate_speed_math(self, offset):
        self.angle = math.atan2(self.game.player.y - self.y, self.game.player.x - self.x)
        if offset:
            self.angle = math.atan2(self.game.player.y - self.y + self.offset_y, self.game.player.x - self.x + self.offset_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def calculate_speed_dumb(self, offset):
        speed = self.speed * self.game.delta_time
        offset = int(offset)


        left = self.game.player.x + offset*self.offset_x < self.x
        right = self.game.player.x + offset*self.offset_x > self.x

        up = self.game.player.y + offset*self.offset_y < self.y
        down = self.game.player.y + offset*self.offset_y > self.y

        self.x_vel = int(left or right) * (-1)**int(left) * speed
        self.y_vel = int(up or down) * (-1)**int(up) * speed

        # print(speed, self.x_vel, self.y_vel)



    def mob_movement(self):
        if self.offset_reset_time == 0:
            self.offset_x = random.randrange(-self.offset, self.offset)
            self.offset_y = random.randrange(-self.offset, self.offset)
            self.offset_reset_time = random.randrange(self.offset_reset, self.offset_reset+30)

        self.distance_from_player = self.euclidian_distance((self.game.player.x, self.game.player.y), (self.x, self.y))

        dx, dy = 0, 0

        # self.calculate_speed_math(self.distance_from_player > math.sqrt(2)*self.offset)
        self.calculate_speed_dumb(self.distance_from_player > math.sqrt(2)*self.offset)

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        if self.x_vel > 1e-3:
            self.moving_right = True
        elif self.x_vel < -1e-3:
            self.moving_left = True

        if self.y_vel > 1e-3:
            self.moveing_down = True
        elif self.y_vel < -1e-3:
            self.moving_up = True


        dx += self.x_vel
        dy += self.y_vel

        self.offset_reset_time -= 1

        return dx, dy

    def player_movement(self):
        dx, dy = 0, 0
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


        dx_mob, dy_mob = self.mob_movement()

        self.check_collision(dx + dx_mob, dy + dy_mob)

    def check_collision(self, dx, dy):

        self.rect = self.rect.move(dx, 0)

        if self.rect.left < self.game.map.map_rect.left:
            self.rect.left = self.game.map.map_rect.left
        elif self.rect.right > self.game.map.map_rect.right:
            self.rect.right = self.game.map.map_rect.right
        factor = 1
        for mob in self.game.mobs:
            if pg.Rect.colliderect(self.rect, mob.rect) and (mob.rect is not self.rect):
                if dx > 0:
                    self.rect.right = mob.rect.left
                else:
                    self.rect.left = mob.rect.right
                # mob.temp_dx = dx*factor
                mob.check_collision(dx*factor, 0)

        self.rect = self.rect.move(0, dy)

        if self.rect.top < self.game.map.map_rect.top:
            self.rect.top = self.game.map.map_rect.top
        elif self.rect.bottom > self.game.map.map_rect.bottom:
            self.rect.bottom = self.game.map.map_rect.bottom

        for mob in self.game.mobs:
            if pg.Rect.colliderect(self.rect, mob.rect) and (mob.rect is not self.rect):
                # rect = self.rect.move(0, dy)
                if dy > 0:
                    self.rect.bottom = mob.rect.top
                else:
                    self.rect.top = mob.rect.bottom
                # mob.temp_dy = dy*factor
                mob.check_collision(0, dy*factor)


        # self.rect = self.rect.move(dx,dy)

        if pg.Rect.colliderect(self.rect, self.game.player.rect):
            if self.game.player.health > 0:
                self.game.player.health -= self.damage




        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.draw_health_bar()
        self.player_movement()
        if self.health <= 0:
            self.game.remove_mob(self)
