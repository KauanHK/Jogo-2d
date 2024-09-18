import pygame
from utils.imagens import carregar_imagem, mudar_tamanho
from typing import Literal

class Nave:

    CIMA = -1
    BAIXO = 1
    ESPACO = 0
    selecionada = 1

    def __init__(self,
                 screen_size: tuple[int],
                 x: int | Literal['center'],
                 y: int | Literal['center'],
                 nave: int | None = None
                 ):
        '''Cria uma instância de Nave.
        
        Parâmetros
        ------------
            screen_size : tuple[int]
            As dimensões da tela onde será inserida a nave. Use screen.get_size().
        '''

        self.screen_size = screen_size
        self.x = x
        self.y = y
        self.nave = nave if nave is not None else Nave.selecionada
        self.img_nave, self.img_fogo = self.carregar_imgs()
        if self.x == 'center':
            self.x = self.calcular_centro(0)
        if self.y == 'center':
            self.y = self.calcular_centro(1)
        self.y_fogo = self.definir_y_fogo()
        self.velocidade = -3

    def carregar_imgs(self) -> tuple[pygame.Surface]:
        '''Retorna, respectivamente, as imagens da nave e do fogo'''
        img_nave = carregar_imagem('imagens', f'nave{self.nave}.png')
        largura_original = img_nave.get_width()

        largura = self.screen_size[0]*0.05
        razao = largura_original / largura
        img_nave = mudar_tamanho(img_nave, (largura, 'auto'))

        img_fogo = carregar_imagem('imagens', f'fogo{self.nave}.png')
        largura_original = img_fogo.get_width()
        largura = largura_original / razao
        img_fogo = mudar_tamanho(img_fogo, (largura, 'auto'))

        return img_nave, img_fogo
    
    def calcular_centro(self, axis: int) -> int:
        center = self.screen_size[axis] / 2
        if axis == 0:
            return self.img_nave.get_rect(centerx = center).left
        return self.img_nave.get_rect(centery = center).top

    def definir_y_fogo(self) -> int:
        '''Define a coordenada y da imagem do fogo'''
        altura_img = self.img_nave.get_height()
        y_fogo = [self.y + altura_img, self.y + (3/4) * altura_img, self.y + altura_img, self.y + altura_img/10*9,self.y + altura_img]
        return round(y_fogo[self.nave - 1])

    def update(self) -> None:
        '''Atualiza o y da nave'''
        self.y += self.velocidade
        self.y_fogo += self.velocidade

    def load_event(self, event: pygame.event.Event):
        '''Carrega um evento. Verificar apenas se foi clicada a seta para cima, baixo, w, s ou ou espaço.'''
        if event.type == pygame.KEYDOWN:

            if event.key in [pygame.K_UP, pygame.K_w]:
                self.velocidade = abs(self.velocidade) * -1

            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.velocidade = abs(self.velocidade)

            elif event.key == pygame.K_SPACE:
                self.velocidade = - self.velocidade

    def exibir(self, screen: pygame.Surface):
        '''Exibe a nave e o fogo se a nave estiver subindo'''
        screen.blit(self.img_nave, (self.x, self.y))
        self.soltar_fogo(screen)

    def soltar_fogo(self, screen: pygame.Surface):
        '''Exibe o fogo se a nave estiver subindo, caso contrário não exibe'''
        if self.velocidade < 0:
            x = self.x + (self.img_nave.get_width() - self.img_fogo.get_width()) / 2
            screen.blit(self.img_fogo,(x,self.y_fogo))

    def get_mask(self):
        '''Retorna o Mask da imagem da nave'''
        return pygame.mask.from_surface(self.img_nave)
    
    def get_rect(self):
        '''Retorna o Rect da nave com sua respectiva coordenada'''
        return self.img_nave.get_rect(topleft=(self.x, self.y))