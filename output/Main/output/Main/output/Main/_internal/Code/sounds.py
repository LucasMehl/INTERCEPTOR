import pygame
from helper import resource_path 

pygame.mixer.init()

# Dictionary to store loaded sounds
loaded_sounds = {}

def load_sound(filepath, sound_name, volume=1.0):
    # Loading a sounds file and storing it in the dictionary

    try:
        sound = pygame.mixer.Sound(filepath)
        sound.set_volume(volume)
        loaded_sounds[sound_name] = sound
    except pygame.error as e:
        print(f"Error loading {filepath}: {e}")

def play_sound(sound_name):
    # Playing a sound from the loaded_sounds dictionary

    if sound_name in loaded_sounds:
        loaded_sounds[sound_name].play()
    else:
        print(f"Sound {sound_name} not loaded.")

def set_sound_volume(sound_name, volume):
    # Setting the volume of a loaded sound

    if sound_name in loaded_sounds:
        loaded_sounds[sound_name].set_volume(volume)
    else:
        print(f"Sound {sound_name} not loaded.")

# Adding a sound
load_sound(resource_path("Assets/game_sounds/Laser.sound.ogg"), "Laser_shot", 0.5)
load_sound(resource_path("Assets/game_sounds/Meteor_impact.ogg"), "M_impact", 0.5)