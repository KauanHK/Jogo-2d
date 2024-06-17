import pygame
import random
import os

import pygame.draw_py

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

# Título da janela
pygame.display.set_caption("Robozinho")

# Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
cinza = (200, 200, 200)

# Classe da nave
class Nave:

    def __init__(self,nave: int, x: int, y: int, largura: int | None = None,altura: int | None = None):
        self.nave = nave
        self.x = x
        self.y = y
        self.velocidade_y = 1
        self.cima = True
        self.acelerador = 1.00038

        if largura:
            self.largura = largura
        else:
            self.largura = LARGURA_TELA * 0.05

        self.max_width = self.largura * 1.1
        self.min_width = self.largura
        
        self.imagem = carregar_imagem(f'nave{nave}.png',(self.largura,'auto'))
        
        if isinstance(altura,int):
            self.altura = altura
        else:
            self.altura = self.imagem.get_height()

        self.max_height = self.altura * 1.1
        self.min_height = self.altura

        self.fogo = carregar_imagem(f'fogo{nave}.png',(LARGURA_TELA*0.05,'auto'))

        self.espaco_pressionado = False

        if self.nave == 1:
            self.selecionado = True
        else:
            self.selecionado = False

    
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
        
        if self.selecionado:
            self.largura = self.max_width
            self.altura = self.max_height
            img_rect = self.imagem.get_rect()
            margem = 10
            x = self.x - margem
            y = self.y - margem
            largura = self.largura + margem
            altura = self.altura + margem
            border_width = 2
            rect = pygame.Rect(x,y,largura,altura)
            pygame.draw.rect(screen,branco,rect,border_width)

        screen.blit(self.imagem,(self.x,self.y))
        if self.cima:
            self.soltar_fogo(screen)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
    
    def soltar_fogo(self,screen):
        screen.blit(self.fogo,(self.x,self.y+self.imagem.get_height()))
    
    def clicked(self,mouse_pos):
        rect = self.imagem.get_rect()
        rect.topleft = (self.x,self.y)
        if rect.collidepoint(mouse_pos):
            self.selecionado = True
            return True
        return False
    
    # def hover_size(self,increase):
    #     # Se o tamanho da imagem for menor do que o máximo
    #     if self.largura < self.max_width:
    #         # Aumentar se for para aumentar
    #         if increase:
    #             self.largura *= 1.05
    #             self.altura *= 1.05

    #         # Se não for para aumentar, e não estiver selecionado, redefinir as dimensões
    #         elif not self.selecionado:
    #             self.largura = self.min_width
    #             self.altura = self.min_height
            
    #         self.imagem = carregar_imagem(f'nave{self.nave}.png',(self.largura,self.altura))
        

    #     # Se as dimensões forem maiores do que as máximas, limitar para o tamanho máximo
    #     else:
    #         self.largura = self.max_height
    #         self.altura = self.max_height
    #         self.imagem = carregar_imagem(f'nave{self.nave}.png',(self.largura,self.altura))


    # def hover(self,mouse_pos):
    #     rect = self.imagem.get_rect()
    #     rect.topleft = (self.x,self.y)
    #     if rect.collidepoint(mouse_pos):
    #         self.hover_size(True)
    #     else:
    #         self.hover_size(False)

    
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
        
class Botao:
    def __init__(self,
                 txt: str,
                 font_size: int, 
                 coordinate: tuple[int,int],  
                 size: tuple[int,int], 
                 color_button: tuple, 
                 color_txt: tuple):

        self.txt = txt
        self.event = txt
        self.font_size = font_size
        self.coordinate = coordinate
        self.size = size
        self.color_button = color_button
        self.color_txt = color_txt

        self.atualizar_botao()

    def atualizar_botao(self):

        # Definindo o texto do botão
        font = pygame.font.Font(None,self.font_size)
        txt = font.render(self.txt,False,self.color_txt)

        # Definindo a superfície do botão
        self.surface = pygame.Surface(self.size)

        # Preenchendo o botão com a sua cor de fundo
        self.surface.fill(self.color_button)

        x = self.surface.get_rect().centerx - (txt.get_width() // 2)
        y = self.surface.get_rect().centery - (txt.get_height() // 2)
        self.surface.blit(txt,(x,y))

        self.botao_rect = self.surface.get_rect()
        self.botao_rect.topleft = self.coordinate


    def desenhar(self,screen):
        screen.blit(self.surface,self.coordinate)

    def collide_mouse(self,mouse_pos):
        if self.botao_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def click_event(self):
        return self.event

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
    

def criar_objetos(screen,nave_selecionada):
    # Criando a nave
    screen_rect = screen.get_rect()
    x = screen_rect.centerx
    y = screen_rect.centery
    nave = Nave(nave_selecionada,x,y)

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

def criar_botao(txt: str, font_size: int, size: tuple, color_button: tuple, color_txt: tuple):

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

def criar_botoes_inicio(screen,colors: list[tuple]):
    
    largura_tela = screen.get_width()
    altura_tela = screen.get_height()

    screen_rect = screen.get_rect()

    largura_botoes = largura_tela // 5
    altura_botoes = altura_tela // 10

    x = screen_rect.centerx - (largura_botoes // 2)
    y = screen_rect.centery - (altura_botoes // 2)
    margem_bottom = altura_botoes * 1.5

    coordinates = (x,y)
    size_botoes = (largura_botoes,altura_botoes)

    botao_iniciar = Botao('Start',48,coordinates,size_botoes,colors[0],preto)

    y += margem_bottom
    coordinates = (x,y)
    botao_naves = Botao('Naves',48,coordinates,size_botoes,colors[1],preto)

    y += margem_bottom
    coordinates = (x,y)
    botao_sair = Botao('Sair',48,coordinates,size_botoes,colors[2],preto)

    return [botao_iniciar,botao_naves,botao_sair]

def criar_titulo(txt: str, txt_size: int, color: tuple):

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
    
    nave_selecionada = 1
    while True:
        event = interface_inicial(screen,fundo)
        if event == 'Sair':
            pygame.quit()
            quit()
        elif event == 'Naves':
            nave_selecionada = interface_naves(screen,fundo,nave_selecionada)
        else:
            main_loop(screen,fundo,nave_selecionada)

    
def main_loop(screen,fundo,nave_selecionada):
    # Criar nave e obstáculos
    nave,paredes = criar_objetos(screen,nave_selecionada)

    # Clock para definir fps
    clock = pygame.time.Clock()
    fps = 60

    timer = 0
    pontuacao = 0

    colidiu = False
    espaco_pressionado = False

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
            game_over(screen,fundo,nave_selecionada)
        
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


def interface_inicial(screen,fundo):

    preto = (0,0,0)
    branco = (255,255,255)
    cinza = (200,200,200)

    cores = [255,255,255]

    titulo = criar_titulo('Jogo da Nave 2D',80,branco)

    largura_titulo = titulo.get_width()
    altura_titulo = titulo.get_height()
    x_titulo = (LARGURA_TELA - largura_titulo) // 2
    y_titulo = (ALTURA_TELA - altura_titulo) // 5

    cor_botao_iniciar = branco
    cor_botao_naves = branco
    cor_botao_sair = branco
    colors = (cor_botao_iniciar,cor_botao_naves,cor_botao_sair)
    botoes = criar_botoes_inicio(screen,colors)


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
                for botao in botoes:
                    if botao.collide_mouse(evento.pos):
                        return botao.click_event()
            else:
                for botao in botoes:
                    if botao.collide_mouse(pygame.mouse.get_pos()):
                        botao.color_button = cinza
                    else:
                        botao.color_button = branco
                    botao.atualizar_botao()




                            # botao.color_button = cinza
                            # botao.atualizar_botao()
            
            # else:
            #     mouse_pos = pygame.mouse.get_pos()
            #     for i,botao,dest in enumerate(botoes):
            #         if botao.get_rect().collidepoint(mouse_pos):
            #             botoes[i] = criar_botao()

            
        titulo = criar_titulo('Jogo da Nave 2D',80,tuple(cores))

        escala_aleatoria = random.choice([0,1,2])
        diminuicao = random.choice([i for i in range(5)])

        screen.blit(fundo,(0,0))
        screen.blit(titulo,(x_titulo,y_titulo))
        for botao in botoes:
            botao.desenhar(screen)

        cores[escala_aleatoria] -= diminuicao
        if cores[escala_aleatoria] < 0:
            cores[escala_aleatoria] = 255

        clock.tick(fps)

        pygame.display.flip()

def interface_naves(screen,fundo,nave_selecionada: int):

    preto = (0,0,0)
    branco = (255,255,255)

    # Definindo as dimensões das imagem das naves
    largura_nave = LARGURA_TELA * 0.075

    # Coordenadas do botão da primeira nave
    x_inicial_nave = LARGURA_TELA // 4 - largura_nave // 2
    y = (ALTURA_TELA // 8) * 3

    # Distância entre cada botão de nave
    aumento_x_nave = LARGURA_TELA // 8

    # Criando as naves
    x = x_inicial_nave
    naves = [Nave(i+1,x+ i*aumento_x_nave,y,largura_nave,'auto') for i in range(5)]
    for nave in naves:
        nave.cima = False
        nave.selecionado = False
    naves[nave_selecionada-1].selecionado = True

    # Definindo o rect de cada nave
    x = x_inicial_nave
    naves_rect = [nave.imagem.get_rect(center=(x * i*aumento_x_nave,y)) for i,nave in enumerate(naves)]

    # Criando a lista de auxílio para verificar se o mouse está em cima de alguma nave e identificar qual
    naves_hover = [False for i in range(5)]

    # Definindo a altura de cada nave
    altura_nave = naves[0].imagem.get_height()

    # Dimensões máximas de cada botão de nave
    max_width = largura_nave * 1.2
    max_height = altura_nave * 1.2

    # Criando o botão voltar
    largura = LARGURA_TELA // 6
    altura = ALTURA_TELA // 10
    x_voltar = (LARGURA_TELA-largura)//2
    y_voltar = (ALTURA_TELA//5) * 4

    botao_voltar = Botao('Voltar',48,(x_voltar,y_voltar),(largura,altura),branco,preto)

    titulo = criar_titulo('Selecione uma nave',80,branco)
    x_titulo = (LARGURA_TELA - titulo.get_width()) // 2
    y_titulo = ALTURA_TELA // 5

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
                if botao_voltar.collide_mouse(evento.pos):
                    return nave_selecionada
                
                # Verificar se selecionou alguma nave
                for i,nave in enumerate(naves):
                    if nave.clicked(evento.pos):
                        nave_selecionada = i + 1
                        for nave in naves:
                            nave.selecionado = False if nave.nave != nave_selecionada else True


        # # Verificar se o mouse está em cima de alguma nave e aumentar o tamanho da imagem
        # mouse_pos = pygame.mouse.get_pos()
        # for nave in naves:
        #     nave.hover(mouse_pos)
        

        screen.blit(fundo,(0,0))
        screen.blit(titulo,(x_titulo,y_titulo))

        for nave in naves:
            nave.desenhar(screen)
        botao_voltar.desenhar(screen)

        clock.tick(60)
        pygame.display.flip()

def game_over(screen,fundo,nave_selecionada):

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
                        main_loop(screen,fundo,nave_selecionada)
        

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