import pygame
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
# from utils.types import InterfaceType
from utils.cores import *


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