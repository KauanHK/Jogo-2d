import pygame
from interfaces.ui_menu_principal import Interface
from typing import Literal

class MenuPrincipal:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.interface = Interface(self.screen.get_size())

    def run(self):
        self.interface.update()
        self.interface.exibir(self.screen)

    def load_event(self, event) -> Literal["Jogo", "MenuNaves", "Sair"] | None:
        for botao in self.interface.botoes:
            if botao.clicked(event):
                return botao.get_event()