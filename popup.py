import pygame

class PopUp:
    def __init__(self,
                 screen: pygame.Surface,
                 size: tuple[int,int] | None = (200,200),
                 color: tuple[int,int,int] | None = (255,255,255)):
        self.screen = screen
        self.size = size
        self.color = color
        self.atualizar_interface()

    def atualizar_interface(self):
        self.interface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.interface.fill(self.color)
        self.coord = self.interface.get_rect(center=self.screen.get_rect().center).topleft

    def exibir(self):
        self.screen.blit(self.interface, self.coord)

    def blit(self, surface: pygame.Surface, dest: tuple[int,int]):
        self.interface.blit(surface, dest)