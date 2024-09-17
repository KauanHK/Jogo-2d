import pygame
from components.popup import PopUp
from components.titulo import Titulo
from components.botao import Botao
from utils.imagens import carregar_imagem
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


    def update_botoes_game_over(self):
        for botao in self.game_over.botoes:
            botao.update()

        # mouse_pos = pygame.mouse.get_pos()
        # for rect, botao in zip(self.game_over.botoes_rects, self.game_over.botoes):
        #     if rect.collidepoint(mouse_pos):
        #         botao.definir_cor_hover()
        #     else:
        #         botao.definir_cor_padrao()

    def update(self, nave: Nave, nave_mask: pygame.mask.Mask, paredes: Paredes, fragmento_mask: pygame.mask.Mask, pausado: bool):
        self._colidiu = self.colidiu(nave, nave_mask, paredes, fragmento_mask)
        if pausado:
            return
        if self._colidiu:
            self.update_botoes_game_over()
            self.game_over.atualizar_popup()
            if not self.salvo:
                self.pontuacao.salvar_pontuacao(self.pontuacao)
                self.salvo = True
        else:
            nave.update()
            paredes.update()

    def exibir(self, screen: pygame.Surface, nave: Nave, paredes: Paredes, pausado: bool):
        nave.exibir(screen)
        paredes.exibir(screen)
        self.pontuacao.exibir(screen)

        if pausado:
            self.pause.exibir(screen)

        elif self._colidiu:
            self.game_over.exibir(screen)
            self.pontuacao.exibir(self.game_over)

    def colidiu(self, nave: Nave, nave_mask: pygame.mask.Mask, paredes: Paredes, fragmento_mask: pygame.mask.Mask) -> bool:
        nave_x, nave_y = nave.x, nave.y
        for parede in paredes:
            x_fragmento = parede.x
            for y_fragmento in parede.tops:
                fragmento_offset = (x_fragmento - nave_x, y_fragmento - nave_y)
                if nave_mask.overlap(fragmento_mask, fragmento_offset):
                    return True
        return False
    
class Pause:

    def __init__(self):
        pass

class GameOver:

    def __init__(self, screen_size: tuple[int]):
        self.popup = self.criar_popup(screen_size)
        self.titulo = self.criar_titulo(screen_size)
        self.botoes = self.criar_botoes(screen_size)
        # self.botoes_rects = self.definir_rects_botoes()

    def criar_popup(self, screen_size: tuple[int]) -> PopUp:
        '''Retorna um Popup'''
        largura = screen_size[0] * 0.4
        altura = screen_size[1] * 0.7
        size = (largura, altura)
        popup = PopUp(screen_size, size, CINZA_TRANSPARENTE)
        return popup
    
    def criar_titulo(self, screen_size: tuple[int,int]) -> Titulo:
        '''Retorna um Titulo com "Game Over" em vermelho'''
        return Titulo(screen_size, 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes(self, screen_size: tuple[int,int]) -> list[Botao]:
        '''Retorna uma lista de Botao com os botões "Restart" e "Menu"'''
        y = screen_size[1] * 0.6
        coord = ('center', y)
        largura = self.popup.get_width() * 0.7
        altura = self.popup.get_height() * 0.15
        size = (largura, altura)
        botao_restart = Botao(screen_size, "Jogo", coord, size, 'Restart', 40)

        y += altura + 20
        coord = ('center', y)
        botao_sair = Botao(screen_size, "MenuPrincipal", coord, size, 'Menu', 40)
        return botao_restart, botao_sair
    
    def definir_rects_botoes(self):
        rects = []
        for botao in self.botoes:
            x = self.popup.coord[0] + botao.coord[0]
            y = self.popup.coord[1] + botao.coord[1]
            rect = botao.get_rect(topleft = (x,y))
            rects.append(rect)
        return rects

    def exibir_botoes(self, screen: pygame.Surface):
        # self.popup.atualizar()
        # self.popup.blit(self.titulo.surface, self.titulo.coord)
        for botao in self.botoes:
            botao.exibir(screen)

    def exibir(self, screen: pygame.Surface):
        self.popup.exibir(screen)

    def blit(self, surface: pygame.Surface, dest: tuple[int,int]):
        self.popup.blit(surface, dest)


