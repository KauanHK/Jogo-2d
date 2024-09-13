import pygame
from components.parede import Parede
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from utils.cores import *


class Interface:

    def __init__(self, screen_size: tuple[int]):
        self.screen_size = screen_size
        self.pause = self.criar_popup()
        popup = self.criar_popup()
        titulo_game_over = self.criar_titulo_game_over(popup)
        botoes_game_over = self.criar_botoes_game_over(popup)
        self.game_over = GameOver(popup, titulo_game_over, botoes_game_over)

    def criar_popup(self) -> PopUp:
        largura = self.screen_size[0] * 0.4
        altura = self.screen_size[1] * 0.7
        size = (largura, altura)
        interface = PopUp(self.screen_size, size, CINZA_TRANSPARENTE)
        return interface

    def criar_titulo_game_over(self, popup: PopUp) -> Titulo:
        return Titulo(popup.get_size(), 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes_game_over(self, popup: PopUp) -> list[Botao]:
        y = self.screen_size[1] * 0.6
        botao_restart = Botao(popup.size, "Jogo", ('center', y), (popup.get_size()[0]/2, 60), 'Restart', 40)
        botao_sair = Botao(popup.size, "MenuPrincipal", ('center', y + botao_restart.size[1]+20), (popup.size[1]/2, 60), 'Menu', 40)
        return botao_restart, botao_sair
    
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

class GameOver:

    def __init__(self, popup: PopUp, titulo: Titulo, botoes: list[Botao]):
        self.popup = popup
        self.titulo = titulo
        self.botoes = botoes
        self.atualizar_popup()
    
    def atualizar_popup(self):
        self.popup.blit(self.titulo, self.titulo.coord)
        for botao in self.botoes:
            self.popup.blit(botao, botao.coord)

    def exibir(self):
        self.popup.exibir()