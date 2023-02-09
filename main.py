import pygame, sys
from random import randint
from pytmx.util_pygame import load_pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image1 = pygame.image.load('sidescrollproject/assets/mmitch.png').convert_alpha()
        self.image = pygame.transform.scale(self.image1, (32,32))
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.angle = 0
        self.image = pygame.image.load('sidescrollproject/assets/taxip.png').convert_alpha()
        self.image1 = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image1.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.angle = 0
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.angle = 180
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.angle = 270
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.angle = 90
        else:
            self.direction.x = 0

    def update(self):
         self.input()
         self.rect.center += self.direction * self.speed
         self.image = pygame.transform.rotate(self.image1, self.angle)
         self.rect = self.image.get_rect(center = self.rect.center)
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset 
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # ground
        
        self.ground_surf = pygame.image.load('sidescrollproject/assets/taximap.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
 
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):

        self.center_target_camera(player)

        # ground 
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

# setup 
camera_group = CameraGroup()
player = Player((640,360),camera_group)

Tree((1500, 200), camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill('lime')

    camera_group.update()
    camera_group.custom_draw(player)

    pygame.display.update()
    clock.tick(60)
