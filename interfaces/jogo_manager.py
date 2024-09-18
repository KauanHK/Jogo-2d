import pygame
from components.nave import Nave
from components.parede import Paredes
from components.titulo import Titulo
from .jogo import Jogo, PopUpGameOver, Pause
from utils.pontuacao import Pontuacao
from utils.cores import *


class JogoManager:

    def __init__(self, screen_size: tuple[int,int]):

        """Gerenciador do jogo. Executa todas as funcionalidades da nave e das paredes 
        e exibe o popup gameover e de pause. Recebe as dimensões da tela como parâmetro."""

        self.screen_size = screen_size

        self.nave = Nave(self.screen_size, 'center', 'center')
        self.paredes = Paredes(self.screen_size)

        self.jogo = Jogo(self.screen_size, self.nave, self.paredes)
        self.game_over = PopUpGameOver(self.screen_size)
        self.pause = Pause(self.screen_size)

        self.nave_mask = self.nave.get_mask()
        self.fragmento_mask = self.paredes.get_mask()

        self.pontuacao = Pontuacao()
        self.titulo_pontuacao = self.criar_titulo_pontuacao()
        self.titulo_recorde = None  # Será criado em 'self.colidiu()' após a colisão

        self._colidiu = False
        self.pausado = False
        self.salvo = False

    def criar_titulo_pontuacao(self):
        return Titulo(self.screen_size, 'center', self.screen_size[1] * 0.1, str(self.pontuacao.pontuacao))

    def criar_titulo_recorde(self):
        return Titulo(self.screen_size, 'center', self.screen_size[1] * 0.4, str(self.pontuacao.get_max_pontuacao()), AQUA, 120)

    def update(self):
        """Atualiza um frame do jogo"""

        if self.pontuou():
            self.pontuacao.add()
            self.titulo_pontuacao.text = str(self.pontuacao.pontuacao)
            self.titulo_pontuacao.update()

        # Verificar se há algum popup ativo
        if self._colidiu or self.colidiu():
            self._colidiu = True
            if not self.salvo:
                self.pontuacao.salvar_pontuacao()
                self.salvo = True
            self.game_over.update()
            self.titulo_pontuacao.coord = ('center', self.screen_size[1] * 0.2)
            self.titulo_pontuacao.update()

        elif self.pausado:
            self.pause.update()

        else:
            self.nave.update()
            self.paredes.update()

    def exibir(self, screen: pygame.Surface):
        """Exibe um frame do jogo. 
        Se estiver pausado, exibe o popup de pause, 
        e se estiver game over, exibe o popup de gameover"""

        # Exibir a nave e as paredes
        self.nave.exibir(screen)
        self.paredes.exibir(screen)
        self.titulo_pontuacao.exibir(screen)

        # # Verificar se há algum popup ativo
        # if self.popup is not None:
        #     self.popup.exibir(screen)
            
        # Verificar se houver alguma colisão
        if self._colidiu or self.colidiu():
            self._colidiu = True
            self.game_over.exibir(screen)
            self.titulo_recorde.exibir(screen)
        elif self.pausado:
            self.pause.exibir(screen)

    def run(self, screen: pygame.Surface):
        self.update()
        self.exibir(screen)

    def load_event(self, event:pygame.event.Event):
        """Carrega um evento."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado

            
        if self._colidiu:
            return self.game_over.load_event(event)
        
        elif self.pausado:
            botao_event = self.pause.load_event(event)
            if botao_event == 'continuar':
                self.pausado = False
            else:
                return botao_event
        
        else:
            self.nave.load_event(event)

    def verificar_colisao(self):
        '''Verificar se houve uma colisão NO FRAME ATUAL. 
        Caso a nave estiver encostada na parede há mais de um frame, retorna False.'''
        if not self._colidiu and self.colidiu():
            self._colidiu = True
            return True
        return False

    def colidiu(self) -> bool:
        """Retorna True se a nave estiver em cima de uma parede, se não False"""
        nave_x, nave_y = self.nave.x, self.nave.y
        for parede in self.paredes:
            x_fragmento = parede.x
            for y_fragmento in parede.tops:
                fragmento_offset = (x_fragmento - nave_x, y_fragmento - nave_y)
                if self.nave_mask.overlap(self.fragmento_mask, fragmento_offset):
                    self.titulo_recorde = self.criar_titulo_recorde()
                    return True
        return False
    
    def pontuou(self):
        for parede in self.paredes:
            if not parede.pontuou and self.nave.x > parede.x:
                parede.pontuou = True
                return True
        return False