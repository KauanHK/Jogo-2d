import pygame
import random
import os

# Inicialize o Pygame
pygame.init()

# Crie uma janela de exibição como fullscreen
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

# Pegando as dimensões da tela
LARGURA_TELA = screen.get_width()
ALTURA_TELA = screen.get_height()

# Título da janela
pygame.display.set_caption("Robozinho")

# Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
cinza = (200, 200, 200)

# Definindo as imagens
IMAGEM_ROBO = pygame.image.load(os.path.join("imagens","nave.png"))
IMAGEM_ROBO = pygame.transform.scale_by(IMAGEM_ROBO,0.035)
LARGURA_IMAGEM_ROBO = IMAGEM_ROBO.get_width()

IMAGEM_PAREDE = pygame.image.load(os.path.join("imagens","NicePng_pipes-png_388476.png"))
IMAGEM_PAREDE = pygame.transform.scale_by(IMAGEM_PAREDE,0.35)
IMAGEM_PAREDE_VERTICAL = IMAGEM_PAREDE
IMAGEM_PAREDE_HORIZONTAL = pygame.transform.rotate(IMAGEM_PAREDE_VERTICAL,90)

# IMAGEM_FUNDO = pygame.image.load(os.path.join("imagens","transferir.jpg"))
# IMAGEM_FUNDO = pygame.transform.scale(IMAGEM_FUNDO, (LARGURA_TELA,ALTURA_TELA))
# IMAGEM_FUNDO.set_alpha(128)

# Dimensões da imagem da parede
LARGURA_IMAGEM_PAREDE = IMAGEM_PAREDE.get_width()
ALTURA_IMAGEM_PAREDE = IMAGEM_PAREDE.get_height()

# Classe do robô
class Robo:

    IMAGEM_ROBO = IMAGEM_ROBO
    LARGURA_IMAGEM_ROBO = LARGURA_IMAGEM_ROBO
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.acelerador = 1.00038
    
    def moverCima(self):
        self.cima = True
    def moverBaixo(self):
        self.cima = False
    
    def atualizar_posicao(self):
        if self.cima:
            self.velocidade_y = - abs(self.velocidade_y) * self.acelerador
        else: 
            self.velocidade_y = abs(self.velocidade_y) * self.acelerador
    
        self.y += self.velocidade_y

    
    def desenhar(self,screen):
        screen.blit(self.IMAGEM_ROBO,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.IMAGEM_ROBO)
    
# Classe da parede
class Parede:

    IMAGEM_PAREDE = IMAGEM_PAREDE
    ALTURA_TELA = ALTURA_TELA
    LARGURA_TELA = LARGURA_TELA
    LARGURA_IMAGEM_PAREDE = LARGURA_IMAGEM_PAREDE
    ALTURA_IMAGEM_PAREDE = ALTURA_IMAGEM_PAREDE
    IMAGEM_PAREDE_HORIZONTAL = IMAGEM_PAREDE_HORIZONTAL
    IMAGEM_PAREDE_VERTICAL = IMAGEM_PAREDE_VERTICAL

    def __init__(self,x,horizontal=False,infinita=False):
        self.x = x
        self.horizontal = horizontal
        self.infinita = infinita

        self.y = random.choice([i for i in range(ALTURA_TELA//2-100,ALTURA_TELA//2+100)])
        # self.y = random.choice([i for i in range(ALTURA_TELA)])
        self.imagem = IMAGEM_PAREDE_VERTICAL
        self.imagem_rotacionada = pygame.transform.rotate(self.imagem,180)
        self.velocidade_x = LARGURA_TELA // 400
        self.passou = False
        self.limite = 200
        self.espaco = 200
    
    def atualizar_posicao(self):
        self.x -= self.velocidade_x
        if self.x < - LARGURA_IMAGEM_PAREDE:
            self.passou = False
            self.x = LARGURA_TELA

            self.y = random.choice([i for i in range(self.y - self.limite,self.y + self.limite)])

            self.limite += 1
            self.espaco += 1

            # Obstáculo muito baixo
            if self.y > ALTURA_TELA - 20:
                self.y = ALTURA_TELA - 20
            
            # Obstáculo muito alto (Embaixo)
            elif self.y < ALTURA_TELA - ALTURA_IMAGEM_PAREDE:
                self.y = ALTURA_IMAGEM_PAREDE

            # # Obstáculo 
            # elif self.y < 220 - ALTURA_IMAGEM_PAREDE:
            #     self.y = ALTURA_IMAGEM_PAREDE
        self.velocidade_x *= 1.0002
                

    def desenhar(self,screen):
        screen.blit(self.imagem,(self.x,self.y))
        screen.blit(self.imagem_rotacionada,(self.x,self.y-ALTURA_IMAGEM_PAREDE-self.espaco))

    def colidiu(self,robo,largura_robo):
        min = (LARGURA_TELA // 2) - LARGURA_IMAGEM_PAREDE - (largura_robo // 2)
        max = (LARGURA_TELA // 2) + largura_robo // 2
        if self.x > min and self.x < max:
            robo_mask = robo.get_mask()

            cano_base_mask = pygame.mask.from_surface(self.imagem)
            cano_topo_mask = pygame.mask.from_surface(self.imagem_rotacionada)

            distancia_base = (round(self.x - robo.x),round(self.y - robo.y))
            distancia_topo = (round(self.x - robo.x),round(self.y-ALTURA_IMAGEM_PAREDE-self.espaco - robo.y))

            if robo_mask.overlap(cano_base_mask,distancia_base) or robo_mask.overlap(cano_topo_mask,distancia_topo):
                return True
            return False

    def pontuacao(self,robo):
        if not self.passou and robo.x >= self.x and robo.x <= self.x + LARGURA_IMAGEM_PAREDE:
            self.passou = True
            return True
        return False
        



def desenhar_tela(screen,robo,paredes,timer):
    # Background preto
    screen.fill(preto)
    # screen.blit(IMAGEM_FUNDO,(0,0))
    robo.atualizar_posicao()
    robo.desenhar(screen)

    for parede in paredes:
        parede.atualizar_posicao()
        parede.desenhar(screen)

    timer_text = fonte.render("{:.2f}".format(timer), True, branco)
    x = LARGURA_TELA / 2 - (timer_text.get_width() / 2)
    y = 100
    screen.blit(timer_text,(x,y))

def verificar_colisao(robo,paredes):
    for parede in paredes:
        if parede.colidiu(robo,LARGURA_IMAGEM_ROBO):
            return True
    return False

def verificar_teclas(robo):
    teclas = pygame.key.get_pressed()
    # Seta para cima
    if teclas[pygame.K_UP]:
        robo.moverCima()

    # Seta para baixo
    elif teclas[pygame.K_DOWN]:
        robo.moverBaixo()
    
    if teclas[pygame.K_ESCAPE]:
        pause()

def exibir_pontuacao(screen,pontuacao,paredes):
    # Exibindo a pontuação na tela
    pontuacao_text = pygame.font.Font(None,70).render(f"{pontuacao}", True, branco)
    x = LARGURA_TELA / 2 - (pontuacao_text.get_width() / 2)
    y = 50
    screen.blit(pontuacao_text,(x,y))

def game_over(screen,robo,paredes):

    robo.parado = True
    for parede in paredes:
        parede.parado = True

    # Definindo o quadrado do Game Over
    largura = LARGURA_TELA // 5
    altura = largura * 1.2
    x = (LARGURA_TELA // 2) - (largura // 2)
    y = (ALTURA_TELA // 2) - (altura // 2)

    quadrado = pygame.Rect(x,y,largura,altura)

    # Exibindo na tela o quadrado com borda
    borda = 5
    x = quadrado.x - borda
    y = quadrado.y - borda
    largura = quadrado.width + 2*borda
    altura = quadrado.height + 2*borda
    pygame.draw.rect(screen,branco,(x,y,largura,altura))
    pygame.draw.rect(screen,preto,quadrado)


    # Texto Game Over
    font = pygame.font.SysFont('Arial',64)
    text = font.render('Game Over',True,branco)
    text_rect = text.get_rect(center=(LARGURA_TELA//2,ALTURA_TELA//3))

    # Exibindo na tela o texto Game Over
    screen.blit(text,text_rect)


    # Definindo o botão
    largura = LARGURA_TELA // 7
    altura *= 0.2
    x = (LARGURA_TELA // 2) - (largura // 2)
    y = (ALTURA_TELA // 2) + altura

    botao = pygame.Rect(x,y,largura,altura)

    # Exibindo o botão na tela
    pygame.draw.rect(screen,cinza,botao)

    # Definindo o texto do botão
    font = pygame.font.SysFont('Arial', 32)
    text_surf = font.render('Restart', True, preto)
    text_rect = text_surf.get_rect(center=botao.center)
    screen.blit(text_surf, text_rect)



    # pygame.draw.rect(quadrado,cinza,)
    # text_surf = font.render(text, True, preto)
    # text_rect = text_surf.get_rect(center=rect.center)
    # screen.blit(text_surf, text_rect)

    # text_rect = text.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))

    # screen.blit(text,text_rect)

def waiting_press_key(robo,paredes):

    robo.desenhar(screen)
    for parede in paredes:
        parede.desenhar(screen)
    pygame.display.flip()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                return True

def pause():
    soltou = False
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            
        teclas = pygame.key.get_pressed()
        pressionou_esc = teclas[pygame.K_ESCAPE]

        if soltou and pressionou_esc:
            return True
        
        if not pressionou_esc:
            soltou = True
        

    return False
    
    
# Criando robô
x = (LARGURA_TELA // 2) - (IMAGEM_ROBO.get_width() // 2)
y = ALTURA_TELA / 2 - IMAGEM_ROBO.get_height()
robo = Robo(x,y)

# Criando as paredes
x = 0.9*LARGURA_TELA
aumento = LARGURA_TELA // 4
paredes = []
while x < 1.9*LARGURA_TELA:
    paredes.append(Parede(x))
    x += aumento

relogio = pygame.time.Clock()
fonte = pygame.font.Font(None,36)
timer = 0
pontuacao = 0

fps = 60
jogo_iniciou = False
rodando = True
contador = 0
colidiu = False

waiting_press_key(robo,paredes)

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            quit()
        

    # Verificar se colidiu
    # if verificar_colisao(robo,paredes) and not teclas[pygame.K_r]:

    colidiu = verificar_colisao(robo,paredes)

    if not colidiu:
        # Verificar as teclas pressionadas
        # Verificar se apertou para fechar o jogo a atualizar variável rodando
        verificar_teclas(robo)

        # Contador do tempo
        if jogo_iniciou:
            timer += 1 / fps

        # Atualizar pontuação
        for parede in paredes:
            if parede.pontuacao(robo):
                pontuacao += 1

        # Ajustar velocidade de acordo com a pontuação
        if pontuacao > 50:
            robo.acelerador = 1.0003
        elif pontuacao > 80:
            robo.acelerador = 1.0002

    # Desenhar todos os objetos e pontuação na tela
    desenhar_tela(screen,robo,paredes,timer)
    exibir_pontuacao(screen,pontuacao,paredes)
    
    # Se colidiu, então Game Over
    if colidiu:
        game_over(screen,robo,paredes)
    

    # Atualizar a tela
    pygame.display.flip()

    # Definindo o FPS
    relogio.tick(fps)

pygame.quit()