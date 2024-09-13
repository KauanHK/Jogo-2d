import pygame
from components.parede import Parede
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from utils.cores import *


class Interface:

    def __init__(self, screen_size: tuple[int]):
        self.pause = GameOver.criar_popup(Pause, screen_size)
        self.game_over = GameOver(screen_size)


    
class Paredes:

    def __init__(self, screen_size: tuple[int], img: pygame.Surface):
        self.screen_size = screen_size
        self.paredes = self.criar_paredes(img)
        self.index = 0

    def definir_coord_paredes(self) -> list[int]:
        x = round(self.screen_size[0] * 0.95)
        x_aumento = round(self.screen_size[0] / 4)
        return [x + i*x_aumento for i in range(4)]
    
    def criar_paredes(self, img: pygame.Surface) -> list[Parede]:
        lefts = self.definir_coord_paredes()
        paredes = [Parede(self.screen_size, img, x) for x in lefts]
        return paredes
    
    def get_mask(self):
        return self.paredes[0].getMask()
    
    def exibir(self, screen: pygame.Surface):
        for parede in self.paredes:
            parede.exibir(screen)
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index >= len(self.paredes):
            raise StopIteration
        parede = self.paredes[self.index]
        self.index += 1
        return parede
    
    def __getitem__(self, index: int):
        return self.paredes[index]

class Pause:

    def __init__(self):
        pass

class GameOver:

    def __init__(self, screen_size: tuple[int]):
        self.popup = self.criar_popup(screen_size)
        self.titulo = self.criar_titulo()
        self.botoes = self.criar_botoes()
        self.botoes_rects = self.definir_rects_botoes()
        self.atualizar_popup()

    def criar_popup(self, screen_size: tuple[int]) -> PopUp:
        largura = screen_size[0] * 0.4
        altura = screen_size[1] * 0.7
        size = (largura, altura)
        popup = PopUp(screen_size, size, CINZA_TRANSPARENTE)
        return popup
    
    def criar_titulo(self) -> Titulo:
        return Titulo(self.popup.get_size(), 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes(self) -> list[Botao]:
        y = self.popup.get_size()[1] * 0.6
        coord = ('center', y)
        largura = self.popup.get_size()[0] / 2
        altura = 60
        size = (largura, altura)
        botao_restart = Botao(self.popup.get_size(), "Jogo", coord, size, 'Restart', 40)

        y += botao_restart.size[1] + 20
        coord = ('center', y)
        largura = self.popup.get_size()[1]/2
        size = (largura, altura)
        botao_sair = Botao(self.popup.get_size(), "MenuPrincipal", coord, size, 'Menu', 40)
        return botao_restart, botao_sair
    
    def definir_rects_botoes(self):
        rects = []
        for botao in self.botoes:
            x = self.popup.coord[0] + botao.coord[0]
            y = self.popup.coord[1] + botao.coord[1]
            rect = botao.get_rect(topleft = (x,y))
            rects.append(rect)
        return rects

    def atualizar_popup(self):
        self.popup.atualizar()
        self.popup.blit(self.titulo.surface, self.titulo.coord)
        for botao in self.botoes:
            self.popup.blit(botao.surface, botao.coord)

    def exibir(self, screen: pygame.Surface):
        self.popup.exibir(screen)