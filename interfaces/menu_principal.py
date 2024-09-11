import pygame
from components.titulo import Titulo
from components.botao import Botao
from interfaces.jogo import Jogo
from interfaces.menu_naves import MenuNaves
from typing import Literal, Union

class MenuPrincipal:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.titulo = self.criar_titulo()
        self.botoes = self.criar_botoes()

    def criar_titulo(self):
        return Titulo(self.screen, 'center', self.screen.get_height()/6, 'Jogo da Nave', (255,0,0), 120)

    def criar_botoes(self, size: tuple[int,int] | None = (280, 80), font_size: int | None = 48):
        centery = self.screen.get_height() // 5 * 3
        sep = size[1] + 40
        botoes = [
            Botao(self.screen, Jogo, ('center', centery-sep), size, 'Jogar', font_size),
            Botao(self.screen, MenuNaves, ('center', centery), size, 'Naves', font_size),
            Botao(self.screen, None, ('center', centery+sep), size, 'Sair', font_size)
        ]
        return botoes

    def run(self):
        
        self.titulo.atualizarCor()
        self.titulo.update()
        self.titulo.exibir()

        for botao in self.botoes:
            botao.exibir()

    def loadEvent(self, event) -> Literal['sair'] | Union["Jogo", "MenuNaves"] | None:
        for botao in self.botoes:
            botao.hover()    
            if botao.clicked(event):
                if botao.event is None:
                    return 'sair'
                return botao.event