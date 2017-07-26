import pygame

pygame.init()
pygame.mixer.music.load("sound_file.ogg")
pygame.mixer.music.play()
pygame.event.wait()
