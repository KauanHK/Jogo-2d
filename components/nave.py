import pygame
from utils.imagens import carregar_imagem, mudar_tamanho

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
        self.img_nave, self.img_fogo = self.carregar_imgs()
        rect_img = self.img_nave.get_rect()
        rect_img.center = self.screen.get_rect().center
        self.x = rect_img.left
        self.y = self.screen.get_rect().centery
        self.y_fogo = self.definir_y_fogo()
        self.velocidade = 3

    def carregar_imgs(self) -> tuple[pygame.Surface]:
        img_nave = carregar_imagem('imagens', f'nave{self.nave}.png')
        largura_original = img_nave.get_width()

        largura = self.screen.get_width()*0.05
        razao = largura_original / largura
        img_nave = mudar_tamanho(img_nave, (largura, 'auto'))

        img_fogo = carregar_imagem('imagens', f'fogo{self.nave}.png')
        largura_original = img_fogo.get_width()
        largura = largura_original / razao
        img_fogo = mudar_tamanho(img_fogo, (largura, 'auto'))

        return img_nave, img_fogo

    def definir_y_fogo(self) -> int:
        altura_img = self.img_nave.get_height()
        y_fogo = [self.y + altura_img, self.y + (3/4) * altura_img, self.y + altura_img, self.y + altura_img/10*9,self.y + altura_img]
        return round(y_fogo[self.nave - 1])

    def atualizarPosicao(self) -> None:
        '''Atualiza self.y'''
        self.y += self.velocidade
        self.y_fogo += self.velocidade

    def mudarDirecao(self, direcao: int) -> None:
        '''Atualiza o valor da velocidade como positiva ou negativa'''
        if direcao:
            self.velocidade = abs(self.velocidade) * direcao
        else:
            self.velocidade *= -1
        
    def exibir(self):
        self.screen.blit(self.img_nave, (self.x, self.y))
        self.soltar_fogo()

    def soltar_fogo(self):
        if self.velocidade < 0:
            x = self.x + (self.img_nave.get_width() - self.img_fogo.get_width()) / 2
            self.screen.blit(self.img_fogo,(x,self.y_fogo))

    def getMask(self):
        return pygame.mask.from_surface(self.img_nave)
    
    def get_rect(self):
        return self.img_nave.get_rect(topleft=(self.x, self.y))