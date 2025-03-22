# Asteroid

import pygame;
import random;
import os;

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Calling the parent class initializer. <---- DO NOT FORGET THIS
        # loading the images into a list
        self.asteroid_images = [
            pygame.image.load(f"Base\Assets\Models\Meteor{i}.png").convert_alpha()
            for i in range(1,9) #Picking the meteors from 1 to 8. You can change this if you want, depending how many sprites do you have
        ]

        self.original_image = random.choice(self.asteroid_images) # Storing the original image
        
        # Random scaling factors
        # You can change the values to change the asteroid size
        scale_factor = random.uniform(0.5, 2) # scaling between 50% and 200% of original size
        
        # Scale the Asteroid image
        scaled_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale_factor),
                                                                    int(self.original_image.get_height() * scale_factor)))
        
        # Getting bounding rectangle of non-transparent pixels
        mask = pygame.mask.from_surface(scaled_image)
        bounding_rects = mask.get_bounding_rects() # Getting a list of bounding rects
        if bounding_rects:
            bounding_rect = bounding_rects[0]
            
        else:
            # Handle the case where there are no non-transparent pixels
            bounding_rect = pygame.Rect(0, 0, scaled_image.get_width(), scaled_image.get_height())
        
        # Create a rectangular base based on the bounding rectangle
        self.base_image = pygame.Surface((bounding_rect.width, bounding_rect.height), pygame.SRCALPHA)
        self.base_image.fill((0, 0, 0, 0)) # Transparent background

        # Bli the scaled image onto the base, offset by the bounding rect's position
        self.base_image.blit(scaled_image, (-bounding_rect.x, -bounding_rect.y))
        
        self.image = self.base_image # Setting the final image
        self.rect = self.image.get_rect()
        
        # Giving health to the asteroid
        self.health = 100
        
        # Random start position (off-screen)
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect.x = random.randint(0, 800)
            self.rect.y = -self.rect.height
            
        elif side == "bottom":
            self.rect.x = random.randint(0, 800)
            self.rect.y = 600
            
        elif side == "left":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, 800)
            
        else: #right
            self.rect.x = 800
            self.rect.y = random.randint(0, 800)
            
	
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Removing the asteroid when it goes off screen
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()