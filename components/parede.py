import pygame
import random

class Fragmento:

    def __init__(self, screen: pygame.Surface, img: pygame.Surface, y: int):
        self.screen = screen
        self.img = img
        self.y = y
        self.mask = self.getMask()
        
        self.velocidade = 3

        self.largura = self.img.get_width()
        self.largura_tela = self.screen.get_width()

    def exibir(self, x):
        self.screen.blit(self.img, (x, self.y))

    def getMask(self):
        return pygame.mask.from_surface(self.img)

class Parede:

    PAREDE_CIMA = 1
    PAREDE_BAIXO = 0

    def __init__(self,
                 screen: pygame.Surface,
                 img: pygame.Surface,
                 x: int
                 ):
        self.screen = screen
        self.img = img
        self.x = x

        self.velocidade = 3
        self.espaco = self.screen.get_height() // 3
        self.y = self.randomY(self.PAREDE_BAIXO)

        self.fragmentos = self.criarParedes()
        self.pontuou = False

    def exibir(self):
        for img in self.fragmentos:
            img.exibir(self.x)

    def atualizarPosicao(self):
        self.x -= self.velocidade
        if self.x  < -self.img.get_width():
            self.x = self.screen.get_width()
            self.pontuou = False


    def criarParedes(self) -> list[Fragmento]:
        '''Retorna os fragmentos das paredes'''
        y = self.y
        altura_tela = self.screen.get_height()
        altura_img = self.img.get_height()
        fragmentos = []
        while y < altura_tela:
            parede = Fragmento(self.screen, self.img, y)
            fragmentos.append(parede)
            y += altura_img
        
        y = self.y - self.espaco - altura_img
        while y > -altura_img:
            parede = Fragmento(self.screen, self.img, y)
            fragmentos.append(parede)
            y -= altura_img
        return fragmentos

    def randomY(self, parede):
        if parede == self.PAREDE_CIMA:
            return random.choice([i for i in range(- self.altura, 0)])
        
        elif parede == self.PAREDE_BAIXO:
            return random.choice([i for i in range(self.espaco, self.screen.get_height())])
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))
    
    def getMask(self, index):
        surface = pygame.Surface(self.fragmentos[index][0].get_size(), pygame.SRCALPHA)
        surface.blit(self.img, (0,0))
        return pygame.mask.from_surface(surface)