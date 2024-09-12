import pygame
from interfaces.ui_menu_principal import Interface
from typing import Literal

class MenuPrincipal:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.interface = Interface(self.screen)

    def run(self):
        
        self.interface.titulo.atualizarCor()
        self.interface.titulo.update()
        self.interface.titulo.exibir()

        for botao in self.interface.botoes:
            botao.exibir()

    def loadEvent(self, event) -> Literal["Jogo", "MenuNaves", "sair"] | None:
        for botao in self.interface.botoes:
            botao.hover()    
            if botao.clicked(event):
                return botao.get_event()