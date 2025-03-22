import pygame
import os
import math

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, width=10, height=30):
        super().__init__()
        
        # Create a solid rectangle for the lase base
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image.fill((0, 0, 0, 0))
    
        # Loading the laser PNG
        self.laser_overlay = pygame.image.load("Base\Assets\FX\Player_Laser.png").convert_alpha()
        self.laser_overlay = pygame.transform.scale(self.laser_overlay, (width, height))

        # Combine rectangle and overlay
        
        self.image = self.original_image.copy()
        self.image.blit(self.laser_overlay, (0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        # Calculating the angle of the laser's direction
        angle_rad = math.atan2(-speed_y, speed_x)
        angle_deg = math.degrees(angle_rad)
        
        # Adjusting the angle for the PNG'S orientation
        angle_deg += 90
        
        # Rotating the combined image
        self.image = pygame.transform.rotate(self.image, angle_deg)
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        self.rect.x += self.speed_x # update x.
        self.rect.y += self.speed_y # update y.

        # Removing it when it goers off screen
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.right < 0 or self.rect.left > 800:
            self.kill()
            

        # updating the angle to match movement direction
        self.angle = math.degrees(math.atan2(-self.speed_y, self.speed_x)) - 90
        # print(f"Laser rotation angle: {self.angle}")            
        