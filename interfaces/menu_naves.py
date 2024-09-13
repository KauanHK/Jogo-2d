import pygame
from components.nave import Nave
from components.botao import Botao
from interfaces.menu_principal import MenuPrincipal
from utils.imagens import carregar_imagem, mudar_tamanho
from utils.cores import *

class MenuNaves:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.nave_selecionada = Nave.selecionada
        self.botao_voltar = self.criar_botao_voltar()
        self.IMAGENS = self.carregar_imagens()
        self.surface_naves = self.criar_surface_naves()
        self.coord_surface_naves = self.calcular_coord_surf_naves()
        self.atualizar_surface_naves()
        self.img_rects = self.criar_imgs_rects()


    def criar_botao_voltar(self) -> Botao:
        return Botao(self.screen.get_size(), "MenuPrincipal", ('center', self.screen.get_height()*0.8), (200,70), 'Voltar', 40)

    def carregar_imagens(self) -> list[pygame.Surface]:
        return [carregar_imagem(f'imagens' ,f'nave{i}.png', size=(100,'auto')) for i in range(1,6)]
    
    def criar_surface_naves(self) -> pygame.Surface:
        '''Cria a superfície onde aparecem todas as naves do jogo no menu'''
        size = (self.screen.get_width() * 0.8, 150)
        return pygame.Surface(size, pygame.SRCALPHA)

    def atualizar_surface_naves(self):
        self.surface_naves = self.criar_surface_naves()
        self.fundos = self.criar_fundos_naves()
        self.lefts_fundos = self.calcular_x_fundos()
        self.inserir_imgs_naves_nos_fundos()
        self.inserir_fundos()

    def calcular_coord_surf_naves(self) -> tuple[int]:
        x = self.surface_naves.get_rect(center = self.screen.get_rect().center).left
        y = self.screen.get_height() * 0.5
        return x,y
    
    def criar_fundos_naves(self) -> list[pygame.Surface]:
        '''Retorna uma lista de Surface's que correspondem ao fundo das imagens das naves.
        Um fundo é cinza transparente, correspondente à nave que está selecionada.'''
        fundos = []
        for i in range(len(self.IMAGENS)):
            fundo = pygame.Surface((150,150), pygame.SRCALPHA)
            if self.nave_selecionada == i+1:
                fundo.fill(CINZA_TRANSPARENTE)
            fundos.append(fundo)
        return fundos
    
    def calcular_x_fundos(self) -> list[int]:
        coords = []
        largura_surface = self.surface_naves.get_width()
        num_imgs = len(self.IMAGENS)
        x_aumento = largura_surface / (num_imgs - 1)
        for i, fundo in enumerate(self.fundos):
            x = x_aumento * i - fundo.get_width() / 2
            if x < 0:
                x = 0
            elif x + fundo.get_width() > largura_surface:
                x = largura_surface - fundo.get_width()
            coords.append(x)
        return coords

    def hover_naves(self, fundos: list[pygame.Surface]):
        y = self.coord_surface_naves[1]
        mouse_pos = pygame.mouse.get_pos()
        imgs = []
        for x, img_nave in zip(self.lefts_fundos, fundos):
            if img_nave.get_rect(topleft = (x, y)).collidepoint(mouse_pos):
                size = img_nave.get_size()
                if size[0] < self.IMAGENS[0].get_width() * 1.5:
                    size = (s * 1.05 for s in size)
                img_nave = mudar_tamanho(img_nave, size)
            imgs.append(img_nave)
        return imgs

    def inserir_imgs_naves_nos_fundos(self) -> None:
        '''Insere as imagens das naves nos seus fundos. Retorna None'''
        imgs_naves = self.hover_naves(self.IMAGENS)
        for fundo, img_nave in zip(self.fundos, imgs_naves):
            x,y = img_nave.get_rect(center = fundo.get_rect().center).topleft
            fundo.blit(img_nave, (x,y))
    
    def criar_imgs_rects(self) -> list[pygame.Rect]:
        '''Cria a lista self.img_rects, que armazena os Rect's de todas as imagens das naves. 
        Depende do Surface self.coord_surface_naves, que deve ser criado antes de executar este método.'''
        y = self.coord_surface_naves[1]
        rects = []
        for fundo, left in zip(self.fundos, self.lefts_fundos):
            x = self.coord_surface_naves[0] + left
            rect = fundo.get_rect(topleft = (x, y))
            rects.append(rect)
        return rects

    def inserir_fundos(self):
        for x, fundo in zip(self.lefts_fundos, self.fundos):
            self.surface_naves.blit(fundo, (x,0))
            

    def exibir_naves(self) -> None:
        self.screen.blit(self.surface_naves, self.coord_surface_naves)

    def run(self) -> None:
        self.botao_voltar.exibir()
        if self.nave_selecionada != Nave.selecionada:
            self.nave_selecionada = Nave.selecionada
            self.atualizar_surface_naves()
        self.exibir_naves()
    
    
    def loadEvent(self, event: pygame.event.Event) -> MenuPrincipal | None:
        self.botao_voltar.hover()
        if self.botao_voltar.clicked(event):
            return self.botao_voltar.get_event()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, nave_rect in enumerate(self.img_rects):
                if nave_rect.collidepoint(event.pos):
                    Nave.selecionada = i+1
                    break