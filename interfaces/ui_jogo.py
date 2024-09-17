import pygame
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from pontuacao import Pontuacao
from utils.cores import *
from components.nave import Nave
from components.parede import Paredes

class Interface:

    def __init__(self, screen_size: tuple[int]):
        self.pause = GameOver.criar_popup(Pause, screen_size)
        self.game_over = GameOver(screen_size)

        self.pontuacao = Pontuacao()
        self.salvo = False
        self._colidiu = False
        self.pausado = False


    def update_botoes_game_over(self):
        for botao in self.game_over.botoes:
            botao.update()

    def update(self):
        if self.pausado:
            self.pause.update()
        
        if self._colidiu:
            self.update_botoes_game_over()
            self.game_over.atualizar_popup()
            if not self.salvo:
                self.pontuacao.salvar_pontuacao(self.pontuacao)
                self.salvo = True

    def exibir(self, screen: pygame.Surface):
        self.pontuacao.exibir(screen)

        if self.pausado:
            self.pause.exibir(screen)

        elif self._colidiu:
            self.game_over.exibir(screen)
            self.pontuacao.exibir(self.game_over)

    

    
    

class GerenciadorJogo:

    def __init__(self, screen_size: tuple[int,int]):
        self.nave = Nave(screen_size, 'center', 'center')
        self.paredes = Paredes(screen_size)
        self.pontuacao = Pontuacao(screen_size, 0)
        self.nave_mask = self.nave.get_mask()
        self.fragmento_mask = self.paredes.get_mask()
        # self._colidiu = False
        # self.game_over = None

    def update(self):
        self.nave.update()
        self.paredes.update()
        self.pontuacao.update(self.nave, self.paredes)
        
    def exibir(self, screen: pygame.Surface):
        self.nave.exibir(screen)
        self.paredes.exibir(screen)
        self.pontuacao.exibir(screen)

    def load_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado
        
        self.nave.load_event(event)


    def colidiu(self) -> bool:
        nave_x, nave_y = self.nave.x, self.nave.y
        for parede in self.paredes:
            x_fragmento = parede.x
            for y_fragmento in parede.tops:
                fragmento_offset = (x_fragmento - nave_x, y_fragmento - nave_y)
                if self.nave_mask.overlap(self.fragmento_mask, fragmento_offset):
                    return True
        return False


class Pause:

    def __init__(self):
        pass

    def update(self):
        pass

class GameOver:

    def __init__(self, screen_copy: pygame.Surface, pontuacao: int):
        self.screen_copy = screen_copy
        screen_size = screen_copy.get_size()
        self.popup = self.criar_popup(screen_size)
        self.titulo = self.criar_titulo(screen_size)
        self.botoes = self.criar_botoes(screen_size)
        self.max_pontuacao = Pontuacao(screen_size, pontuacao)


    def update_max_pontuacao(self):
        self.max_pontuacao.x = 'center'
        self.max_pontuacao.y = 'center'
        self.max_pontuacao.update_txt_pontuacao()

    def criar_popup(self, screen_size: tuple[int]) -> PopUp:
        '''Retorna um Popup'''
        largura = screen_size[0] * 0.4
        altura = screen_size[1] * 0.7
        size = (largura, altura)
        popup = PopUp(screen_size, size, CINZA_TRANSPARENTE)
        return popup
    
    def criar_titulo(self, screen_size: tuple[int,int]) -> Titulo:
        '''Retorna um Titulo com "Game Over" em vermelho'''
        return Titulo(screen_size, 'center', screen_size[1] * 0.2, 'Game Over', VERMELHO, 100)

    def criar_botoes(self, screen_size: tuple[int,int]) -> list[Botao]:
        '''Retorna uma lista de Botao com os botões "Restart" e "Menu"'''
        y = screen_size[1] * 0.5
        coord = ('center', y)
        largura = self.popup.get_width() * 0.7
        altura = self.popup.get_height() * 0.15
        size = (largura, altura)
        botao_restart = Botao(screen_size, "Jogo", coord, size, 'Restart', 40)

        y += altura + 20
        coord = ('center', y)
        botao_sair = Botao(screen_size, "MenuPrincipal", coord, size, 'Menu', 40)
        return botao_restart, botao_sair
    
    def botoes_update(self):
        for botao in self.botoes:
            botao.update()

    def exibir_botoes(self, screen: pygame.Surface):
        for botao in self.botoes:
            botao.exibir(screen)

    def update(self):
        self.popup.update()
        self.titulo.update()
        self.botoes_update()
        self.update_max_pontuacao()

    def exibir(self, screen: pygame.Surface):
        screen.blit(self.screen_copy, (0,0))
        self.popup.exibir(screen)
        self.titulo.exibir(screen)
        self.exibir_botoes(screen)
        self.max_pontuacao.exibir(screen)

    def load_event(self, event):
        for botao in self.botoes:
            if botao.clicked(event):
                return botao.get_event()

    def blit(self, surface: pygame.Surface, dest: tuple[int,int]):
        self.popup.blit(surface, dest)


