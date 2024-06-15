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
            altura = largura / relacao

            # Carregando a imagem de acordo com as dimensões calculadas
            imagem = pygame.transform.scale(imagem,(largura,altura))
        
        else:
            # Caso todas as dimensões sejam informadas, carregar imagem com elas
            imagem = pygame.transform.scale(imagem,size)
        
    return imagem

IMAGEM_PAREDE = carregar_imagem('obstaculo.jpg',('auto',0.4*ALTURA_TELA))
IMAGEM_PAREDE_ROTACIONADA = pygame.transform.rotate(IMAGEM_PAREDE,180)
FUNDO = carregar_imagem('fund.jpg',(LARGURA_TELA,ALTURA_TELA))


IMAGEM_NAVE1 = carregar_imagem('nave1.png',(0.05*LARGURA_TELA,'auto'))
IMAGEM_NAVE2 = carregar_imagem('nave2.png',(0.05*LARGURA_TELA,'auto'))
FOGO_NAVE1 = carregar_imagem('fogo1.png',(0.05*LARGURA_TELA,'auto'))
FOGO_NAVE2 = carregar_imagem('fogo2.png',(0.05*LARGURA_TELA,'auto'))


# Título da janela
pygame.display.set_caption("Robozinho")

# Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
cinza = (200, 200, 200)

# Classe do robô
class Nave:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.acelerador = 1.00038
        self.imagem = IMAGEM_NAVE2
        self.fogo = FOGO_NAVE2
        self.espaco_pressionado = False
    
    def mover(self,direction):
        if direction == 1:
            self.cima = False
        elif direction == 2:
            self.cima = False if self.cima else True
        else:
            self.cima = True
    
    def atualizar_posicao(self):
        if self.cima:
            self.velocidade_y = - abs(self.velocidade_y) * self.acelerador
        else: 
            self.velocidade_y = abs(self.velocidade_y) * self.acelerador
    
        self.y += self.velocidade_y

    
    def desenhar(self,screen):
        screen.blit(self.imagem,(self.x,self.y))
        if self.cima:
            screen.blit(self.fogo,(self.x,self.y+self.imagem.get_height()))
    
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



    def colidiu(self,nave):
        min = (LARGURA_TELA // 2) - self.largura_imagem - (self.largura_imagem // 2)
        max = (LARGURA_TELA // 2) + self.largura_imagem // 2
        if self.x > min and self.x < max:
            robo_mask = nave.get_mask()

            cano_base_mask = pygame.mask.from_surface(self.parede)
            cano_topo_mask = pygame.mask.from_surface(self.parede_rotacionada)

            distancia_base = (round(self.x - nave.x),round(self.y - nave.y))
            distancia_topo = (round(self.x - nave.x),round(self.y-(2*self.altura_imagem)-self.espaco - nave.y))

            if robo_mask.overlap(cano_base_mask,distancia_base) or robo_mask.overlap(cano_topo_mask,distancia_topo):
                return True
            return False

    def pontuacao(self,nave):
        if not self.passou and nave.x >= self.x and nave.x <= self.x + self.largura_imagem:
            self.passou = True
            return True
        return False
        

def atualizar_posicao(nave,paredes):
    nave.atualizar_posicao()
    for parede in paredes:
        parede.atualizar_posicao(paredes)

def desenhar_tela(screen,fundo,nave,paredes):
    # Background preto
    screen.fill(preto)

    screen.blit(fundo,(0,0))
    
    nave.desenhar(screen)
    for parede in paredes:
        parede.desenhar(screen)
    
def verificar_colisao(nave,paredes):
    for parede in paredes:
        if parede.colidiu(nave):
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


def waiting_press_key(screen,nave,paredes):

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                return True

def pause(screen,fundo,nave,paredes,pontuacao,timer):
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

        desenhar_tela(screen,fundo,nave,paredes)
        exibir_pontuacao(screen,pontuacao,timer)

        font = pygame.font.SysFont('Arial',64)
        text = font.render('Jogo Pausado',True,branco)
        screen.blit(text, (250, 250))
        text = font.render('Pressione ESC para continuar',True,branco)
        screen.blit(text, (250,350))
        pygame.display.flip()
        clock.tick(10)
            
    return False
    

def criar_objetos(screen):
    # Criando a nave
    screen_rect = screen.get_rect()
    x = screen_rect.centerx
    y = screen_rect.centery
    nave = Nave(x,y)

    # Criando as paredes
    x = 0.9*LARGURA_TELA
    aumento = LARGURA_TELA / 4
    paredes = []
    id = 0
    while x < 1.9*LARGURA_TELA:
        paredes.append(Parede(x,id))
        x += aumento
        id += 1
    
    return nave,paredes

def criar_botao(txt: str,dest: tuple,font_size,txt_color):

    # Definindo o texto do botão
    font = pygame.font.Font(None,font_size)
    txt = font.render(txt,False,txt_color)

    # Criando o rect do botão
    botao = pygame.Surface(dest)
    botao_rect = botao.get_rect()
    botao.blit(txt,botao_rect.center)


    return botao_rect


def criar_titulo(txt: str, dest: tuple, txt_size: int, color: tuple):

    font = pygame.font.Font(None,txt_size)
    txt = font.render(txt,False,color)
    return txt

def funcao():
    pass
    # # Criando o botão Iniciar
    # largura = LARGURA_TELA // 6
    # altura = ALTURA_TELA // 10
    # x_botao_iniciar = (screen.get_width() - largura) // 2
    # y_botao_iniciar = ALTURA_TELA // 2
    # botao_iniciar = pygame.Rect(x_botao_iniciar,y_botao_iniciar,largura,altura)
    # pygame.draw.rect(screen,cor,botao_iniciar)

    # # Texto do botão Iniciar
    # font = pygame.font.Font(None,48)
    # txt_start = font.render('Start',False,preto)

    # # Coordenadas do texto no botão Iniciar
    # x_txt = x_botao_iniciar + (largura - txt_start.get_width()) // 2
    # y_txt = y_botao_iniciar + (altura - txt_start.get_height()) // 2

    # # Inserindo o texto no botão
    # screen.blit(txt_start,(x_txt,y_txt))

    # # pygame.draw.rect(surf_buttons,(255,255,255),botao_iniciar)
    # # surf_buttons.blit(botao_iniciar,(0,0))
    # # screen.blit(surf_buttons,(x_surf_buttons,y_surf_buttons))

def main(screen,fundo):
    # Criar nave e obstáculos
    nave,paredes = criar_objetos(screen)

    # Clock para definir fps
    clock = pygame.time.Clock()
    fps = 60

    timer = 0
    pontuacao = 0

    colidiu = False
    espaco_pressionado = False

    inicio_jogo(screen,fundo)
    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not espaco_pressionado:
                    nave.mover(2)
                    espaco_pressionado = True
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    espaco_pressionado = False
                


            
        # Verificar teclas
        teclas = pygame.key.get_pressed()
        
    
        if teclas[pygame.K_UP]:
            nave.mover(0)
        elif teclas[pygame.K_DOWN]:
            nave.mover(1)
        # if teclas[pygame.K_SPACE]:
        #     nave.mover(2)
        if teclas[pygame.K_ESCAPE]:
            pause(screen,fundo,nave,paredes,pontuacao,timer)

        # Verificar colisões
        colidiu = verificar_colisao(nave,paredes)
        if colidiu and not teclas[pygame.K_r]:
            game_over(screen,fundo)
        
        # Contador do tempo
        timer += 1 / fps

        # Atualizar pontuação
        for parede in paredes:
            if parede.pontuacao(nave):
                pontuacao += 1

        # Desenhar todos os objetos e pontuação na tela
        atualizar_posicao(nave,paredes)
        desenhar_tela(screen,fundo,nave,paredes)
        exibir_pontuacao(screen,pontuacao,timer)
        
        # Atualizar a tela
        pygame.display.flip()

        # Definindo o FPS
        clock.tick(fps)

def inicio_jogo(screen,fundo):

    branco = (255,255,255)
    cinza = (200,200,200)

    cores = [255,255,255]

    x_titulo = (screen.get_width() - txt.get_width()) // 2
    y_titulo = (screen.get_height() - txt.get_height()) // 5

    botao_iniciar = criar_botao('Start',screen.get_rect().center,80,branco)

    clock = pygame.time.Clock()
    fps = 60

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if botao_iniciar.collidepoint(evento.pos):
                        return
            
        mouse_position = pygame.mouse.get_pos()

        if botao_iniciar.collidepoint(mouse_position):
            cor_botao_iniciar = cinza
        else:
            cor_botao_iniciar = branco
                    
        titulo = criar_titulo((cores[0],cores[1],cores[2]))
        botao_iniciar = criar_botao('Start',screen.get_rect().center,80,branco)

        escala_aleatoria = random.choice([0,1,2])
        diminuicao = random.choice([i for i in range(5)])

        screen.fill(fundo)
        screen.blit(titulo,(x_titulo,y_titulo))
        screen.blit(botao_iniciar,)

        cores[escala_aleatoria] -= diminuicao
        if cores[escala_aleatoria] < 0:
            cores[escala_aleatoria] = 255

        clock.tick(fps)

        pygame.display.flip()
        


def game_over(screen,fundo):

    branco = (255,255,255)
    preto = (0,0,0)
    cinza = (200,200,200)

    # Definindo o texto Game Over
    font = pygame.font.SysFont('Arial',80)
    txt_game_over = font.render('Game Over',True,vermelho)

    # Definindo as coordenadas do texto Game Over
    x_go = (screen.get_width() - txt_game_over.get_width()) // 2
    y_go = (screen.get_height() - txt_game_over.get_height()) // 3

    # Definindo o texto do botão Restart
    font = pygame.font.Font(None,48)
    txt_restart = font.render('Restart',False,preto)

    # Definindo as dimensões do botão
    largura_botao = LARGURA_TELA // 6
    altura_botao = ALTURA_TELA // 10
    x_botao = (LARGURA_TELA - largura_botao) // 2
    y_botao = (ALTURA_TELA - altura_botao) // 2

    # Criando o botão
    botao = pygame.Surface((largura_botao,altura_botao))

    # Definindo o rect do botão
    botao_rect = botao.get_rect()
    botao_rect.topleft = (x_botao,y_botao)

    # Definindo as coordenadas do texto Restart
    x_restart = (botao.get_width() - txt_restart.get_width()) // 2
    y_restart = (botao.get_height() - txt_restart.get_height()) // 2

    # Definindo o fundo do botão como cinza
    botao.fill(branco)

    # Inserindo o texto Restart no botão
    botao.blit(txt_restart,(x_restart,y_restart))

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
                    if botao_rect.collidepoint(evento.pos):
                        main(screen,fundo)
        

        mouse = pygame.mouse.get_pos()
        if botao_rect.collidepoint(mouse):
            botao.fill(cinza)
        else:
            botao.fill(branco)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            go = False

        screen.blit(txt_game_over,(x_go,y_go))
        botao.blit(txt_restart,(x_restart,y_restart))
        screen.blit(botao,(x_botao,y_botao))

        # 60 FPS
        clock.tick(60)

        # Atualizando a tela
        pygame.display.flip()

        
main(screen,FUNDO)

pygame.quit()