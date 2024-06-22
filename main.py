import pygame
import random
import os

import pygame.draw_py

# Inicializar o Pygame
pygame.init()

# Criar uma janela de exibição como fullscreen
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
pygame.display.set_caption("Jogo da Nave 2D")

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
        
        original_nave = carregar_imagem(f'nave{nave}.png').get_width()
        self.imagem = carregar_imagem(f'nave{nave}.png',(self.largura,'auto'))

        original_width = carregar_imagem(f'fogo{nave}.png').get_width()
        largura_fogo = original_width * self.largura // original_nave
        self.fogo = carregar_imagem(f'fogo{nave}.png',(largura_fogo,'auto'))
        
        if isinstance(altura,int):
            self.altura = altura
        else:
            self.altura = self.imagem.get_height()

        self.max_height = self.altura * 1.1
        self.min_height = self.altura


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
    
    def desenhar(self, screen, menu: bool | None = False):

        cinza = (200,200,200,50)
        
        if menu and self.selecionado:
            # Definindo as coordenadas da borda
            padding = 30
            x = self.x - padding
            y = self.y - padding

            # Definindo as dimensões da borda
            largura = self.largura + 2*padding
            altura = self.altura + 2*padding

            # Criando a borda e exibindo-a na tela
            surface = pygame.Surface((largura,altura),pygame.SRCALPHA)
            rect = pygame.Rect(0,0,largura,altura)
            rect.center = (surface.get_width() // 2, surface.get_height() // 2)

            pygame.draw.rect(surface,cinza,rect)
            screen.blit(surface,(x,y))

            
            # self.imagem = pygame.transform.scale(self.imagem,(self.largura,self.altura))

        screen.blit(self.imagem,(self.x,self.y))

        if self.cima:
            self.soltar_fogo(screen)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
    
    def soltar_fogo(self,screen):
        y_fogo = [self.y + self.altura, self.y + (3/4) * self.altura, self.y + self.altura, self.y + self.altura/10*9,self.y + self.altura]
        
        x = self.imagem.get_rect(topleft=(self.x,self.y)).centerx - (self.fogo.get_width() // 2)
        y = y_fogo[self.nave - 1]
        screen.blit(self.fogo,(x,y))
    
    def clicked(self,mouse_pos):
        rect = self.imagem.get_rect(topleft = (self.x,self.y))
        if rect.collidepoint(mouse_pos):
            self.selecionado = True
            return True
        return False

    def hover(self,mouse_pos):
        rect = self.imagem.get_rect(topleft=(self.x,self.y))
        if rect.collidepoint(mouse_pos):
            self.largura *= 1.03
            self.altura *= 1.03
        else:
            self.largura = self.min_width
            self.altura = self.min_height
        
        if self.largura > self.max_width:
            self.largura = self.max_width
            self.altura = self.max_height
            

        # Redefinindo o tamanho da imagem
        self.imagem = carregar_imagem(f'nave{self.nave}.png',(self.largura,'auto'))

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
        # min = (LARGURA_TELA // 2) - self.largura_imagem - (self.largura_imagem // 2)
        # max = (LARGURA_TELA // 2) + self.largura_imagem // 2
        # if self.x > min and self.x < max:
        if self.x <= nave.x + nave.largura and self.x + self.largura_imagem >= nave.x:
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
                 coordinate: tuple[int,int],  
                 size: tuple[int,int], 
                 color_button: tuple, 
                 color_txt: tuple):

        self.txt = txt
        self.event = txt
        self.coordinate = coordinate
        self.size = size
        self.color_button = color_button
        self.color_txt = color_txt

        self.atualizar_botao()

    def atualizar_botao(self):

        # Definindo o tamanho da letra
        font_size = round(self.size[1] / 1.5)

        # Definindo o texto do botão
        font = pygame.font.Font(None,font_size)
        txt = font.render(self.txt,False,self.color_txt)

        # Definindo a superfície do botão
        self.surface = pygame.Surface(self.size)

        # Preenchendo o botão com a sua cor de fundo
        self.surface.fill(self.color_button)

        x = self.surface.get_rect().centerx - (txt.get_width() // 2)
        y = self.surface.get_rect().centery - (txt.get_height() // 2)
        self.surface.blit(txt,(x,y))


    def desenhar(self,screen):
        screen.blit(self.surface,self.coordinate)
    
    def get_centered_rect(self):
        return self.surface.get_rect(topleft=self.coordinate)

    def collide_mouse(self,mouse_pos):
        botao_rect = self.surface.get_rect(topleft=self.coordinate)
        if botao_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def get_event(self):
        return self.event
    
class Titulo:

    def __init__(self, txt: str, font_size: int, coordinate: tuple[int,int], color: tuple[int,int,int] | None = (255,255,255)):
        self.txt = txt
        self.font_size = font_size
        self.coordinate = coordinate
        self.color = color

        self.atualizar_titulo()
    
    def atualizar_titulo(self):
        font = pygame.font.Font(None,self.font_size)
        txt = font.render(self.txt,False,self.color)
        self.titulo = txt

        x = self.coordinate[0]
        y = self.coordinate[1]
        if x == 'center':
            x = (screen.get_width() - txt.get_width()) // 2
        
        self.coordinate = (x,y)


    
    def exibir_titulo(self,screen):
        screen.blit(self.titulo, self.coordinate)

def atualizar_posicao(nave,paredes):
    nave.atualizar_posicao()
    for parede in paredes:
        parede.atualizar_posicao(paredes)

def desenhar_tela(screen,fundo,nave,paredes):
    
    screen.blit(fundo,(0,0))
    
    nave.desenhar(screen,False)
    for parede in paredes:
        parede.desenhar(screen)

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

def verificar_colisao(nave,paredes):
    for parede in paredes:
        if parede.colidiu(nave):
            return True
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

def criar_botoes_inicio(screen,colors: list[tuple]):

    preto = (0,0,0)
    
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

    botao_iniciar = Botao('Jogar',coordinates,size_botoes,colors[0],preto)

    y += margem_bottom
    coordinates = (x,y)
    botao_naves = Botao('Naves',coordinates,size_botoes,colors[1],preto)

    y += margem_bottom
    coordinates = (x,y)
    botao_sair = Botao('Sair',coordinates,size_botoes,colors[2],preto)

    return [botao_iniciar,botao_naves,botao_sair]

def interface_inicial(screen,fundo):

    branco = (255,255,255)
    cinza = (200,200,200)

    cores = [255,255,255]

    titulo_font_size = screen.get_height() // 8
    y = screen.get_height() // 5
    titulo = Titulo('Jogo da Nave 2D',titulo_font_size, ('center',y), tuple(cores))

    colors = (branco,branco,branco)
    botoes = criar_botoes_inicio(screen,colors)

    naves = None    

    velocidade = ALTURA_TELA // 300

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
                        return botao.get_event()
        
        
        
        mouse_pos = pygame.mouse.get_pos()
        for botao in botoes:
            if botao.collide_mouse(mouse_pos):
                botao.color_button = cinza
            else:
                botao.color_button = branco
            botao.atualizar_botao()

        escala_aleatoria = random.choice([0,1,2])
        diminuicao = random.choice([i for i in range(5)])
        cores[escala_aleatoria] -= diminuicao
        if cores[escala_aleatoria] < 0:
            cores[escala_aleatoria] = 255
        titulo.color = tuple(cores)
        titulo.atualizar_titulo()

        screen.blit(fundo,(0,0))
        titulo.exibir_titulo(screen)
        for botao in botoes:
            botao.desenhar(screen)

        naves = nave_voando(velocidade,naves)

        clock.tick(fps)

        pygame.display.flip()

def criar_naves_voando():

    nave_aleat = random.choice([i+1 for i in range(5)])

    largura = LARGURA_TELA // 20
    x = LARGURA_TELA // 10 - largura // 2
    y = ALTURA_TELA
    nave1 = Nave(nave_aleat,x,y,largura)

    nave_aleat = random.choice([i+1 for i in range(5)])
    x = LARGURA_TELA * 0.9 - largura // 2
    nave2 = Nave(nave_aleat,x,y,largura)

    naves = [nave1, nave2]
    return naves

def nave_voando(velocidade, naves: list[Nave,Nave] | None = None):

    if not naves:
        naves = criar_naves_voando()

    naves_recriar = False
    for i,nave in enumerate(naves):
        nave.desenhar(screen)
        nave.y -= velocidade

        if nave.y < -100:
            naves_recriar = True

    if naves_recriar:
        naves = criar_naves_voando()
    return naves
    
def interface_naves(screen,fundo,nave_selecionada: int):

    preto = (0,0,0)
    branco = (255,255,255)
    cinza = (200,200,200)

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

    botao_voltar = Botao('Voltar',(x_voltar,y_voltar),(largura,altura),branco,preto)

    altura_tela = screen.get_height()
    font_size = altura_tela // 10
    y_titulo = altura_tela // 8

    titulo = Titulo('Selecione uma nave',font_size,('center',y_titulo),branco)

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
            
        


        # Verificar se o mouse está em cima de alguma nave e aumentar o tamanho da imagem
        mouse_pos = pygame.mouse.get_pos()
        for nave in naves:
            nave.hover(mouse_pos)
        
        if botao_voltar.collide_mouse(mouse_pos):
            botao_voltar.color_button = cinza
        else:
            botao_voltar.color_button = branco
        botao_voltar.atualizar_botao()
        

        screen.blit(fundo,(0,0))
        titulo.exibir_titulo(screen)

        for nave in naves:
            nave.desenhar(screen, True)
        botao_voltar.desenhar(screen)

        clock.tick(60)
        pygame.display.flip()

def game_over(screen,fundo,nave_selecionada,nave,paredes):

    branco = (255,255,255)
    preto = (0,0,0)
    cinza = (200,200,200)
    vermelho = (255,0,0)

    # Definindo o texto Game Over
    font_size = ALTURA_TELA // 6
    y = ALTURA_TELA // 4
    txt_game_over = Titulo('Game Over', font_size, ('center',y),vermelho)

    # Definindo as dimensões dos botões
    largura_botao = LARGURA_TELA // 6
    altura_botao = ALTURA_TELA // 10

    # Definindo as coordenadas do botão Restart
    x_restart = (LARGURA_TELA - largura_botao) // 2
    y_restart = (ALTURA_TELA - altura_botao) // 2

    # Definindo as coordenadas do botão Menu
    x_naves = x_restart
    y_naves = y_restart + 1.5*altura_botao
    
    # Definindo as coordenadas do botão Menu
    x_menu = x_naves
    y_menu = y_naves + 1.5*altura_botao
    


    surface = pygame.Surface((largura_botao+100,4.5*altura_botao+100),pygame.SRCALPHA)
    surface_pos = (x_restart-50,y_restart-50)

    rect = pygame.Rect(0,0,surface.get_width(),surface.get_height())
    cor = (200,200,200,50)
    pygame.draw.rect(surface,cor,rect)

    # Criando os botões
    x = (surface.get_width() - largura_botao) // 2
    y = 50

    botao_restart = Botao('Restart',(x,y),(largura_botao,altura_botao),branco,preto)

    y += altura_botao * 1.5
    botao_naves = Botao('Naves',(x,y),(largura_botao,altura_botao),branco,preto)

    y += altura_botao * 1.5
    botao_menu = Botao('Menu',(x,y),(largura_botao,altura_botao),branco,preto)

    botoes = [botao_restart,botao_naves,botao_menu]

    go = True
    clock = pygame.time.Clock()
    while go:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                go = False
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_r:
                    return 'roubar'
                
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                
                relative_mouse_pos = (mouse_pos[0] - surface_pos[0], mouse_pos[1] - surface_pos[1])
                
                if botao_restart.collide_mouse(relative_mouse_pos):
                    return 'Jogar', nave_selecionada

                if botao_naves.collide_mouse(relative_mouse_pos):
                    nave_selecionada = interface_naves(screen,fundo,nave_selecionada)
                
                if botao_menu.collide_mouse(relative_mouse_pos):
                    return None, nave_selecionada
        
        
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - surface_pos[0], mouse_pos[1] - surface_pos[1])
        for botao in botoes:
            if botao.collide_mouse(relative_mouse_pos):
                botao.color_button = cinza
            else:
                botao.color_button = branco
            botao.atualizar_botao()
            botao.desenhar(surface)

        screen.blit(fundo,(0,0))
        desenhar_tela(screen,fundo,nave,paredes)
        txt_game_over.exibir_titulo(screen)
        screen.blit(surface,(surface_pos))

        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - surface_pos[0], mouse_pos[1] - surface_pos[1])

        # 60 FPS
        clock.tick(60)

        # Atualizando a tela
        pygame.display.flip()

def pause(screen, surface, titulo, botoes, coord_surface):
    branco = (255,255,255)
    cinza = (200,200,200,100)

    surface.fill(cinza)

    titulo.atualizar_titulo()

    mouse_pos = pygame.mouse.get_pos()
    for botao in botoes:
        relative_mouse_pos = (mouse_pos[0] - coord_surface[0], mouse_pos[1] - coord_surface[1])
        if botao.collide_mouse(relative_mouse_pos):
            botao.color_button = cinza
        else:
            botao.color_button = branco
        botao.atualizar_botao()
        botao.desenhar(surface)
    
    for i
    titulo.exibir_titulo(screen)
    return surface

def main_loop(screen,fundo,nave_selecionada):

    # Criar nave e obstáculos
    nave,paredes = criar_objetos(screen,nave_selecionada)

    # Cores
    branco = (255,255,255)
    preto = (0,0,0)

    # Definindo as dimensões dos botões
    largura_botao = LARGURA_TELA // 6
    altura_botao = ALTURA_TELA // 10
    size_botao = (largura_botao,altura_botao)


    # Criando a superfície dos botões
    surface = pygame.Surface((LARGURA_TELA // 3, ALTURA_TELA * 0.7), pygame.SRCALPHA)
    x_surface_pause = (LARGURA_TELA - surface.get_width()) // 2
    y_surface_pause = (ALTURA_TELA - surface.get_height()) // 2
    coord_surface = (x_surface_pause, y_surface_pause)
    
    # Título 'Jogo Pausado'
    font_size = surface.get_width() // 10
    x = 'center'
    y = y_surface_pause + 50
    jogo_pausado = Titulo('Jogo Pausado',font_size,(x,y))

    # Definindo as coordenadas do botão Continuar
    x = (surface.get_width() - largura_botao) // 2
    y = (surface.get_height() - altura_botao) // 2
    dest_continuar = (x,y)

    botao_continuar = Botao('Continuar',dest_continuar,size_botao,branco,preto)

    y += altura_botao * 1.5
    botao_sair = Botao('Menu', (x,y), size_botao,branco,preto)


    botoes = [botao_continuar, botao_sair]

    # Clock para definir fps
    clock = pygame.time.Clock()
    fps = 60

    timer = 0
    pontuacao = 0

    colidiu = False
    espaco_pressionado = False
    esc_pressionado = False
    pausado = False
    roubar = False

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
                
                elif evento.key == pygame.K_ESCAPE and not esc_pressionado:
                    # Jogo pausado
                    esc_pressionado = True 
                    pausado = True if not pausado else False

                elif evento.key == pygame.K_UP:
                    nave.mover(0)

                elif evento.key == pygame.K_DOWN:
                    nave.mover(1)
                
                elif evento.key == pygame.K_r:
                    roubar = True
                

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    espaco_pressionado = False
                if evento.key == pygame.K_ESCAPE:
                    esc_pressionado = False
                if evento.key == pygame.K_r:
                    roubar = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and pausado:
                for botao in botoes:
                    relative_mouse_pos = (evento.pos[0] - coord_surface[0], evento.pos[1] - coord_surface[1])
                    if botao.collide_mouse(relative_mouse_pos):
                        if botao.get_event() == 'Continuar':
                            pausado = False
                        else:
                            return None, nave_selecionada

                
        if pausado:
            surface_pause = pause(screen, surface, jogo_pausado, botoes, coord_surface)


        # Contador do tempo
        timer += 1 / fps

        # Atualizar pontuação
        for parede in paredes:
            if parede.pontuacao(nave):
                pontuacao += 1

        # Desenhar todos os objetos e pontuação na tela
        desenhar_tela(screen,fundo,nave,paredes)
        if pausado:
            screen.blit(surface_pause, coord_surface)
        else:
            atualizar_posicao(nave,paredes)
            exibir_pontuacao(screen,pontuacao,timer)
        
        # Verificar colisões
        if not roubar:
            colidiu = verificar_colisao(nave,paredes)
            if colidiu:
                event, nave_selecionada = game_over(screen,fundo,nave_selecionada,nave,paredes)
                if event == 'roubar':
                    roubar = True
                else:
                    return event, nave_selecionada
                
        
        # Atualizar a tela
        pygame.display.flip()

        # Definindo o FPS
        clock.tick(fps)

def main(screen,fundo):
     # Definir a primeira nave como a nave selecionada
    nave_selecionada = 1
    event = None

    # Loop que alterna entre cada interface (menu inicial, seleção de naves e o jogo)
    while True:
        if not event:
            event = interface_inicial(screen,fundo)

        if event == 'Sair':
            pygame.quit()
            quit()

        elif event == 'Naves':
            nave_selecionada = interface_naves(screen,fundo,nave_selecionada)
            event = None

        elif 'Jogar':
            event,nave_selecionada = main_loop(screen,fundo,nave_selecionada)
        else:
            event = None

main(screen,FUNDO)

pygame.quit()