import pygame
from components.botao import Botao
from components.titulo import Titulo
from utils.cores import VERMELHO

class Interface:

    def __init__(self, screen_size: tuple[int]):
        self.screen_size = screen_size
        self.titulo = self.criar_titulo(screen_size)
        self.botoes = self.criar_botoes(screen_size)

    def criar_titulo(self, screen_size: tuple[int]):
        x = 'center'
        y = screen_size[1] / 6
        txt = 'Jogo da Nave'
        font_size = 120
        return Titulo(screen_size, x, y, txt, VERMELHO, font_size)

    def criar_botoes(self, screen_size: tuple[int]):
        size = (280, 80)
        font_size = 48
        centery = screen_size[1] // 5 * 3
        sep = size[1] + 40

        botoes = [
            Botao(screen_size, "Jogo", ('center', centery-sep), size, 'Jogar', font_size),
            Botao(screen_size, "MenuNaves", ('center', centery), size, 'Naves', font_size),
            Botao(screen_size, "sair", ('center', centery+sep), size, 'Sair', font_size)
        ]
        return botoes
    
    def update(self):
        self.titulo.atualizar_cor()
        self.titulo.update()
        for botao in self.botoes:
            botao.update()

    def exibir(self, screen: pygame.Surface):
        self.titulo.exibir(screen)
        for botao in self.botoes:
            botao.exibir(screen)