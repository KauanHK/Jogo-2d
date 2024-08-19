import pygame
import random
from imagens import carregar_imagem

class Nave:

    CIMA = -1
    BAIXO = 1
    ESPACO = 0
    selecionada = 1

    def __init__(self,
                 screen: pygame.Surface,
                 ):
        
        self.screen = screen
        self.img = carregar_imagem('imagens', f'nave{Nave.selecionada}.png', size=(self.screen.get_width()*0.05, 'auto'))

        rect_img = self.img.get_rect()
        rect_img.center = self.screen.get_rect().center
        self.x = rect_img.left
        self.y = self.screen.get_rect().centery
        self.velocidade = 3
    
    def atualizarPosicao(self):
        self.y += self.velocidade

    def mudarDirecao(self, direcao: int):
        if direcao:
            self.velocidade = abs(self.velocidade) * direcao
        else:
            self.velocidade *= -1
        
    def exibir(self):
        self.screen.blit(self.img, (self.x, self.y))

    def getMask(self):
        return pygame.mask.from_surface(self.img)
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))

class Parede:

    PAREDE_CIMA = 1
    PAREDE_BAIXO = 0

    class Imagem:

        def __init__(self, screen: pygame.Surface, img: pygame.Surface, y: int):
            self.screen = screen
            self.img = img
            self.y = y
            
            self.velocidade = 3

            self.largura = self.img.get_width()
            self.largura_tela = self.screen.get_width()

        def exibir(self, x):
            self.screen.blit(self.img, (x, self.y))

        def getMask(self):
            return pygame.mask.from_surface(self.img)

    def __init__(self,
                 screen: pygame.Surface,
                 img: pygame.Surface,
                 x: int
                 ):
        self.screen = screen
        self.img = img
        self.x = x

        self.largura_tela, self.altura_tela = self.screen.get_size()
        self.largura, self.altura = self.img.get_size()
        self.velocidade = 3
        self.espaco = self.altura_tela // 3
        self.y = self.randomY(self.PAREDE_BAIXO)

        self.all_paredes = self.criarParedes()
        self.pontuou = False


    def exibir(self):
        for img in self.all_paredes:
            img.exibir(self.x)

    def atualizarPosicao(self):
        self.x -= self.velocidade
        if self.x  < -self.largura:
            self.x = self.largura_tela
            self.pontuou = False

    def criarParedes(self):
        y = self.y
        paredes = []
        while y < self.altura_tela:
            parede = self.Imagem(self.screen, self.img, y)
            paredes.append(parede)
            y += self.altura
        
        y = self.y - self.espaco - self.altura
        while y > -self.altura:
            parede = self.Imagem(self.screen, self.img, y)
            paredes.append(parede)
            y -= self.altura
        
        return paredes

    def randomY(self, parede):
        if parede == self.PAREDE_CIMA:
            return random.choice([i for i in range(- self.altura, 0)])
        
        elif parede == self.PAREDE_BAIXO:
            return random.choice([i for i in range(self.espaco, self.altura_tela)])
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))
    
    def getMask(self, index):
        surface = pygame.Surface(self.all_paredes[index][0].get_size(), pygame.SRCALPHA)
        surface.blit(self.img, (0,0))
        return pygame.mask.from_surface(surface)