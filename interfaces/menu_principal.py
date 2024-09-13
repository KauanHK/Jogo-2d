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
        self.interface.titulo.exibir(self.screen)

        for botao in self.interface.botoes:
            if botao.hover():
                botao.definir_cor_hover()
            else:
                botao.definir_cor_padrao()
            botao.exibir(self.screen)

    def loadEvent(self, event) -> Literal["Jogo", "MenuNaves", "sair"] | None:
        for botao in self.interface.botoes:
            if botao.clicked(event):
                return botao.get_event()