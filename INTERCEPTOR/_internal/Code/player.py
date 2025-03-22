# Player.py

import pygame;
import math;
import os
import Weapons
import sounds;
from helper import resource_path

from Weapons import Laser;

# Creating the player object
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites_group):
        super().__init__();
        # Creating an triangle placeholder
        self.original_image = pygame.Surface((35, 35), pygame.SRCALPHA)   
        self.original_image.fill((0,0,0,0))
        
        
        #Drawing the triangle using pygame draw tool
        pygame.draw.polygon(self.original_image, (0, 0, 0), [(15, 0), (0, 30), (30, 30)])
        self.image = self.original_image
        
    
        #Loading the ship png
        self.ship_overlay = pygame.image.load(resource_path("Assets\Models\Player_ship.png")).convert_alpha()
        
        self.ship_overlay = pygame.transform.scale(self.ship_overlay, (35, 35)) #resizing the image to fit the triangle

        # Combine triangle and overlay into a single surface
        self.original_combined_image = self.original_image.copy()
        self.original_combined_image.blit(self.ship_overlay, (0, 0))
        self.image = self.original_combined_image
        
        # Resizing the player ship size
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # Centering the rect
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100
        self.angle = 0
        self.rotation_speed = 5
        self.average_angle = 0
        
        # Setting the trail
        self.trail_interval = 50 # Adjusting the interval
        self.last_trail_time = pygame.time.get_ticks() - self.trail_interval
        self.all_sprites_group = all_sprites_group
        
    def shoot(self, laser_group, all_sprites):
        
        # Adding sound to the laser
        sounds.play_sound("Laser_shot")
        sounds.set_sound_volume("Laser_shot", 0.6)
        
        angle_rad = math.radians(-self.average_angle - 90) # Converting the angle to radians
        speed_x = 10 * math.cos(angle_rad) # get x component of speed.
        speed_y = 10 * math.sin(angle_rad) # get y component of speed.

        # Calculate offset for the internal origin (slightly inside the ship)
        internal_offset_x = (self.rect.width / 3) * math.cos(angle_rad)  # Adjust factor for desired depth
        internal_offset_y = (self.rect.width / 3) * math.sin(angle_rad)  # Adjust factor for desired depth

        # Calculate laser spawn position (internal origin)
        laser_x = self.rect.centerx + internal_offset_x
        laser_y = self.rect.centery + internal_offset_y
        
        # Fixing the laser T pose spawn
        ahead_offset = 5
        ahead_x = laser_x + ahead_offset * math.cos(angle_rad)
        ahead_y = laser_y + ahead_offset * math.sin(angle_rad)
        
        #Creating the laser at the internal origin
        laser_instance = Weapons.Laser(ahead_x, ahead_y, speed_x, speed_y, width = 40, height = 70)
        laser_group.add(laser_instance)
        all_sprites.add(laser_instance)
        
        # Adjusting laser's rect to visually align with the origin
        laser_instance.rect.centerx = ahead_x
        laser_instance.rect.centery = ahead_y
        

        #normalizing the speed x and speed y
        magnitude = math.sqrt(speed_x**2 + speed_y **2)
        if magnitude != 0:
            speed_x = speed_x / magnitude * 10
            speed_y = speed_y / magnitude * 10
        
    # updating player position    
    
    def update(self): 
        # Making the ship move, using the keyboard arrows
        # X - Axis
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # X - Axis
        if keys[pygame.K_a or pygame.KEY_LEFT]:
            self.speed_x = -5
            if current_time - self.last_trail_time > self.trail_interval:
                self.create_trail()
        elif keys[pygame.K_d or pygame.KEY_RIGHT]:
            self.speed_x = 5
            if current_time - self.last_trail_time > self.trail_interval:
                self.create_trail()
        else:
            self.speed_x = 0
            
        # Y - Axis
        if keys[pygame.K_w or pygame.KEY_UP]:
            self.speed_y = -5
            if current_time - self.last_trail_time > self.trail_interval:
                self.create_trail()
        elif keys[pygame.K_s or pygame.KEY_DOWN]:
            self.speed_y = 5
            if current_time - self.last_trail_time > self.trail_interval:
                self.create_trail()
        else: 
            self.speed_y = 0
            
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y # Adding vertical movement
        
        # Keeping the player withing the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            
        
        # Making the tip of the ship follow the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos() # picking the mouse position
        rel_x = mouse_x - self.rect.centerx
        rel_y = mouse_y - self.rect.centery
        target_angle = math.degrees(math.atan2(-rel_y, rel_x)) - 90
        
        # updating average angle
        self.update_average_angle(target_angle)
        
        self.image = pygame.transform.rotate(self.original_combined_image, self.average_angle)
        self.ret = self.image.get_rect(center=self.rect.center)
        
    def update_average_angle(self, target_angle):
        angle_diff = (target_angle - self.average_angle) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Adjusting the average angle towards the target angle
        self.average_angle += angle_diff * 0.2

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            
    def create_trail(self):
        trail_offset = 15
        trail_x = self.rect.centerx - trail_offset * math.cos(math.radians(-self.average_angle - 90))
        trail_y = self.rect.centery - trail_offset * math.sin(math.radians(-self.average_angle - 90))

        trail_particle = Trail((trail_x, trail_y), (255, 255, 255), (5, 5), 200)
        self.all_sprites_group.add(trail_particle)
        self.groups()[0].add(trail_particle)
        self.last_trail_time = pygame.time.get_ticks()
    
class Trail(pygame.sprite.Sprite):
    def __init__ (self, position, color, size, lifetime):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size[0] // 2, size[1] // 2), size[0] // 2)
        self.rect = self.image.get_rect(center = position)
        self.alpha = 255
        self.lifetime = lifetime
        self.creation_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time
        self.alpha = max(0, 255 - (elapsed_time / self.lifetime) * 255)
        self.image.set_alpha(int(self.alpha))
        if self.alpha <= 0:
            self.kill()
            
            
            
        
        