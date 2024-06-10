import pygame
import random
import os

# Inicialize o Pygame
pygame.init()

# Crie uma janela de exibição como fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Pegando as dimensões da tela
LARGURA_TELA = screen.get_width()
ALTURA_TELA = screen.get_height()

# Carregar imagens e redimensionar
def carregar_imagem(caminho, largura=None, altura=None):
    imagem = pygame.image.load(caminho)
    if largura and altura:
        imagem = pygame.transform.scale(imagem, (largura, altura))
    return imagem

fundo = carregar_imagem(os.path.join('imagens', 'fund.jpg'), LARGURA_TELA, ALTURA_TELA)
IMAGEM_ROBO = carregar_imagem(os.path.join('imagens', 'nave.png'), int(0.035 * LARGURA_TELA), int(0.035 * ALTURA_TELA))
IMAGEM_PAREDE = carregar_imagem(os.path.join('imagens', 'obstaculo.jpg'))

# Título da janela
pygame.display.set_caption("Robozinho")

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)

# Classe do robô
class Robo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.acelerador = 1.00038
        self.imagem = IMAGEM_ROBO
        self.largura_imagem = self.imagem.get_width()

    def mover_cima(self):
        self.cima = True

    def mover_baixo(self):
        self.cima = False

    def atualizar_posicao(self):
        self.velocidade_y = -abs(self.velocidade_y) * self.acelerador if self.cima else abs(self.velocidade_y) * self.acelerador
        self.y += self.velocidade_y

    def desenhar(self, screen):
        screen.blit(self.imagem, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classe da parede
class Parede:
    def __init__(self, x, id):
        self.x = x
        self.y = random.randint(ALTURA_TELA // 4, ALTURA_TELA // 2)
        self.imagem = pygame.transform.scale(IMAGEM_PAREDE, (LARGURA_TELA // 10, ALTURA_TELA))
        self.velocidade_x = LARGURA_TELA // 400
        self.passou = False
        self.limite = ALTURA_TELA // 5
        self.espaco = ALTURA_TELA * 0.25
        self.id = id

    def atualizar_posicao(self, paredes):
        self.x -= self.velocidade_x
        self.velocidade_x *= 1.0002
        if self.x < -self.imagem.get_width():
            parede_anterior = paredes[self.id - 1]
            self.y = random.randint(parede_anterior.y - self.limite, parede_anterior.y + self.limite)
            self.y = max(self.espaco + 20, min(ALTURA_TELA - self.espaco - 20, self.y))
            self.x = LARGURA_TELA
            self.passou = False

    def desenhar(self, screen):
        screen.blit(self.imagem, (self.x, self.y))
        screen.blit(pygame.transform.flip(self.imagem, False, True), (self.x, self.y - self.espaco - self.imagem.get_height()))

    def colidiu(self, robo):
        robo_mask = robo.get_mask()
        parede_mask = pygame.mask.from_surface(self.imagem)
        offset = (self.x - robo.x, self.y - robo.y)
        if robo_mask.overlap(parede_mask, offset):
            return True
        return False

    def pontuacao(self, robo):
        if not self.passou and self.x + self.imagem.get_width() // 2 < robo.x:
            self.passou = True
            return True
        return False

# Funções do jogo
def criar_objetos():
    robo = Robo((LARGURA_TELA // 2) - (IMAGEM_ROBO.get_width() // 2), ALTURA_TELA // 2)
    paredes = [Parede(LARGURA_TELA + i * (LARGURA_TELA // 4), i) for i in range(4)]
    return robo, paredes

def desenhar_tela(screen, robo, paredes):
    screen.blit(fundo, (0, 0))
    robo.desenhar(screen)
    for parede in paredes:
        parede.desenhar(screen)

def atualizar_posicoes(robo, paredes):
    robo.atualizar_posicao()
    for parede in paredes:
        parede.atualizar_posicao(paredes)

def verificar_colisoes(robo, paredes):
    for parede in paredes:
        if parede.colidiu(robo):
            return True
    return False

def main():
    robo, paredes = criar_objetos()
    clock = pygame.time.Clock()
    pontuacao = 0
    timer = 0
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            robo.mover_cima()
        elif teclas[pygame.K_DOWN]:
            robo.mover_baixo()
        if teclas[pygame.K_ESCAPE]:
            rodando = False

        if not verificar_colisoes(robo, paredes):
            atualizar_posicoes(robo, paredes)
            desenhar_tela(screen, robo, paredes)
            pontuacao += sum(parede.pontuacao(robo) for parede in paredes)
        else:
            rodando = False

        pygame.display.flip()
        clock.tick(60)

    # Game Over screen
    game_over(screen, pontuacao)

def game_over(screen, pontuacao):
    fonte = pygame.font.SysFont('Arial', 64)
    texto = fonte.render('Game Over', True, BRANCO)
    screen.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, ALTURA_TELA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

main()
pygame.quit()
