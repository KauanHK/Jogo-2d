import pygame
import csv
import os
from datetime import date
from components.nave import Nave
from components.parede import Paredes
from utils.cores import AQUA, BRANCO
from components.titulo import Titulo
from typing import Literal

class Pontuacao:

    def __init__(self, screen_size: tuple[int,int], pontuacao: int, filename: str = 'pontuacoes.csv'):
        self.pontuacao = pontuacao
        self.filename = filename
        self.criar_tabela()


    def criar_tabela(self):
        with open(self.filename, 'w', newline='') as arq:
            writer = csv.writer(arq)
            writer.writerow(['data', 'pontuacao'])

    def add(self, n: int | None = 1):
        self.pontuacao += n

    def definir_pontuacao(self, pontuacao: int):
        self.pontuacao = pontuacao

    def criar_titulo(self, screen_size: tuple[int,int]) -> Titulo:

        if self.type == 'pont':  # Título da pontuação que aparece durante o jogo
            y = screen_size[1] * 0.1
            txt = str(self.pontuacao)
            cor = BRANCO

        else:  # Título da máxima pontuação que aparece no popup gameover
            y = screen_size[1] * 0.35
            txt = str(self.get_max_pontuacao())
            cor = AQUA

        return Titulo(screen_size, 'center', y, txt, cor, 80)
    

    def update(self, nave: Nave, paredes: Paredes) -> None:
        for parede in paredes:
            if nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True
        self.update_txt_pontuacao()

    def get_max_pontuacao(self):
        pontuacoes = self.carregar_pontuacoes()
        if not len(pontuacoes):
            return 0
        return max(pontuacoes)

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