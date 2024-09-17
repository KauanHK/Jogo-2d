import pygame

class PopUp:
    def __init__(self,
                 screen_size: tuple[int],
                 size: tuple[int,int] | None = (200,200),
                 color: tuple[int,int,int] | None = (255,255,255)):
        self.screen_size = screen_size
        self.size = size
        self.color = color
        self.update()

    def update(self):
        self.interface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.interface.fill(self.color)
        self.coord = self.interface.get_rect(center=self.calcular_centro((0,0), self.screen_size)).topleft

    def calcular_centro(self, coord: tuple[int], dimensoes: tuple[int]):
        x = round(coord[0] + dimensoes[0] / 2)
        y = round(coord[1] + dimensoes[1] / 2)
        return x, y

    def exibir(self, screen: pygame.Surface):
        self.update()
        screen.blit(self.interface, self.coord)

    def blit(self, surface: pygame.Surface, dest: tuple[int,int]):
        self.interface.blit(surface, dest)

    def get_size(self):
        return self.size
    
    def get_width(self):
        return self.interface.get_width()
    
    def get_height(self):
        return self.interface.get_height()