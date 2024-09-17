import pygame

class Titulo:
    def __init__(self,
                 screen_size: tuple[int],
                 x: int | str,
                 y: int | str,
                 text: str,
                 color: tuple[int,int,int] | None = (255,255,255),
                 font_size: int | None = 80):
        self.screen_size = screen_size
        self.coord = (x,y)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.update()
        self.velocidade_atual = (0,3,0)

    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        center = (round(self.screen_size[0] / 2), round(self.screen_size[1] / 2))
        x,y = self.coord
        if x == 'center':
            x = self.surface.get_rect(center = center).left
        if y == 'center':
            y = self.surface.get_rect(center = center).top
        self.coord = (x,y)

    def exibir(self, screen: pygame.Surface):
        screen.blit(self.surface, self.coord)

    def atualizar_cor(self):

        velocidades = {
            (255,0,0): (0,3,0),
            (255,255,0): (-3,0,0),
            (0,255,0): (0,0,3),
            (0,255,255): (0,-3,0),
            (0,0,255): (3,0,0),
            (255,0,255): (0,0,-3)
        }

        velocidade = velocidades.get(self.color)

        r,g,b = self.color
        if velocidade:
            r += velocidade[0]
            g += velocidade[1]
            b += velocidade[2]
            self.velocidade_atual = velocidade
        else:
            r += self.velocidade_atual[0]
            g += self.velocidade_atual[1]
            b += self.velocidade_atual[2]

        self.color = (r,g,b)
