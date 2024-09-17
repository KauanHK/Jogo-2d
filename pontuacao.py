import pygame
import csv
import os
from datetime import date
from components.nave import Nave
from components.parede import Paredes
from utils.cores import AQUA, BRANCO

class Pontuacao:

    def __init__(self, filename: str = 'pontuacoes.csv'):
        self.filename = filename
        self.pontuacao = 0
        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)

    def update(self, nave: Nave, paredes: Paredes) -> None:
        for parede in paredes:
            if nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True

    @property
    def max_pontuacao(self):
        pontuacoes = self.carregar_pontuacoes()
        if not len(pontuacoes):
            return 0
        return max(pontuacoes)

    def criar_tabela(self):
        with open(self.filename, 'w', newline='') as arq:
            writer = csv.writer(arq)
            writer.writerow(['data', 'pontuacao'])

    def carregar_pontuacoes(self) -> list[int]:
        if not os.path.exists(self.filename):
            self.criar_tabela()

        with open(self.filename, 'r') as arq:
            reader = csv.DictReader(arq)
            return [int(linha['pontuacao']) for linha in reader]

    def salvar_pontuacao(self, pontuacao: int) -> None:
        if not os.path.exists(self.filename):
            self.criar_tabela()
        with open(self.filename, 'a', newline='') as arq:
            writer = csv.writer(arq)
            writer.writerow([date.today(), pontuacao])

    def criar_txt_pontuacoes(self) -> tuple[pygame.Surface, pygame.Surface]:
        pontuacao = self.font2.render(str(self.pontuacao), True, AQUA)
        max_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, BRANCO)
        return pontuacao, max_pontuacao
    
    def exibir(self, screen: pygame.Surface) -> None:

        txt_pontuacao, txt_max_pontuacao = self.criar_txt_pontuacoes()
        coord = self.calcular_coords_pontuacao(screen, txt_pontuacao)
        screen.blit(txt_pontuacao, coord)
        # self.game_over.popup.interface.blit(txt_pontuacao, (x,y))

        x = txt_max_pontuacao.get_rect(center = txt_pontuacao.get_rect().center).left
        y = coord[1] + txt_pontuacao.get_height() + 20
        screen.blit(txt_max_pontuacao, (x,y))

    def exibir_pontuacao(self, screen: pygame.Surface, pontuacao: str | int):
        txt_pontuacao = self.font.render(str(pontuacao), True, BRANCO)
        x = (screen.get_width() - txt_pontuacao.get_width()) / 2
        y = 100
        screen.blit(txt_pontuacao, (x,y))

    def calcular_coords_pontuacao(self, screen: pygame.Surface, txt_pontuacao: pygame.Surface) -> tuple[int,int]:  # txt_pontuacao: pygame.Surface
        return txt_pontuacao.get_rect(center = screen.get_rect().center).topleft
        x = txt_pontuacao.get_rect(center = self.game_over.popup.interface.get_rect().center).left
        y = self.game_over.titulo.coord[1] + self.game_over.titulo.surface.get_height() + 20
        return x,y