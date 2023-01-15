from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, x, y, game,
                 scale = PLAYER_SIZE_SCALE,
                 path ="Assets/player/player_walk_{}.png",
                 max_health = PLAYER_MAX_HEALTH,
                 health = PLAYER_MAX_HEALTH):
        self.x = x
        self.y = y

        self.game = game

        self.animation_count = 0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.orientation_left = False
        self.animation_speed = PLAYER_ANIMATION_SPEED

        self.scale = scale

        self.path = path
        self.scale_image = lambda image: pg.transform.scale(image, (image.get_width()*self.scale, image.get_height()*self.scale))
        self.object_walk_img = [self.scale_image(pg.image.load(self.path.format(i))) for i in range(4)]
        self.current_img = self.object_walk_img[0]

        # print("Player:", self.current_img)
        self.rect = self.current_img.get_rect()
        self.rect.move_ip(self.x, self.y)

        self.max_health = max_health
        self.health = health

        self.health_bar_padding = PLAYER_HEALTH_BAR_PADDING
        self.health_bar_x = PLAYER_HEALTH_BAR_X
        self.health_bar_y = PLAYER_HEALTH_BAR_Y
        self.health_bar_width = PLAYER_HEALTH_BAR_WIDTH
        self.health_bar_height = PLAYER_HEALTH_BAR_HEIGHT
        self.speed = PLAYER_SPEED

        self.stats_x = PLAYER_STATS_X
        self.stats_y = PLAYER_STATS_Y
        self.stats_width = PLAYER_STATS_WIDTH
        self.stats_height = PLAYER_STATS_HEIGHT

        self.score = 0
        self.lvl = 1
        self.damage = BULLET_DAMAGE
        self.time_between_shots = TIME_BETWEEN_SHOTS
        self.pierce = False
        self.bounce = False





    def animation(self):
        moving = self.moving_left or self.moving_right or self.moving_up or self.moving_down
        index = int(moving) * int(self.animation_count * self.animation_speed) % 4
        image = self.object_walk_img[index]

        if self.orientation_left:
            self.current_img = pg.transform.flip(image, True, False)
            return
        self.current_img = image



    def draw(self):
        if not self.game.menu.active:
            self.animation()

        self.game.screen.blit(self.current_img, (self.x, self.y))

        self.animation_count += 1

        # pg.draw.rect(self.game.screen, (255, 0, 0), (self.rect), width=1)

    def draw_health_bar(self):
        pad = self.health_bar_padding
        pg.draw.rect(self.game.screen, (255, 255, 0), (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height), width=1)
        pg.draw.rect(self.game.screen, (255, 0, 0), (self.health_bar_x + pad,
                                                     self.health_bar_y + pad,
                                                     (self.health/self.max_health)*(self.health_bar_width - 2*pad),
                                                     self.health_bar_height - 2*pad))

    def draw_score(self):
        # font = pg.font.Font(FONT, 20)
        font = pg.font.SysFont(FONT, FONT_SIZE)
        text = font.render('Score: ' + str(self.score), True, "white")
        textRect = text.get_rect()
        textRect.move_ip(50, 50)
        self.game.screen.blit(text, textRect)

    def draw_stats(self):
        self.transparent_surface = pg.Surface((self.stats_width - 2,self.stats_height - 2), pg.SRCALPHA)
        self.transparent_surface.fill((0,0,0,128))
        pg.draw.rect(self.game.screen, (255, 255, 0), (self.stats_x, self.stats_y, self.stats_width, self.stats_height), width=1)
        self.game.screen.blit(self.transparent_surface, (self.stats_x + 1, self.stats_y + 1))

        space_between_text = 15

        # font = pg.font.Font(FONT, 20)
        font = pg.font.SysFont(FONT, FONT_SIZE)
        damageText = font.render('Damage: ' + str(self.damage), True, "white")
        damageRect = damageText.get_rect()
        damageRect.move_ip(self.stats_x + 10, self.stats_y + space_between_text)
        self.game.screen.blit(damageText, damageRect)

        asText = font.render('Attack speed: ' + f"{int(1000/self.time_between_shots)}", True, "white")
        asRect = asText.get_rect()
        asRect.move_ip(self.stats_x + 10, damageRect.bottom + space_between_text)
        self.game.screen.blit(asText, asRect)

        maxHealthText = font.render('Max Health: ' + f"{self.max_health}", True, "white")
        maxHealthRect = maxHealthText.get_rect()
        maxHealthRect.move_ip(self.stats_x + 10, asRect.bottom + space_between_text)
        self.game.screen.blit(maxHealthText, maxHealthRect)

        bounceText = font.render('Bounce: ' + f"{self.bounce}", True, "white")
        bounceRect = bounceText.get_rect()
        bounceRect.move_ip(self.stats_x + 10, maxHealthRect.bottom + space_between_text)
        self.game.screen.blit(bounceText, bounceRect)

        pierceText = font.render('Pierce: ' + f"{self.pierce}", True, "white")
        pierceRect = pierceText.get_rect()
        pierceRect.move_ip(self.stats_x + 10, bounceRect.bottom + space_between_text)
        self.game.screen.blit(pierceText, pierceRect)

    def player_movement(self):

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.moving_up = True

        if keys[pg.K_s]:
            self.moving_down = True

        if keys[pg.K_a]:
            self.moving_left = True
            self.orientation_left = True

        if keys[pg.K_d]:
            self.moving_right = True
            self.orientation_left = False

    def level_up(self):
        self.game.menu.active = True
        self.game.menu.levelup = True
        # self.damage += 5
        # self.time_between_shots = max(TIME_BETWEEN_SHOTS//2, int(self.time_between_shots*0.75))
        self.lvl += 1

    def update(self):
        while self.lvl < self.score // 10 + 1:
            # print("level up")
            # self.speed += 5
            self.level_up()

        self.draw_health_bar()
        self.draw_score()
        self.draw_stats()
        self.player_movement()



