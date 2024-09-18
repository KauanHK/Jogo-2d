import pygame
from interfaces.menu_principal import MenuPrincipal
from typing import Literal

class MenuPrincipalManager:

    def __init__(self, screen_size: tuple[int,int]):
        self.screen_size = screen_size
        self.interface = MenuPrincipal(self.screen_size)

    def run(self, screen: pygame.Surface) -> None:
        self.interface.update()
        self.interface.exibir(screen)

    def load_event(self, event) -> Literal["Jogo", "MenuNaves", "Sair"] | None:
        for botao in self.interface.botoes:
            if botao.clicked(event):
                return botao.get_event()