import pygame
import random
from imagens import carregar_imagem, mudar_tamanho

class Nave:

    CIMA = -1
    BAIXO = 1
    ESPACO = 0
    selecionada = 1

    def __init__(self,
                 screen: pygame.Surface,
                 ):
        
        self.screen = screen
        self.nave = Nave.selecionada
        self.carregar_imgs()
        rect_img = self.img_nave.get_rect()
        rect_img.center = self.screen.get_rect().center
        self.x = rect_img.left
        self.y = self.screen.get_rect().centery
        self.y_fogo = self.definir_y_fogo()
        self.velocidade = 3

    def carregar_imgs(self):
        self.img_nave = carregar_imagem('imagens', f'nave{self.nave}.png')
        # razao_img_nave = self.img_nave.get_width() / self.img_nave.get_height()
        largura_original = self.img_nave.get_width()

        largura = self.screen.get_width()*0.05
        razao = largura_original / largura
        self.img_nave = mudar_tamanho(self.img_nave, (largura, 'auto'))

        self.img_fogo = carregar_imagem('imagens', f'fogo{self.nave}.png')
        largura_original = self.img_fogo.get_width()
        largura = largura_original / razao
        self.img_fogo = mudar_tamanho(self.img_fogo, (largura, 'auto'))

    def carregar_img_fogo(self):
        pass
        largura = None
        self.img_fogo = carregar_imagem('imagens', f'fogo{self.nave}.png', size = (self.img_nave.get_width(), 'auto'))

    def definir_y_fogo(self):
        altura_img = self.img_nave.get_height()
        y_fogo = [self.y + altura_img, self.y + (3/4) * altura_img, self.y + altura_img, self.y + altura_img/10*9,self.y + altura_img]
        return y_fogo[self.nave - 1]

    def atualizarPosicao(self):
        self.y += self.velocidade
        self.y_fogo += self.velocidade

    def mudarDirecao(self, direcao: int):
        if direcao:
            self.velocidade = abs(self.velocidade) * direcao
        else:
            self.velocidade *= -1
        
    def exibir(self):
        self.screen.blit(self.img_nave, (self.x, self.y))
        self.soltar_fogo()

    def soltar_fogo(self):
        self.screen.blit(self.img_fogo,(self.x,self.y_fogo))

    def getMask(self):
        return pygame.mask.from_surface(self.img_nave)
    
    def get_rect(self):
        return self.img_nave.get_rect(topleft=(self.x, self.y))

class Fragmento:

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
            y -= altura_img
        
        y = self.y - self.espaco - self.altura
        while y > -altura_img:
            parede = Fragmento(self.screen, self.img, y)
            fragmentos.append(parede)
            y -= altura_img
        return fragmentos

    def randomY(self, parede):
        if parede == self.PAREDE_CIMA:
            return random.choice([i for i in range(- self.altura, 0)])
        
        elif parede == self.PAREDE_BAIXO:
            return random.choice([i for i in range(self.espaco, self.altura_tela)])
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))
    
    def getMask(self, index):
        surface = pygame.Surface(self.fragmentos[index][0].get_size(), pygame.SRCALPHA)
        surface.blit(self.img, (0,0))
        return pygame.mask.from_surface(surface)