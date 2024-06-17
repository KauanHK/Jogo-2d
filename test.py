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

def criar_botao(txt,size,color_button,color_txt):

    # Definindo o texto do botão
    font = pygame.font.Font(None,48)
    botao_txt = font.render(txt,False,color_txt)

    # Definindo a superfície do botão
    botao_surf = pygame.Surface(size)

    # Preenchendo o botão com a sua cor de fundo
    botao_surf.fill(color_button)

    # Definindo as coordenadas
    x = (botao_surf.get_width() - botao_txt.get_width()) // 2
    y = (botao_surf.get_height() - botao_txt.get_height()) // 2

    botao_surf.blit(botao_txt,(x,y))

    return botao_surf

def exibir_interface_inicial(screen,fundo,cor_txt):

    # Definindo o fundo
    screen.blit(fundo,(0,0))

    font = pygame.font.Font(None,80)
    txt = font.render('Jogo 2D da Nave',False,cor_txt)
    x = (screen.get_width() - txt.get_width()) // 2
    y = (screen.get_height() - txt.get_height()) // 5
    screen.blit(txt,(x,y))


def criar_botoes_inicio(screen,cor):

    preto = (0,0,0)

    # Criando o botão Iniciar
    largura = LARGURA_TELA // 6
    altura = ALTURA_TELA // 10
    x_botao_iniciar = (screen.get_width() - largura) // 2
    y_botao_iniciar = ALTURA_TELA // 2
    botao_iniciar = pygame.Rect(x_botao_iniciar,y_botao_iniciar,largura,altura)
    pygame.draw.rect(screen,cor,botao_iniciar)

    # Texto do botão Iniciar
    font = pygame.font.Font(None,48)
    txt_start = font.render('Start',False,preto)

    # Coordenadas do texto no botão Iniciar
    x_txt = x_botao_iniciar + (largura - txt_start.get_width()) // 2
    y_txt = y_botao_iniciar + (altura - txt_start.get_height()) // 2

    # Inserindo o texto no botão
    screen.blit(txt_start,(x_txt,y_txt))

    # pygame.draw.rect(surf_buttons,(255,255,255),botao_iniciar)
    # surf_buttons.blit(botao_iniciar,(0,0))
    # screen.blit(surf_buttons,(x_surf_buttons,y_surf_buttons))

    return botao_iniciar

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

    inicio_jogo(screen,fundo)
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
        if colidiu and not teclas[pygame.K_r]:
            game_over(screen,fundo)
        
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

def inicio_jogo(screen,fundo):

    branco = (255,255,255)
    cinza = (200,200,200)

    cores = [255,255,255]

    exibir_interface_inicial(screen,fundo,(255,255,255))
    botao_iniciar = criar_botoes_inicio(screen,branco)

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
                    
        exibir_interface_inicial(screen,fundo,(cores[0],cores[1],cores[2]))
        botao_iniciar = criar_botoes_inicio(screen,cor_botao_iniciar)

        escala_aleatoria = random.choice([0,1,2])
        diminuicao = random.choice([i for i in range(5)])

        cores[escala_aleatoria] -= diminuicao
        if cores[escala_aleatoria] < 0:
            cores[escala_aleatoria] = 255

        clock.tick(fps)

        pygame.display.flip()
        
def interface_inicial():
    largura = LARGURA_TELA // 6
    altura = ALTURA_TELA // 10
    x = screen.get_rect().centerx - (largura // 2)
    y = ALTURA_TELA // 2
    botao_iniciar = criar_botao()
    botao_naves = criar_botao()
    botao_sair = criar_botao()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    return 'start'
                elif botao_naves.collidepoint(evento.pos):
                    return 'naves'
                elif botao_sair.collidepoint(evento.pos):
                    rodando = False
                    pygame.quit()
                    quit()

def interface_naves(screen,fundo):

    preto = (0,0,0)
    branco = (255,255,255)
    cinza = (200,200,200)

    # Definindo as dimensões das imagem das naves
    largura = LARGURA_TELA * 0.1

    # # Carregando as imagens de cada nave
    # botoes_naves = []
    # for i in range(5):
    #     botao_nave = carregar_imagem(f'nave{i+1}.png',largura,'auto')
    #     botoes_naves.append()
    

    largura_nave = LARGURA_TELA * 0.05
    naves_surf = [carregar_imagem('nave.png',(largura_nave,'auto')) for i in range(5)]
    altura_nave = naves_surf[0].get_height()

    x_inicial_nave = (LARGURA_TELA // 6) - (naves_surf[0].get_width() // 4)
    y_inicial_nave = (ALTURA_TELA // 8) * 3
    aumento_x_nave = x_inicial_nave
    naves_rect = [nave.get_rect() for nave in naves_surf]
    x = x_inicial_nave
    y = y_inicial_nave
    for nave in naves_rect:
        nave.topleft = (x,y)
        x += aumento_x_nave


    # Criando o botão voltar
    largura = LARGURA_TELA // 6
    altura = ALTURA_TELA // 10
    x_voltar = (LARGURA_TELA-largura)//2
    y_voltar = (ALTURA_TELA//5) * 4
    surf_voltar = criar_botao('Voltar',(largura,altura),branco,preto)
    botao_voltar = surf_voltar.get_rect()
    botao_voltar.topleft = (x_voltar,y_voltar)


    # botao_nave1 = carregar_imagem('nave1.png',largura,'auto')
    # botao_nave2 = carregar_imagem('nave2.png',largura,'auto')
    # botao_nave3 = carregar_imagem('nave3.png',largura,'auto')
    # botao_nave4 = carregar_imagem('nave4.png',largura,'auto')
    # botao_nave5 = carregar_imagem('nave5.png',largura,'auto')

    naves_hover = [False for i in range(5)]
    nave_selecionada = None

    max_width = largura_nave * 1.2
    max_height = altura_nave * 1.2

    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            # Evento de click
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(evento.pos):
                    return
                
                # Verificar se clicou em alguma nave e retornar em qual nave clicou
                for nave,botao_nave in enumerate(naves_rect):
                    if botao_nave.collidepoint(evento.pos):
                        nave_selecionada = nave + 1
            else:
                # Verificar se o mouse está em cima de alguma nave e aumentar o tamanho da imagem
                mouse_pos = pygame.mouse.get_pos()
                for i,botao_nave in enumerate(naves_rect):
                    if botao_nave.collidepoint(mouse_pos):
                        naves_hover[i] = True
                    else:
                        naves_hover[i] = False
        

        screen.blit(fundo,(0,0))



        x_nave = x_inicial_nave
        y_nave = y_inicial_nave
        for i,n_hover in enumerate(naves_hover):
            if n_hover:
                nave = naves_surf[i]
                largura *= 1.001
                altura *= 1.001
                if largura > max_width:
                    largura = max_width
                    altura = max_height
                nave = pygame.transform.scale(nave,(largura,altura))
                screen.blit(nave,(x_nave,y_nave))
            else:
                screen.blit(naves_surf[i],(x_nave,y_nave))
            
            x_nave += aumento_x_nave
                    
        

        # screen.blit(fundo,(0,0))

        # for botao_nave in botoes_naves:
        #     screen.blit(botao_nave,(x_inicial_nave,y_inicial_nave))
        #     x_inicial_nave += aumento_x_nave
        
        screen.blit(surf_voltar,(x_voltar,y_voltar))

        clock.tick(60)
        pygame.display.flip()

def game_over(screen,fundo):

    branco = (255,255,255)
    preto = (0,0,0)
    cinza_transparente = (200,200,200,128)

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
    font = pygame.font.SysFont('Arial',80)
    game_over_text_surf = font.render('Game Over',True,vermelho)
    game_over_text_surf.convert_alpha()
    game_over_rect = game_over_text_surf.get_rect(center=(quadrado.centerx,(quadrado.centery)-(quadrado.height//3)))

    # Definindo o fundo do txt Game Over
    surf_game_over = pygame.Surface(game_over_text_surf.get_size(),pygame.SRCALPHA)
    

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

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            go = False

        # pygame.draw.rect(screen,branco,quadrado_borda)
        # pygame.draw.rect(screen,preto,quadrado)
        surf_game_over.fill(cinza_transparente)
        surf_game_over.blit(game_over_text_surf,(0,0))
        pygame.draw.rect(screen,cor_botao,botao)
        screen.blit(restart_text_surf, restart_rect)
        screen.blit(game_over_text_surf,game_over_rect)

        # 60 FPS
        clock.tick(60)

        # Atualizando a tela
        pygame.display.flip()

        

interface_naves(screen,FUNDO)

pygame.quit()