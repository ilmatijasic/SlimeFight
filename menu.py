from settings import *
import pygame as pg
import math
import random
import numpy as np
import sys

class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, game, text,  pos, font, bg="black", feedback=""):
        self.game = game
        self.x, self.y = pos
        # self.font = pg.font.SysFont(FONT, font)
        self.font = pg.font.SysFont(FONT, 50)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black", padding = 10):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pg.Color("White"))
        self.size = self.text.get_size()
        self.surface = pg.Surface((self.size[0] + padding, self.size[1] + padding))
        self.surface.fill(bg)
        self.surface.blit(self.text, (padding/2, padding/2))
        self.rect = pg.Rect(self.x, self.y, self.size[0] + padding, self.size[1] + padding)

    def show(self):
        self.game.screen.blit(self.surface, (self.rect))


class Menu:
    def __init__(self, game):
        self.game = game
        self.transparent_surface = pg.Surface((WIDTH,HEIGHT), pg.SRCALPHA)
        self.transparent_surface.fill((0,0,0,128))
        self.active = False
        self.levelup = False
        self.click = False
        self.random_power_up_init = True
        self.power_ups = {}
        self.message1, self.power_up1 = 0, 0
        self.message2, self.power_up2 = 0, 0
        self.message3, self.power_up3 = 0, 0
        self.init_power_ups()


    def init_power_ups(self):
        def damage_up(n = 2):
            self.game.player.damage += n

        def attack_speed_up(n = 0.1, max_as = MAX_TIME_BETWEEN_SHOTS):
            new_attack_speed = int(1000/self.game.player.time_between_shots) * (1 + n)

            self.game.player.time_between_shots = max(max_as, int(1000/new_attack_speed))
            # print(self.game.player.time_between_shots)

        def bounce():
            self.game.player.bounce = True
            self.power_ups.pop("Bounce")

        def pierce():
            self.game.player.pierce = True
            self.power_ups.pop("Pierce")

        def heal(n = 20):
            self.game.player.health = min(self.game.player.max_health, self.game.player.health + n)

        def max_health_up(n = 5):
            self.game.player.max_health += 5
            heal(5)

        self.power_ups["Damage +2"] = damage_up
        self.power_ups["Attack Speed +10%"] = attack_speed_up
        self.power_ups["Bounce"] = bounce
        self.power_ups["Pierce"] = pierce
        self.power_ups["Heal 20"] = heal
        self.power_ups["Max Health +5"] = max_health_up


    def draw(self):
        if self.game.player.health <= 0:
            self.active = True

        if self.active:
            self.game.player.draw_health_bar()
            self.game.player.draw_stats()
            for mob in self.game.mobs:
                # mob.draw_score()
                mob.draw_health_bar()
            self.game.screen.blit(self.transparent_surface, (0,0))
            if self.levelup:
                self.draw_level_up_menu()

            else:
                self.draw_menu(self.game.player.health <= 0)
            self.game.player.draw_score()

            pg.display.flip()
            self.game.delta_time = self.game.clock.tick(FPS)
            pg.display.set_caption(f'{self.game.clock.get_fps() :.1f}')

        self.click = False

    def draw_menu(self, death = False):
        message = "PAUSE"
        if death:
            message = "GAME OVER"
        # font = pg.font.Font(FONT, 50)
        font = pg.font.SysFont(FONT, 50)
        text = font.render(message, True, "white")
        textRect = text.get_rect()
        textRect.center = (HALF_WIDTH, HALF_HEIGHT/2)
        self.game.screen.blit(text, textRect)

        resume_button = Button(self.game, "Resume", (0,0), 40)
        resume_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 100)
        resume_button.show()

        restart_button = Button(self.game, "Restart", (0,0), 40)
        restart_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 175)
        restart_button.show()

        exit_button = Button(self.game, "Exit", (0,0), 40)
        exit_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 250)
        exit_button.show()

        # click = pg.mouse.get_pressed()
        if self.click:
            x, y = pg.mouse.get_pos()
            if restart_button.rect.collidepoint(x, y):
                self.game.new_game()

            if exit_button.rect.collidepoint(x, y):
                self.game.quit()

            if resume_button.rect.collidepoint(x, y):
                self.game.menu.active = False
                self.game.resume = True

    def draw_level_up_menu(self):
        message = "Level Up"
        # font = pg.font.Font(FONT, 50)
        font = pg.font.SysFont(FONT, 50)
        text = font.render(message, True, "white")
        textRect = text.get_rect()
        textRect.center = (HALF_WIDTH, HALF_HEIGHT/2)
        self.game.screen.blit(text, textRect)

        distance_between_buttons = 50

        # resume_button = Button(self.game, "Resume", (0,0), 40)
        # resume_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 100)
        # resume_button.show()
        if self.random_power_up_init:
            self.message1, self.power_up1 = random.choice(list(self.power_ups.items()))
            self.message2, self.power_up2 = random.choice(list(self.power_ups.items()))
            self.message3, self.power_up3 = random.choice(list(self.power_ups.items()))
            # print(self.message1, self.power_up1)
            # print(self.message2, self.power_up2)
            # print(self.message3, self.power_up3)
            self.random_power_up_init = False

        center_button = Button(self.game, self.message2, (0,0), 40)
        center_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 150)
        center_button.show()

        left_button = Button(self.game, self.message1, (0,0), 40)
        # print(center_button.rect.left + 30)
        left_button.rect.center = (0, HALF_HEIGHT/2 + 150)
        left_button.rect.right = center_button.rect.left - distance_between_buttons
        left_button.show()


        right_button = Button(self.game, self.message3, (0,0), 40)
        right_button.rect.center = (0, HALF_HEIGHT/2 + 150)
        right_button.rect.left = center_button.rect.right + distance_between_buttons
        right_button.show()

        exit_button = Button(self.game, "Exit", (0,0), 40)
        exit_button.rect.center = (HALF_WIDTH, HALF_HEIGHT/2 + 250)
        exit_button.show()



        if self.click:
            x, y = pg.mouse.get_pos()

            # if resume_button.rect.collidepoint(x, y):
            #     self.game.menu.active = False
            #     self.game.resume = True
            #     self.levelup = False

            if left_button.rect.collidepoint(x, y):
                self.game.menu.active = False
                self.levelup = False
                self.game.resume = True
                self.random_power_up_init = True

                self.power_up1()

            if center_button.rect.collidepoint(x, y):
                self.game.menu.active = False
                self.levelup = False
                self.game.resume = True
                self.random_power_up_init = True

                self.power_up2()

            if right_button.rect.collidepoint(x, y):
                self.game.menu.active = False
                self.levelup = False
                self.game.resume = True
                self.random_power_up_init = True

                self.power_up3()
                # print(self.game.player.damage)

            if exit_button.rect.collidepoint(x, y):
                self.game.quit()








