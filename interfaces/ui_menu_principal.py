import pygame
from components.botao import Botao
from components.titulo import Titulo

class Interface:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.titulo = self.criar_titulo()
        self.botoes = self.criar_botoes()

    def criar_titulo(self):
        return Titulo(self.screen.get_size(), 'center', self.screen.get_height()/6, 'Jogo da Nave', (255,0,0), 120)

    def criar_botoes(self, size: tuple[int,int] | None = (280, 80), font_size: int | None = 48):
        centery = self.screen.get_height() // 5 * 3
        sep = size[1] + 40
        botoes = [
            Botao(self.screen.get_size(), "Jogo", ('center', centery-sep), size, 'Jogar', font_size),
            Botao(self.screen.get_size(), "MenuNaves", ('center', centery), size, 'Naves', font_size),
            Botao(self.screen.get_size(), None, ('center', centery+sep), size, 'Sair', font_size)
        ]
        return botoes