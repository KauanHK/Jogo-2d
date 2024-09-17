import pygame
from components.nave import Nave
from interfaces.ui_jogo import Interface
from components.nave import Nave
from components.parede import Paredes


class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # Criar a nave, paredes e a interface
        screen_size = self.screen.get_size()
        self.nave = Nave(screen_size, 'center', 'center')
        self.paredes = Paredes(screen_size)
        self.interface = Interface(screen_size)

        # Definir Mask da nave e de um fragmento da imagem da parede
        self.nave_mask = self.nave.get_mask()
        self.fragmento_mask = self.paredes.get_mask()


    def run(self) -> None:
        '''Executa um frame do jogo'''
        
        self.interface.update(self.nave, self.nave_mask, self.paredes, self.fragmento_mask, self.pausado)
        self.interface.exibir(self.screen, self.nave, self.paredes, self.pausado)

        # self.exibir_pontuacao()

    def load_event(self, event: pygame.event.Event):
        if not self.pausado:
            self.nave.load_event(event)
            if event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado
        else:
            self.interface.load_event
        
        # if self.colidiu():
        #     for botao in self.interface.game_over.botoes:
        #         if botao.clicked(event):
        #             return botao.get_event()
            
    
    