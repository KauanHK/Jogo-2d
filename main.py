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

def carregar_imagem(file_name,size: tuple | None=None):
    
    # Carregando a imagem original
    imagem = pygame.image.load(os.path.join('imagens',file_name))

    # Se for fornecido um tamanho para a imagem
    if size:

        # Definindo as dimensões desejadas
        largura = size[0]
        altura = size[1]

        # Verificar se alguma dimensão deve ser calculada
        if largura == 'auto':
            
            # Calcular medida da largura
            # Definindo as dimensões originais da imagem
            largura_original = imagem.get_width()
            altura_original = imagem.get_height()

            # Razão entre a largura e altura originais da imagem
            relacao = largura_original / altura_original

            # Definindo a medida da largura da imagem
            largura = altura * relacao

            # Carregando a imagem de acordo com as dimensões calculadas
            imagem = pygame.transform.scale(imagem,(largura,altura))

        elif altura == 'auto':
            # Calcular medida da altura
            # Definindo as dimensões originais da imagem
            largura_original = imagem.get_width()
            altura_original = imagem.get_height()

            # Razão entre a largura e altura originais
            relacao = largura_original / altura_original
            altura = largura * relacao

            # Carregando a imagem de acordo com as dimensões calculadas
            imagem = pygame.transform.scale(imagem,(largura,altura))
        
        else:
            # Caso todas as dimensões sejam informadas, carregar imagem com elas
            imagem = pygame.transform.scale(imagem,size)
        
    return imagem

IMAGEM_ROBO = carregar_imagem('nave.png',(0.05*LARGURA_TELA,'auto'))
IMAGEM_PAREDE = carregar_imagem('obstaculo.jpg',('auto',0.4*ALTURA_TELA))
IMAGEM_PAREDE_ROTACIONADA = pygame.transform.rotate(IMAGEM_PAREDE,180)
FUNDO = carregar_imagem('fund.jpg',(LARGURA_TELA,ALTURA_TELA))

# Título da janela
pygame.display.set_caption("Robozinho")

# Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
cinza = (200, 200, 200)

# Classe do robô
class Robo:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.acelerador = 1.00038
        self.imagem = IMAGEM_ROBO
    
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
        screen.blit(self.imagem,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
    
# Classe da parede
class Parede:

    def __init__(self,x,id):
        self.x = x
        self.y = 200

        self.imagem = IMAGEM_PAREDE
        self.largura_imagem = self.imagem.get_width()
        self.altura_imagem = self.imagem.get_height()

        self.imagem_rotacionada = IMAGEM_PAREDE_ROTACIONADA
        self.velocidade_x = LARGURA_TELA // 400
        self.passou = False
        self.limite = ALTURA_TELA // 5
        self.y = random.choice([i for i in range((ALTURA_TELA//2) - int(self.limite//2),(ALTURA_TELA//2) + int(self.limite//2))])
        self.espaco = ALTURA_TELA * 0.25

        self.id = id

        # Calcular número de imagens que devem ser postas uma sobre a outra
        altura_total = 0
        img_count = 1
        while altura_total < ALTURA_TELA:
            img_count += 1
            altura_total += self.altura_imagem
        
        self.img_count = img_count
        self.altura_total = altura_total

    def novo_obstaculo(self,y_parede_anterior):
        self.passou = False
        self.limite += 2
        self.x = LARGURA_TELA

        y = random.choice([i for i in range(ALTURA_TELA)])
        if y > y_parede_anterior + self.limite:
            y = y_parede_anterior + self.limite
        elif y < y_parede_anterior - self.limite:
            y = y_parede_anterior - self.limite

        if y > ALTURA_TELA - self.espaco - 20:
            y = ALTURA_TELA - self.espaco - 20
        elif y < self.espaco + 20:
            y = self.espaco + 20

        self.y = y

        self.espaco += 1

    def atualizar_posicao(self,paredes):
        self.x -= self.velocidade_x
        self.velocidade_x *= 1.0002
        
        if self.x < - self.largura_imagem:
            parede_anterior = paredes[self.id-1]
            y = parede_anterior.y
            self.novo_obstaculo(y)

    def desenhar(self,screen):
        self.parede = pygame.Surface((self.largura_imagem,ALTURA_TELA))
        altura = 0
        for img in range(self.img_count):
            self.parede.blit(self.imagem,(0,altura))
            altura += self.altura_imagem

        self.parede_rotacionada = pygame.Surface((self.largura_imagem,self.altura_imagem*2))
        altura = 0
        for img in range(self.img_count):
            self.parede_rotacionada.blit(self.imagem_rotacionada,(0,altura))
            altura += self.altura_imagem

        screen.blit(self.parede,(self.x,self.y))
        screen.blit(self.parede_rotacionada,(self.x,self.y-self.espaco-(2*self.altura_imagem)))



    def colidiu(self,robo):
        min = (LARGURA_TELA // 2) - self.largura_imagem - (self.largura_imagem // 2)
        max = (LARGURA_TELA // 2) + self.largura_imagem // 2
        if self.x > min and self.x < max:
            robo_mask = robo.get_mask()

            cano_base_mask = pygame.mask.from_surface(self.parede)
            cano_topo_mask = pygame.mask.from_surface(self.parede_rotacionada)

            distancia_base = (round(self.x - robo.x),round(self.y - robo.y))
            distancia_topo = (round(self.x - robo.x),round(self.y-(2*self.altura_imagem)-self.espaco - robo.y))

            if robo_mask.overlap(cano_base_mask,distancia_base) or robo_mask.overlap(cano_topo_mask,distancia_topo):
                return True
            return False

    def pontuacao(self,robo):
        if not self.passou and robo.x >= self.x and robo.x <= self.x + self.largura_imagem:
            self.passou = True
            return True
        return False
        

def atualizar_posicao(robo,paredes):
    robo.atualizar_posicao()
    for parede in paredes:
        parede.atualizar_posicao(paredes)

def desenhar_tela(screen,fundo,robo,paredes):
    # Background preto
    screen.fill(preto)

    screen.blit(fundo,(0,0))
    
    robo.desenhar(screen)
    for parede in paredes:
        parede.desenhar(screen)
    
def verificar_colisao(robo,paredes):
    for parede in paredes:
        if parede.colidiu(robo):
            return True
    return False

def exibir_pontuacao(screen,pontuacao,timer):

    # Exibindo a pontuação na tela
    branco = (255,255,255)
    fonte = pygame.font.Font(None,64)
    pontuacao_text = fonte.render(str(pontuacao), True, branco)
    x = LARGURA_TELA / 2 - (pontuacao_text.get_width() / 2)
    y = 50
    screen.blit(pontuacao_text,(x,y))

    # Exibindo o timer na tela
    fonte = pygame.font.Font(None,32)
    timer_text = fonte.render("{:.2f}".format(timer), True, branco)
    x = LARGURA_TELA / 2 - (timer_text.get_width() / 2)
    y = 100
    screen.blit(timer_text,(x,y))


def waiting_press_key(screen,robo,paredes):

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                return True

def pause(screen,fundo,robo,paredes,pontuacao,timer):
    clock = pygame.time.Clock()
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = False

        desenhar_tela(screen,fundo,robo,paredes)
        exibir_pontuacao(screen,pontuacao,timer)

        font = pygame.font.SysFont('Arial',64)
        text = font.render('Jogo Pausado',True,branco)
        screen.blit(text, (250, 250))
        text = font.render('Pressione ESC para continuar',True,branco)
        screen.blit(text, (250,350))
        pygame.display.flip()
        clock.tick(10)
            
    return False
    

def criar_objetos():
    # Criando robô
    x = (LARGURA_TELA // 2) - (IMAGEM_ROBO.get_width() // 2)
    y = ALTURA_TELA / 2 - IMAGEM_ROBO.get_height()
    robo = Robo(x,y)

    # Criando as paredes
    x = 0.9*LARGURA_TELA
    aumento = LARGURA_TELA / 4
    paredes = []
    id = 0
    while x < 1.9*LARGURA_TELA:
        paredes.append(Parede(x,id))
        x += aumento
        id += 1
    
    return robo,paredes

def main(screen,fundo):
    # Criar robo e obstáculos
    robo,paredes = criar_objetos()

    # Clock para definir fps
    clock = pygame.time.Clock()
    fps = 60

    # Timer e pontuação
    timer = 0
    pontuacao = 0

    colidiu = False

    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            
        # Verificar teclas
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_UP]:
            robo.moverCima()
        elif teclas[pygame.K_DOWN]:
            robo.moverBaixo()
        if teclas[pygame.K_ESCAPE]:
            pause(screen,fundo,robo,paredes,pontuacao,timer)

        # Verificar colisões
        colidiu = verificar_colisao(robo,paredes)
        if colidiu:
            game_over(screen,fundo,robo,paredes)
        
        # Contador do tempo
        timer += 1 / fps

        # Atualizar pontuação
        for parede in paredes:
            if parede.pontuacao(robo):
                pontuacao += 1

        # # Ajustar velocidade de acordo com a pontuação
        # if pontuacao > 50:
        #     robo.acelerador = 1.0003
        # elif pontuacao > 80:
        #         robo.acelerador = 1.0002

        # Desenhar todos os objetos e pontuação na tela
        atualizar_posicao(robo,paredes)
        desenhar_tela(screen,fundo,robo,paredes)
        exibir_pontuacao(screen,pontuacao,timer)
        
        # Atualizar a tela
        pygame.display.flip()

        # Definindo o FPS
        clock.tick(fps)

def game_over(screen,fundo,robo,paredes):

    branco = (255,255,255)
    preto = (0,0,0)

    # Definindo o quadrado do Game Over
    largura_quad_go = LARGURA_TELA // 5
    altura_quad_go = largura_quad_go * 1.2
    x = (LARGURA_TELA // 2) - (largura_quad_go // 2)
    y = (ALTURA_TELA // 2) - (altura_quad_go // 2)

    quadrado = pygame.Rect(x,y,largura_quad_go,altura_quad_go)

    # Exibindo na tela o quadrado com borda
    borda = 5
    x = quadrado.x - borda
    y = quadrado.y - borda
    largura_borda = quadrado.width + 2*borda
    altura_borda = quadrado.height + 2*borda

    quadrado_borda = pygame.Rect(x,y,largura_borda,altura_borda)

    # Definindo o texto 'Game Over'
    font = pygame.font.SysFont('Arial',48)
    game_over_text_surf = font.render('Game Over',True,branco)
    game_over_rect = game_over_text_surf.get_rect(center=(quadrado.centerx,(quadrado.centery)-(quadrado.height//3)))

    # Definindo o botão
    largura = LARGURA_TELA // 7
    altura = altura_borda * 0.2
    x = (LARGURA_TELA // 2) - (largura // 2)
    y = (ALTURA_TELA // 2) + altura

    botao = pygame.Rect(x,y,largura,altura)

    # Definindo o texto do botão
    font = pygame.font.SysFont('Arial', 32)
    restart_text_surf = font.render('Restart', True, preto)
    restart_rect = restart_text_surf.get_rect(center=botao.center)

    cor_botao = cinza
    go = True
    clock = pygame.time.Clock()
    while go:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                go = False
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    go = False
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if botao.collidepoint(evento.pos):
                        main(screen,fundo)

        pygame.draw.rect(screen,branco,quadrado_borda)
        pygame.draw.rect(screen,preto,quadrado)
        pygame.draw.rect(screen,cor_botao,botao)
        screen.blit(restart_text_surf, restart_rect)
        screen.blit(game_over_text_surf,game_over_rect)


        clock.tick(60)
        # Atualizando a tela
        pygame.display.flip()


        
main(screen,FUNDO)

pygame.quit()