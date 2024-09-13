import pygame
import random

class Fragmento:

    def __init__(self, img: pygame.Surface):
        self.img = img

    def exibir(self, screen: pygame.Surface, coord: tuple[int]):
        screen.blit(self.img, coord)

class Parede:

    PAREDE_CIMA = 1
    PAREDE_BAIXO = 0

    def __init__(self,
                 screen_size: tuple[int],
                 img: pygame.Surface,
                 x: int
                 ):
        self.screen_size = screen_size
        self.img = img
        self.x = x
        self.espaco = round(self.screen_size[1] / 3)
        self.y = self.randomY()
        self.altura_cima = self.calcular_altura(True)
        self.altura_baixo = self.calcular_altura()

        self.velocidade = 3

        self.fragmento = Fragmento(self.img)
        self.tops = self.calcular_tops()
        self.pontuou = False

    def calcular_altura(self, cima: bool = False):
        if cima:
            return self.y + self.img.get_height()
        return self.screen_size[1] - self.y - self.espaco + self.img.get_height()

    def calcular_tops(self):
        altura_img = self.img.get_height()
        tops = []
        y = self.y
        while y < self.screen_size[1] + altura_img:
            tops.append(y)
            y += altura_img
        y = self.y - self.espaco - altura_img
        while y > - altura_img:
            tops.append(y)
            y -= altura_img
        return tops

    def exibir(self, screen: pygame.Surface):
        for y in self.tops:
            self.fragmento.exibir(screen, (self.x, y))

    def atualizarPosicao(self):
        self.x -= self.velocidade
        if self.x  < -self.img.get_width():
            self.x = self.screen_size[0]
            self.pontuou = False


    def criar_fragmentos(self) -> list[Fragmento]:
        '''Retorna os fragmentos das paredes'''
        y = self.y
        altura_tela = self.screen_size[1]
        altura_img = self.img.get_height()

        fragmentos = []
        while y < altura_tela:
            fragmento = Fragmento(self.img, y)
            fragmentos.append(fragmento)
            y += altura_img
        
        y = self.y - self.espaco - altura_img
        while y > -altura_img:
            fragmento = Fragmento(self.img, y)
            fragmentos.append(fragmento)
            y -= altura_img

        return fragmentos

    def randomY(self):
        return random.randint(self.espaco+20, self.screen_size[1]-20)
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))
    
    def getMask(self):
        return pygame.mask.from_surface(self.img)