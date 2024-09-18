import pygame
from components.nave import Nave
from components.parede import Paredes
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from utils.cores import *


class Jogo:

    def __init__(self, screen_size: tuple[int,int], nave: Nave, paredes: Paredes):
        self.screen_size = screen_size
        self.nave = nave
        self.paredes = paredes



class PopUpGameOver:

    def __init__(self, screen_size: tuple[int,int]):
        """PopUp do game over."""
        self.screen_size = screen_size

        self.popup = self.criar_popup(screen_size)
        self.titulo = self.criar_titulo(screen_size)
        self.botoes = self.criar_botoes(screen_size)
        self.popup.update()

    def criar_popup(self, screen_size: tuple[int,int]):
        size = (screen_size[0] * 0.5, screen_size[1] * 0.75)
        return PopUp(screen_size, size, CINZA_TRANSPARENTE)
    
    def criar_titulo(self, screen_size: tuple[int,int]):
        y = self.popup.coord[1] + 100
        return Titulo(screen_size, 'center', y, 'Game Over', VERMELHO)
    
    def criar_botoes(self, screen_size: tuple[int,int]):
        y = self.popup.coord[1] + self.popup.size[1] * 0.6
        size = (self.popup.size[0] * 0.6, self.popup.size[1] * 0.12)
        botoes = [
            Botao(screen_size, "Jogo", ('center', y), size, 'Restart', 32),
            Botao(screen_size, "MenuPrincipal", ('center', y+size[1]+20), size, 'Menu', 32),
        ]
        return botoes

    def update(self):
        for botao in self.botoes:
            botao.update()

    def exibir(self, screen: pygame.Surface):
        self.popup.exibir(screen)
        self.titulo.exibir(screen)
        for botao in self.botoes:
            botao.exibir(screen)

    def load_event(self, event: pygame.event.Event):
        for botao in self.botoes:
            if botao.clicked(event):
                return botao.get_event()
            
class Pause:

    def __init__(self, screen_size: tuple[int,int]):
        self.screen_size = screen_size
        self.popup = self.criar_popup(self.screen_size)
        self.titulo = self.criar_titulo(self.screen_size)
        self.botoes = self.criar_botoes(self.screen_size)

    def criar_popup(self, screen_size: tuple[int,int]) -> PopUp:
        size = (screen_size[0] * 0.4, screen_size[1] * 0.5)
        return PopUp(screen_size, size, CINZA_TRANSPARENTE)
    
    def criar_titulo(self, screen_size: tuple[int,int]):
        y = self.popup.coord[1] + 70
        return Titulo(screen_size, 'center', y, 'Pause')

    def criar_botoes(self, screen_size: tuple[int,int]):
        size = (screen_size[0] * 0.25, screen_size[1] * 0.1)
        y = self.popup.coord[1] + self.popup.size[1] - size[1] - 20
        botao_sair = Botao(screen_size, "MenuPrincipal", ('center', y), size, 'Menu', 40)

        y -= botao_sair.size[1] + 20
        botao_continuar = Botao(screen_size, 'continuar', ('center', y), size, 'Continuar', 40)

        return botao_continuar, botao_sair

    def update(self):
        for botao in self.botoes:
            botao.update()

    def exibir(self, screen: pygame.Surface):
        self.popup.exibir(screen)
        self.titulo.exibir(screen)
        for botao in self.botoes:
            botao.exibir(screen)

    def load_event(self, event: pygame.event.Event):
        for botao in self.botoes:
            if botao.clicked(event):
                print(botao.get_event())
                return botao.get_event()