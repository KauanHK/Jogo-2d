import pygame
from components.nave import Nave
from components.botao import Botao
from components.titulo import Titulo
from interfaces.menu_principal_manager import MenuPrincipalManager
from utils.imagens import carregar_imagem, mudar_tamanho
from utils.cores import *

class MenuNaves:

    def __init__(self, screen_size: tuple[int,int]):
        self.screen_size = screen_size

        self.titulo = self.criar_titulo(self.screen_size)
        self.imagens = self.carregar_imagens()
        self.fundo_nave = self.criar_fundo()
        self.centers_fundos = self.calcular_coords_fundos(self.screen_size)
        self.botao_voltar = self.criar_botao_voltar(self.screen_size)

    def criar_titulo(self, screen_size: tuple[int,int]):
        return Titulo(screen_size, 'center', screen_size[1]*0.2, 'Selecione uma Nave')

    def carregar_imagens(self) -> list[pygame.Surface]:
        return [carregar_imagem(f'imagens' ,f'nave{i}.png', size=(100,'auto')) for i in range(1,6)]

    def criar_fundo(self):
        fundo = pygame.Surface((150,150), pygame.SRCALPHA)
        fundo.fill(CINZA_TRANSPARENTE)
        return fundo

    def calcular_coords_fundos(self, screen_size: tuple[int,int]) -> list[int]:
        coords = [None for i in range(5)]
        largura = self.fundo_nave.get_width()

        coords[0] = screen_size[0] * 0.1 + largura//2           # Primeiro
        coords[4] = (screen_size[0] * 0.9) - largura//2         # Último
        coords[2] = screen_size[0] // 2             # Meio
        coords[1] = (coords[0] + coords[2]) // 2      # Segundo
        coords[3] = (coords[2] + coords[4]) // 2      # Penúltimo

        y = screen_size[1] * 0.75 - (self.fundo_nave.get_height() // 2)
        coords = [(x, y) for x in coords]
        return coords

    def criar_botao_voltar(self, screen_size: tuple[int,int]) -> Botao:
        return Botao(screen_size, "MenuPrincipal", ('center', screen_size[1]*0.8), (200,70), 'Voltar', 40)
    
    def exibir_naves(self, screen: pygame.Surface) -> None:
        for i, coord in enumerate(self.centers_fundos):

            # Se a nave estiver selecionada, exibir o fundo cinza
            x,y = self.fundo_nave.get_rect(center = coord).topleft
            if Nave.selecionada == i+1:
                screen.blit(self.fundo_nave, (x,y))

            # Exibir a nave no centro do fundo
            x,y = self.imagens[i].get_rect(center = coord).topleft
            screen.blit(self.imagens[i], (x,y))

    def exibir(self, screen: pygame.Surface):
        self.titulo.exibir(screen)
        self.exibir_naves(screen)
        self.botao_voltar.exibir(screen)

    def load_event(self, event: pygame.event.Event) -> MenuPrincipalManager | None:
        if self.botao_voltar.clicked(event):
            return self.botao_voltar.get_event()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rects = [nave.get_rect(center = center) for nave, center in zip(self.imagens, self.centers_fundos)]
            for i, rect in enumerate(rects):
                if rect.collidepoint(event.pos):
                    Nave.selecionada = i + 1

    def update(self):
        self.botao_voltar.update()
        