# Menu

import pygame

pygame.font.init()

class Menu:
    def __init__(self, screen, screen_width, screen_height, background_image, font, title_font, button_sound, select_sound):
        self.screen = screen
        self.width = screen_width
        self.height = screen_height
        self.font = pygame.font.Font("Base\Assets\Interface\main_font.ttf", 40)
        self.title_font = pygame.font.Font("Base\Assets\Interface\main_font.ttf", 60)
        self.selected_option = 0
        self.options = ["PLAY", "QUIT"]
        self.background_image = background_image
        self.button_sound = button_sound
        self.select_sound = select_sound
        
    def draw(self):
        self.screen.blit(self.background_image, (0, 0)) # Black Background - PLACEHOLDER
        
        # Title
        title_text = self.title_font.render("INTERCEPTOR", True, (255, 255, 255))
        title_rect = title_text.get_rect(center = (self.width // 2, self.height // 3))
        self.screen.blit(title_text, title_rect)
        
        # Menu Options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 60))
            self.screen.blit(text, rect)
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.button_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len (self.options)
                self.button_sound.play()
            elif event.key == pygame.K_RETURN:
                self.select_sound.play() # Select sound
                return self.selected_option # Return selected option index
            
        return None