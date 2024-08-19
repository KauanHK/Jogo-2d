import pygame

class Titulo:
    def __init__(self,
                 screen: pygame.Surface,
                 x: int | str,
                 y: int | str,
                 text: str,
                 color: tuple[int,int,int] | None = (255,255,255),
                 font_size: int | None = 80):
        self.titulo = None
        self.screen = screen
        self.coord = (x,y)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.update()
        self.velocidade_atual = (0,3,0)

    def update(self):
        self.titulo = self.font.render(self.text, True, self.color)
        x,y = self.coord
        if x == 'center':
            x = self.titulo.get_rect(center=self.screen.get_rect().center).left
        if y == 'center':
            y = self.titulo.get_rect(center=self.screen.get_rect().center).top
        self.coord = (x,y)

    def exibir(self):
        self.update()
        self.screen.blit(self.titulo, self.coord)

    def atualizarCor(self):

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
