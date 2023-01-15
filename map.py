from settings import *
import pygame as pg
import math
import random
import numpy as np



class Tileset:
    def __init__(self, file, size=(32, 32), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pg.image.load(file)

        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()


    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pg.Surface(self.size)
                tile.blit(self.image, (0, 0), (y, x, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


class SideBool:
    def __init__(self):
        self.top = False
        self.bottom = False
        self.left =  False
        self.right = False


class MapBlock:
    def __init__(self, rect, game):
        self.top = False
        self.bottom = False
        self.left =  False
        self.right = False
        self.rect = rect
        self.game = game

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        sides = SideBool()

        if self.rect.bottom < self.player.y and not self.top:
            sides.top = True
        if self.rect.top > self.player.y and not self.bottom:
            sides.bottom = True
        if self.rect.left > self.player.x and not self.right:
            sides.right = True
        if self.rect.right < self.player.x and not self.left:
            sides.left = True

        return sides

    def change_sides(self, sides):
        self.top = sides.top
        self.bottom = sides.bottom
        self.left =  sides.left
        self.right = sides.right

    def __str__(self) -> str:
        return f"top: {self.top}, bottom: {self.bottom}, left: {self.left}, right: {self.right}"


class Wall:
    def __init__(self, game):
        self.game = game
        self.size = (8, 8)
        self.tileset = Tileset(MAP_WALL_PATH, size = (8,8))
        self.wall = pg.Surface((8*12, 8*1))
        # print(self.map.map_rect.bottom, self.map.map_rect.left)
        self.wall_rect = pg.Rect(0, 0, 8*12, 8*1)
        self.sidewall = pg.Surface((8, 8*12))
        self.sidewall_rect = pg.Rect(0, 0, 8, 8*12)
        self.tilemap = []
        self.init_bottom_wall()
        self.init_sidewall()

    def init_bottom_wall(self):
        # 36 - 43
        start = (36+12, 4)
        size = (12, 1)
        for i in range(size[1]):
            temp_list = []
            for j in range(size[0]):
                tile = self.tileset.tiles[(j+start[0])+64*(i + start[1])]
                rect = pg.Rect(j*8,i*8, 8, 8)
                self.wall.blit(tile, rect)
                temp_list.append((tile, rect))
            self.tilemap.append(temp_list)

    def init_sidewall(self):
        # 36 - 43
        start = (36, 4)
        size = (1, 12)
        for i in range(size[1]):
            temp_list = []
            for j in range(size[0]):
                tile = self.tileset.tiles[(j+start[0])+64*(i + start[1])]
                rect = pg.Rect(j*8,i*8, 8, 8)
                self.sidewall.blit(tile, rect)
                temp_list.append((tile, rect))
            self.tilemap.append(temp_list)

    def draw(self):
        self.game.screen.blit(self.wall, self.wall_rect)
        self.game.screen.blit(self.sidewall, self.sidewall_rect)

    def draw_wall_tileset(self):
        for i in range(64):
            for j in range(13):
                self.game.screen.blit(self.tileset.tiles[j+64*i], (j*9+300, i*9+300))
        # for i in range(16):
        #     for j in range(16):
        #         self.game.screen.blit(self.wall_tileset.tiles[j+16*i], (j*32+300, i*32+300))


class Map:
    def __init__(self, game):
        self.game = game
        self.tileset = Tileset(MAP_PATH)
        self.objects = []
        self.wall = Wall(game)
        self.size = 2*self.game.width//32, 2*self.game.height//32
        # print(32 * self.size[0], 32 * self.size[1])
        self.tilemap_index = np.random.randint(44, size=self.size)
        self.tilemap = []
        self.grass_size = self.game.player.rect.left - self.wall.size[0], self.game.player.rect.top - self.wall.size[1]
        # print(self.grass_size)
        self.bigmap_size = (32 * self.size[0] + 2*self.wall.size[0] + 2*self.grass_size[0], 32 * self.size[1]+ 2*self.wall.size[1] + + 2*self.grass_size[1])
        self.map_size = (32 * self.size[0] + 2*self.wall.size[0], 32 * self.size[1]+ 2*self.wall.size[1])
        self.map = pg.Surface(self.map_size)
        self.bigmap = pg.Surface(self.bigmap_size)
        self.map_rects = []
        self.map_rect = pg.Rect(0,0, self.map_size[0], self.map_size[1])
        # self.map_rect = pg.Rect(0,0, self.map_size[0], self.map_size[1])
        self.map_rect.move_ip(self.wall.size)
        self.bigmap_rect = pg.Rect(- self.grass_size[0],- self.grass_size[1], self.bigmap_size[0], self.bigmap_size[1])
        # print(self.init_map)
        self.init_grass()
        self.init_tilemap()
        self.init_wall()
        self.bigmap.blit(self.map, self.map_rect.move(self.grass_size[0],self.grass_size[1]))

    def init_wall(self):
        # top wall
        # self.wall.wall_rect.move_ip(0,self.grass_size[1])
        # self.wall.sidewall_rect.move_ip(self.grass_size[0], 0)
        top_wall = self.wall.wall_rect.move(0, 0)
        self.map.blit(self.wall.wall, top_wall)
        for i in range((32 * self.size[0])//96):
            top_wall.move_ip(96, 0)
            self.map.blit(self.wall.wall, top_wall)

        # bottom wall
        bottom_wall = self.wall.wall_rect.move(0, 32 * self.size[1] + self.wall.size[1])
        self.map.blit(self.wall.wall, bottom_wall)
        for i in range((32 * self.size[0])//96):
            bottom_wall.move_ip(96, 0)
            self.map.blit(self.wall.wall, bottom_wall)

        # left wall
        left_wall = self.wall.sidewall_rect.move(0, 0)
        self.map.blit(self.wall.sidewall, left_wall)
        for i in range((32 * self.size[1])//96):
            left_wall.move_ip(0, 96)
            self.map.blit(self.wall.sidewall, left_wall)

        # right wall
        right_wall = self.wall.sidewall_rect.move(32 * self.size[0] + self.wall.size[0], 0)
        self.map.blit(self.wall.sidewall, right_wall)
        for i in range((32 * self.size[1])//96):
            right_wall.move_ip(0, 96)
            self.map.blit(self.wall.sidewall, right_wall)

    def init_tilemap(self):
        for i in range(2*self.game.height//32):
            temp_list = []
            for j in range(2*self.game.width//32):
                tile = self.tileset.tiles[self.tilemap_index[j, i]]
                # rect = pg.Rect(self.grass_size[0] + self.wall.size[0] + j*32, self.grass_size[1] + self.wall.size[1] + i*32,32,32)
                rect = pg.Rect(self.wall.size[0] + j*32, self.wall.size[1] + i*32,32,32)
                self.map.blit(tile, rect)
                temp_list.append((tile, rect))
            self.tilemap.append(temp_list)

    def init_grass(self):
        for i in range(self.bigmap_size[1]//32):
            temp_list = []
            for j in range(self.bigmap_size[0]//32):
                tile = self.tileset.tiles[random.randrange(0, 31)]
                rect = pg.Rect(j*32, i*32,32,32)
                self.bigmap.blit(tile, rect)
                temp_list.append((tile, rect))
            self.tilemap.append(temp_list)


    def draw(self):

        self.game.screen.blit(self.bigmap, self.bigmap_rect)
        # self.game.screen.blit(self.map, self.map_rect)
        # self.wall.draw_wall_tileset()
        # self.wall.draw()
        # self.game.screen.blit(self.tileset.tiles[self.map[j, i]], (j*32, i*32))
        # for i in range(self.game.height//32):
        #     for j in range(self.game.width//32):
        #         self.game.screen.blit(self.tilemap[i][j][0], self.tilemap[i][j][1])
        # for map_rect in self.map_rects:
        #     self.game.screen.blit(self.map, map_rect.rect)

    def draw_tileset(self):
        for i in range(8):
            for j in range(8):
                self.game.screen.blit(self.tileset.tiles[j+8*i], (j*33+300, i*33+300))




    def update(self):
        dx, dy = 0, 0
        speed = self.game.player.speed * self.game.delta_time


        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dy += speed
        if keys[pg.K_s]:
            dy -= speed
        if keys[pg.K_a]:
            dx += speed
        if keys[pg.K_d]:
            dx -= speed

        if (keys[pg.K_w] or keys[pg.K_s]) and (keys[pg.K_a] or keys[pg.K_d]) and self.game.diagonal_speed_reduction:
            speed_reduction = PLAYER_DIAGONAL_SPEED_REDUCTION
            dx /= speed_reduction
            dy /= speed_reduction


        self.check_collision(dx, dy)





    def check_collision(self, dx, dy):

        # for i in range(self.game.height//32):
        #     for j in range(self.game.width//32):
        #         self.tilemap[i][j][1].move_ip(dx, dy)
        self.game.player_movement_x = True
        self.game.player_movement_y = True
        temp_rect = self.map_rect.move(dx, dy)
        if temp_rect.bottom < self.game.player.rect.bottom:
            self.game.player_movement_y = False
            dy = 0
        if temp_rect.top> self.game.player.rect.top:
            self.game.player_movement_y = False
            dy = 0
        if temp_rect.left> self.game.player.rect.left:
            self.game.player_movement_x = False
            dx = 0
        if temp_rect.right< self.game.player.rect.right:
            self.game.player_movement_x = False
            dx = 0

        self.map_rect.move_ip(dx, dy)
        self.bigmap_rect.move_ip(dx, dy)
