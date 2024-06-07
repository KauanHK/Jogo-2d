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

# Definindo as imagens
IMAGEM_ROBO = pygame.image.load(os.path.join("imagens","nave.png"))
IMAGEM_ROBO = pygame.transform.scale_by(IMAGEM_ROBO,0.035)

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

    img = IMAGEM_ROBO
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.parado = True
        self.acelerador = 1.00038
    
    def moverCima(self):
        self.cima = True
    def moverBaixo(self):
        self.cima = False
    
    def atualizar_posicao(self):
        if not self.parado:
            if self.cima:
                self.velocidade_y = - abs(self.velocidade_y) * self.acelerador
            else: 
                self.velocidade_y = abs(self.velocidade_y) * self.acelerador
        
            self.y += self.velocidade_y

    
    def desenhar(self):
        screen.blit(self.img,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
# Classe da parede
class Parede:

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
        self.parado = True
        self.limite = 200
        self.espaco = 200
    
    def atualizar_posicao(self):
        if not self.parado:
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
                

    def desenhar(self):
        screen.blit(self.imagem,(self.x,self.y))
        screen.blit(self.imagem_rotacionada,(self.x,self.y-ALTURA_IMAGEM_PAREDE-self.espaco))

    def colidiu(self,robo_mask):
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
        



def desenhar_tela(robo,paredes,timer):
    # Background preto
    screen.fill(preto)
    # screen.blit(IMAGEM_FUNDO,(0,0))
    robo.atualizar_posicao()
    robo.desenhar()

    for parede in paredes:
        parede.atualizar_posicao()
        parede.desenhar()

    timer_text = fonte.render("{:.2f}".format(timer), True, branco)
    x = LARGURA_TELA / 2 - (timer_text.get_width() / 2)
    y = 100
    screen.blit(timer_text,(x,y))

def verificar_colisao(robo,paredes):
    robo_mask = robo.get_mask()
    for parede in paredes:
        if parede.colidiu(robo_mask):
            return True
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

# paredes.append(Parede(0,ALTURA_TELA - LARGURA_IMAGEM_PAREDE,True,True))
# paredes.append(Parede(0,0,True,True))

relogio = pygame.time.Clock()
fonte = pygame.font.Font(None,36)
timer = 0
pontuacao = 0

fps = 60
jogo_iniciou = False
rodando = True
contador = 0
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            quit()
    

    # Teclas pressionadas
    teclas = pygame.key.get_pressed()

    if verificar_colisao(robo,paredes) and not teclas[pygame.K_r]:
        game_over_text = pygame.font.Font(None,70).render("Game Over", True, branco)
        x = LARGURA_TELA / 2 - (game_over_text.get_width() / 2)
        y = ALTURA_TELA / 2 - (game_over_text.get_height() / 2)
        screen.blit(game_over_text,(x,y))
        contador += 1
        if contador > 60 and any(teclas) and not teclas[pygame.K_r]:
            rodando = False
            quit()

    else:
    

        if any(teclas):
            robo.parado = False
            for parede in paredes:
                parede.parado = False
            jogo_iniciou = True


        if jogo_iniciou:
            # Seta para cima
            if teclas[pygame.K_UP]:
                robo.moverCima()

            # Seta para baixo
            if teclas[pygame.K_DOWN]:
                robo.moverBaixo()
            
            # Botão roubar (R)
            if teclas[pygame.K_r]:
                contador = 0

            # Contador do tempo
            timer += 1 / fps


        desenhar_tela(robo,paredes,timer)

        for parede in paredes:
            if parede.pontuacao(robo):
                pontuacao += 1

        if pontuacao > 50:
            robo.acelerador = 1.0003
        elif pontuacao > 80:
            robo.acelerador = 1.0002
        
        pontuacao_text = pygame.font.Font(None,70).render(f"{pontuacao}", True, branco)
        x = LARGURA_TELA / 2 - (pontuacao_text.get_width() / 2)
        y = 50
        screen.blit(pontuacao_text,(x,y))
    


    # Atualizar a tela
    pygame.display.flip()

    # 60 FPS
    relogio.tick(fps)


pygame.quit()