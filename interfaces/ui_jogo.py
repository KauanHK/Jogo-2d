import pygame
from components.parede import Parede
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from utils.cores import *
from utils.imagens import carregar_imagem


class Interface:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.pause = self.criar_popup()
        self.game_over = GameOver()
        self.game_over = self.criar_popup()
        self.titulo_game_over = self.criar_titulo_game_over()
        self.botoes_game_over = self.criar_botoes_game_over()

    def criar_popup(self) -> PopUp:
        largura = self.screen.get_width() * 0.4
        altura = self.screen.get_height() * 0.7
        size = (largura, altura)
        interface = PopUp(self.screen, size, CINZA_TRANSPARENTE)
        return interface

    def criar_titulo_game_over(self) -> Titulo:
        return Titulo(self.game_over.interface, 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes_game_over(self) -> list[Botao]:
        y = self.screen.get_height() * 0.6
        botao_restart = Botao(self.screen, "Jogo", ('center', y), (self.game_over.size[0]/2, 60), 'Restart', 40)
        botao_sair = Botao(self.screen, "MenuPrincipal", ('center', y + botao_restart.size[1]+20), (self.game_over.size[0]/2, 60), 'Menu', 40)
        return botao_restart, botao_sair
    
class Paredes:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.paredes = self.criar_paredes()
        self.index = 0

    def definir_coord_paredes(self) -> list[int]:
        x = round(self.screen.get_width() * 0.95)
        x_aumento = round(self.screen.get_width() / 4)
        return [x + i*x_aumento for i in range(4)]
    
    def carregar_img_parede(self):
        largura_parede = self.screen.get_width() / 10
        largura_parede = 80 if largura_parede > 80 else largura_parede
        return carregar_imagem('imagens', 'obstaculo.jpg', size=(largura_parede,'auto'))

    def criar_paredes(self) -> list[Parede]:
        lefts = self.definir_coord_paredes()
        img = self.carregar_img_parede()
        paredes = [Parede(self.screen,img, x) for x in lefts]
        for x in lefts:
            paredes.append(Parede(self.screen, img, x))
        return paredes
    
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

    def _init__(self, popup: PopUp, titulo: Titulo, botoes: list[Botao]):
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