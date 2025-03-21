import pygame
import player
import Asteroid
import sounds
import UI
import Menu

# Initialize Pygame
pygame.init()

# SCREEN SETUP
Screen_Width, Screen_Height = 800, 600
screen = pygame.display.set_mode((Screen_Width, Screen_Height), pygame.SRCALPHA)
pygame.display.set_caption("GAME TEST!")

# MENU ASSETS
menu_bg = pygame.transform.scale(pygame.image.load("Base/Assets/Background/Bkg2.png").convert(), (Screen_Width, Screen_Height))
menu_font = pygame.font.Font(None, 48)
menu_title_font = pygame.font.Font(None, 72)
button_sound = pygame.mixer.Sound("Base/Assets/game_sounds/UI_buttons.ogg")
button_sound.set_volume(0.5)
select_sound = pygame.mixer.Sound("Base/Assets/game_sounds/UI_buttons.ogg")
select_sound.set_volume(0.5)
main_menu = Menu.Menu(screen, Screen_Width, Screen_Height, menu_bg, menu_font, menu_title_font, button_sound, select_sound)
show_menu = True

# GAME ASSETS
font = pygame.font.Font(None, 36)
background = pygame.transform.scale(pygame.image.load("Base/Assets/Background/Bkg2.png").convert(), (Screen_Width, Screen_Height))
cursor = pygame.transform.scale(pygame.image.load("Base/Assets/Interface/crosshair.png").convert_alpha(), (20, 20))

# GAME STATE
game_over = False
game_over_option = 0

# Meteor spawn
spawn_timer = 0
spawn_interval = 150
initial_spawn_count = 20
spawn_count = initial_spawn_count
spawn_increase_interval = 1000
spawn_increase_timer = pygame.time.get_ticks()

# Sprite groups
all_sprites = pygame.sprite.Group()
Asteroid_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
player_ship = player.Player(Screen_Width // 2, Screen_Height // 2, all_sprites)
all_sprites.add(player_ship)

# UI
ui = UI.UI(screen, background)

# Cursor
pygame.mouse.set_visible(False)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    if show_menu:
        main_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                selection = main_menu.handle_input(event)
                if selection == 0:
                    show_menu = False
                elif selection == 1:
                    running = False
    elif not game_over:
        if current_time - spawn_timer > spawn_interval:
            for _ in range(1):
                asteroid = Asteroid.Asteroid()
                all_sprites.add(asteroid)
                Asteroid_group.add(asteroid)
            spawn_timer = current_time

        if current_time - spawn_increase_timer > spawn_increase_interval:
            spawn_count += 1
            spawn_increase_timer = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                player_ship.shoot(laser_group, all_sprites)

        screen.blit(background, (0, 0))
        all_sprites.update()
        laser_group.draw(screen)
        all_sprites.draw(screen)

        if pygame.sprite.spritecollide(player_ship, Asteroid_group, False):
            game_over = True

        collisions = pygame.sprite.groupcollide(laser_group, Asteroid_group, True, False)
        for asteroids in collisions.values():
            for asteroid in asteroids:
                asteroid.health -= 100
                sounds.play_sound("M_impact")
                if asteroid.health <= 0:
                    asteroid.kill()
                    ui.update_score(ui.score + 10)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor, (mouse_x - cursor.get_width() / 2, mouse_y - cursor.get_height() / 2))
        ui.draw_score()
    else:
        ui.draw_game_over(Screen_Width, Screen_Height, game_over_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_over_option = (game_over_option - 1) % 2
                    button_sound.play()
                elif event.key == pygame.K_DOWN:
                    game_over_option = (game_over_option + 1) % 2
                    button_sound.play()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    if game_over_option == 0:
                        game_over = False
                        ui.update_score(0)
                        Asteroid_group.empty()
                        all_sprites.empty()
                        laser_group.empty()
                        player_ship = player.Player(Screen_Width // 2, Screen_Height // 2, all_sprites)
                        all_sprites.add(player_ship)
                        spawn_timer = 0
                        spawn_count = initial_spawn_count
                        spawn_increase_timer = pygame.time.get_ticks()
                    elif game_over_option == 1:
                        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()