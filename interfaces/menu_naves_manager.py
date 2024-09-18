import pygame
from .menu_naves import MenuNaves
from components.nave import Nave


class MenuNavesManager:

    def __init__(self, screen_size: tuple[int,int]):
        self.screen_size = screen_size
        self.nave_selecionada = Nave.selecionada
        self.interface = MenuNaves(self.screen_size)


    def run(self, screen: pygame.Surface):
        self.interface.update()
        self.interface.exibir(screen)

    def load_event(self, event: pygame.event.Event):
        return self.interface.load_event(event)