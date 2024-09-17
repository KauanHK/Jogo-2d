import pygame
from pontuacao import Pontuacao

pygame.init()

p = Pontuacao((100,800), 0)

print(p.get_max_pontuacao())