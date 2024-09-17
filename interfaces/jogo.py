import pygame
from interfaces.ui_jogo import GameOver
from interfaces.ui_jogo import GerenciadorJogo


class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.interface = GerenciadorJogo(self.screen.get_size())
        self._colidiu = False

    def run(self) -> None:
        '''Executa um frame do jogo'''
        
        self.interface.update()
        self.interface.exibir(self.screen)
        if not self._colidiu and self.interface.colidiu():
            self._colidiu = True
            self.interface = GameOver(self.screen.copy(), self.interface.pontuacao.pontuacao)

        # self.exibir_pontuacao()

    def load_event(self, event: pygame.event.Event):
        return self.interface.load_event(event)