import pygame
from typing import Literal

class Botao:

    def __init__(self,
                 screen_size: tuple[int],
                 event: Literal["Jogo", "MenuPrincipal", "MenuNaves", "sair"],
                 coord: tuple[int, int],
                 size: tuple[int, int],
                 text: str,
                 font_size: int,
                 cor_padrao: tuple[int,int,int] | None = (255,255,255),
                 txt_color: tuple[int,int,int] | None = (0,0,0),
                 cor_hover: tuple[int,int,int] | None = (180,180,180)):
        
        self.screen_size = screen_size
        self.event = event
        if coord is not None:
            if any(p == 'center' for p in coord):
                self.coord = coord
        else:
            self.coord = (0,0)

        self.size = size
        self.text = text
        self.font_size = font_size
        self.cor_padrao = cor_padrao
        self.txt_color = txt_color
        self.cor_hover = cor_hover
        self.cor = self.cor_padrao
        self._update()
        self.rect = self.get_rect()
        
    def update(self):
        '''Atualiza o botão. Caso algo do botão tenha sido modificado (size, text, font_size, etc), 
        a mudança só será aplicada após executar este método. 
        Este método verifica também a posição do mouse. Caso passe por cima do botão, ele atualizará a cor.
        '''

        # Verificar se o mouse está em cima do botão
        if self.hover():
            if self.cor != self.cor_hover:
                self.cor = self.cor_hover
        else:
            if self.cor != self.cor_padrao:
                self.cor = self.cor_padrao
        
        self._update()

    def _update(self):

        # Criar o Surface
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.cor)

        txt = pygame.font.Font(None, self.font_size)
        txt = txt.render(self.text, True, self.txt_color)

        centro = self.surface.get_rect().center
        centro = txt.get_rect(center=centro).topleft
        self.surface.blit(txt, centro)

        x,y = self.coord
        if x == 'center':
            screen_centerx = self.screen_size[0] / 2
            x = self.surface.get_rect(centerx=screen_centerx).left
        
        if y == 'center':
            screen_centery = self.screen_size[1] / 2
            y = self.surface.get_rect(centery=screen_centery).top
        
        self.coord = (x,y)
        self.rect = self.surface.get_rect(topleft=self.coord)


    def exibir(self, screen: pygame.Surface):
        if self.hover():
            self._update()
        screen.blit(self.surface, self.coord)

    def clicked(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover():
                return True
        return False

    def hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def get_event(self):
        return self.event
    
    def get_rect(self, **kwargs):
        return self.surface.get_rect(**kwargs)
    
    def definir_posicao_absoluta(self, **kwargs) -> pygame.Rect:
        self.pos_absoluta = self.get_rect(**kwargs).topleft