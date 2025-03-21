# Ui

import pygame

pygame.font.init() # Initializing the font module
    
class UI:
    def __init__(self, screen, background_image):
        self.screen = screen
        # Loading custom font
        self.font = pygame.font.Font("Base\Assets\Interface\main_font.ttf", 40)
        self.score = 0
        self.background_image = background_image
        
    def update_score(self, score):
        self.score = score
        
    def draw_score(self):
        score_display = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_display, (10, 10))            

    def draw_game_over(self, screen_width, screen_height, selected_option): # Adding the game over function
        self.screen.blit(self.background_image, (0, 0))
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(game_over_text, text_rect)
        
        # Drawing the score
        score_display = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        score_rect = score_display.get_rect(center=(screen_width // 2, screen_height // 3))
        
        self.screen.blit(score_display, score_rect)
        self.screen.blit(score_display, score_rect)
        
        options = ["RESTART", "QUIT"]
        for i, option in enumerate(options):
            color = (255, 255, 255) if i != selected_option else (255, 0, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center = (screen_width // 2, screen_height // 2 + i * 60))
            self.screen.blit(text, rect)