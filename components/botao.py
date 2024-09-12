import pygame
from typing import Literal

class Botao:

    def __init__(self,
                 screen: pygame.Surface,
                 event: Literal["Jogo", "MenuPrincipal", "MenuNaves"] | None,
                 coord: tuple[int, int],
                 size: tuple[int, int],
                 text: str,
                 font_size: int,
                 back_color: tuple[int,int,int] | None = (255,255,255),
                 txt_color: tuple[int,int,int] | None = (0,0,0),
                 hover_color: tuple[int,int,int] | None = (180,180,180)):
        self.screen = screen
        self.event = event
        if coord is not None:
            if any(p == 'center' for p in coord):
                self.coord = coord
        else:
            self.coord = (0,0)

        self.size = size
        self.text = text
        self.font_size = font_size
        self.back_color = back_color
        self.txt_color = txt_color
        self.hover_color = hover_color

        self.color = self.back_color
        self.atualizarBotao()
        
    def atualizarBotao(self):
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        txt = pygame.font.Font(None, self.font_size)
        txt = txt.render(self.text, True, self.txt_color)

        centro = self.surface.get_rect().center
        centro = txt.get_rect(center=centro).topleft
        self.surface.blit(txt, centro)

        x,y = self.coord
        if x == 'center':
            screen_centerx = self.screen.get_width() / 2
            x = self.surface.get_rect(centerx=screen_centerx).left
        
        if y == 'center':
            screen_centery = self.screen.get_height() / 2
            y = self.surface.get_rect(centery=screen_centery).top
        
        self.coord = (x,y)
        self.rect = self.surface.get_rect(topleft=self.coord)

    def exibir(self):
        self.screen.blit(self.surface, self.coord)

    def clicked(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover():
                return True
        return False

    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
            self.atualizarBotao()
            return True
        self.color = self.back_color
        self.atualizarBotao()
        return False

    def get_event(self):
        return self.event