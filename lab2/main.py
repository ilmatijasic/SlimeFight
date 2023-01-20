import pygame, sys, random
from dataclasses import dataclass


mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((700, 800))

# Load in balloon image
balloon_img= pygame.image.load("objects/balloon.bmp")
balloon_size = balloon_img.get_size()
balloon_img = pygame.transform.scale(balloon_img, (balloon_size[0]//2,balloon_size[1]//2 ))

width, height = pygame.display.get_surface().get_size()

# list of wind polygons
wind_left = []
wind_right = []

# parameters for balloon speed, wind and drag
start_velocity = (0., -5.)
start_acceleration = (0., 0.)
wind_acceleration = 0.2
drag_acceleration = 0.05


@dataclass
class Balloon:
    '''Dataclass for balloon'''
    img: pygame.Surface
    x: int = 0
    y: int = 0
    velocity_x: float = start_velocity[0]
    velocity_y: float = start_velocity[1]
    acceleration_x: float = start_acceleration[0]
    acceleration_y: float = start_acceleration[1]
    time: float = 1.
    collision: bool = False
    left_wind: bool = False
    right_wind: bool = False

    def __post_init__(self):

        self.rect: pygame.Rect = self.img.get_rect() # Get rect of image

        self.offset = {} # Offset so the center of the balloon spawns on mouse and not top left corner
        self._offset_x = -self.rect.center[0]
        self._offset_y = -self.rect.center[1]
        self.x += self._offset_x
        self.y += self._offset_y
        self.rect.move_ip(self.x, self.y) # Move the rect to mouse


    def check_wind(self):
        '''Check if balloon is in the wind area, if so change acceleration to the defined wind acceleration'''

        for i in range(max(len(wind_right), len(wind_left))):
            if len(wind_right) > 0 and i < len(wind_right)and (wind_right[i][0] > self.rect.top > wind_right[i][1]):
                self.acceleration_x = wind_right[i][2]
                return True

            if len(wind_left) > 0 and i < len(wind_left) and (wind_left[i][0] > self.rect.top > wind_left[i][1]):
                self.acceleration_x = wind_left[i][2]
                return True

        self.acceleration_x = start_acceleration[0]
        return False


    def update(self, time_remove=0.005):
        '''Update position, speed, and time of the balloon'''

        # Check if in wind area
        self.check_wind()

        # Lower time
        self.time -= time_remove

        # Move horizontally
        self.rect.move_ip(self.velocity_x, 0)

        # Check horizontal collisions with the edges of the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width

        # Move vertically
        self.rect.move_ip(0, self.velocity_y)

        # Check vertical collisions with the edges of the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

        self.x = self.rect.x
        self.y = self.rect.y

        # Change speed
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y

        # Drag
        self.velocity_x += -drag_acceleration * (self.velocity_x)


    def render(self):
        '''Draw balloon on screen'''

        screen.blit(self.img,(self.rect))

        # print(self.rect, " ; ",self.x, self.y)
        # print(self.acceleration_x, self.velocity_x)


balloons = []

wind_left.append((600, 400, -wind_acceleration))
wind_right.append((300, 100, wind_acceleration*1.5))
wind_right.append((700, 600, wind_acceleration))


clicking = False
while True:
    screen.fill((0,0,0))

    # Draw wind areas
    for i in wind_left:

        pygame.draw.rect(screen, (0, 100, 0), Rect(0,i[1], width, (i[0]-i[1])))
    for i in wind_right:
        pygame.draw.rect(screen, (0, 0, 100), Rect(0,i[1], width, (i[0]-i[1])))

    # Get position of mouse
    mx, my = pygame.mouse.get_pos()

    # Draw balloon on click
    if clicking:
        rect = balloon_img.get_rect()
        balloons.append(Balloon(img=balloon_img, x=mx, y=my))

        clicking = False

    dead_ballons = []
    for balloon in balloons:
        # Update the position and speed of the balloon
        balloon.update()

        # Add balloon to dead balloons to be removed later
        if balloon.time <= 0:
            dead_ballons.append(balloon)
            continue

        # Draw the balloon on screen
        balloon.render()

    # Remove dead balloons
    for balloon in dead_ballons:
        balloons.remove(balloon)




    # Check for button press
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    pygame.display.update()
    mainClock.tick(60)
