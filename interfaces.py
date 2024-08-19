import pygame
from objetos import Nave, Parede
from pontuacao import carregar_pontuacao, salvar_pontuacao
from imagens import carregar_imagem
from titulo import Titulo
from botao import Botao
from cores import *


class MenuPrincipal:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.titulo = self.criar_titulo()
        self.botoes = self.criar_botoes()

    def criar_titulo(self):
        return Titulo(self.screen, 'center', self.screen.get_height()/6, 'Jogo da Nave', (255,0,0), 120)

    def criar_botoes(self, size: tuple[int,int] | None = (280, 80), font_size: int | None = 48):
        centery = self.screen.get_height() // 5 * 3
        sep = size[1] + 40
        botoes = [
            Botao(self.screen, Jogo, ('center', centery-sep), size, 'Jogar', font_size),
            Botao(self.screen, MenuNaves, ('center', centery), size, 'Naves', font_size),
            Botao(self.screen, None, ('center', centery+sep), size, 'Sair', font_size)
        ]
        return botoes

    def run(self):
        
        self.titulo.atualizarCor()
        self.titulo.update()
        self.titulo.exibir()

        for botao in self.botoes:
            botao.exibir()

    def loadEvent(self, event):
        for botao in self.botoes:
            botao.hover()    
            if botao.clicked(event):
                if botao.event is None:
                    return 'sair'
                return botao.event

class MenuNaves:

    IMAGENS = [carregar_imagem(f'imagens' ,f'nave{i}.png', size=(100,'auto')) for i in range(1,6)]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.largura_tela, self.altura_tela = self.screen.get_size()
        self.botao_voltar = Botao(self.screen, MenuPrincipal, ('center', self.screen.get_height()*0.8), (200,70), 'Voltar', 40)
        self.fundo_nave_selecionada = pygame.Surface((150, 150), pygame.SRCALPHA)

    def run(self):
        self.botao_voltar.exibir()
        self.exibirNaves()
    
    def exibirNaves(self):
        self.img_rects = []
        
        x = (self.largura_tela / 8)
        x_aumento = x * 8/5
        x -= 75
        y = self.altura_tela / 2
        for i,img in enumerate(self.IMAGENS):
            if i+1 == Nave.selecionada:
                coord = img.get_rect(center=self.fundo_nave_selecionada.get_rect().center).topleft
                self.fundo_nave_selecionada.fill(CINZA_TRANSPARENTE)
                self.fundo_nave_selecionada.blit(img, coord)
                self.screen.blit(self.fundo_nave_selecionada, (x-25,y-25))
            else:
                self.screen.blit(img, (x,y))
            self.img_rects.append(img.get_rect(topleft=(x,y)))
            x += x_aumento
    
    def loadEvent(self, event):
        self.botao_voltar.hover()
        if self.botao_voltar.clicked(event):
            return self.botao_voltar.event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, nave_rect in enumerate(self.img_rects):
                if nave_rect.collidepoint(event.pos):
                    Nave.selecionada = i+1

class Jogo:

    class Criar:

        @staticmethod
        def paredes(screen: pygame.Surface):
            largura_tela = screen.get_width()
            largura_parede = largura_tela / 10
            largura_parede = 80 if largura_parede > 80 else largura_parede
            x = largura_tela * 0.95
            x_aumento = largura_tela / 4
            img = carregar_imagem('imagens', 'obstaculo.jpg', size=(largura_parede,'auto'))
            paredes = []
            for i in range(4):
                paredes.append(Parede(screen, img, x))
                x += x_aumento
            return paredes
        
        class PopUp:
            def __init__(self,
                         screen: pygame.Surface,
                         size: tuple[int,int] | None = (200,200),
                         color: tuple[int,int,int] | None = (255,255,255)):
                self.screen = screen
                self.size = size
                self.color = color

                self.interface = pygame.Surface(size, pygame.SRCALPHA)
                self.interface.fill(self.color)
                self.coord = self.interface.get_rect(center=self.screen.get_rect().center).topleft

            def exibir(self):
                self.screen.blit(self.interface, self.coord)

            def blit(self, surface: pygame.Surface, dest: tuple[int,int]):
                self.interface.blit(surface, dest)


    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.largura_tela = self.screen.get_width()
        self.altura_tela = self.screen.get_height()

        self.nave = Nave(screen)
        self.paredes = self.Criar.paredes(self.screen)
        self.img_mask = pygame.mask.from_surface(self.paredes[0].all_paredes[0].img)
        self.interface_pause, self.interface_game_over = self.criar_interfaces()
        self.titulo_game_over = self.criar_titulo_game_over()
        self.botoes_game_over = self.criar_botoes_game_over()

        self.pausado = False

        self.pontuacao = 0
        self.max_pontuacao = 0
        self.salvo = False

        self.nave_mask = self.nave.getMask()
        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)


    def criar_interfaces(self):
        largura = self.screen.get_width() * 0.4
        altura = self.screen.get_height() * 0.7
        size_interfaces = (largura, altura)
        interface = self.Criar.PopUp(self.screen, size_interfaces, CINZA_TRANSPARENTE)
        return interface, interface

    def criar_titulo_game_over(self):
        return Titulo(self.interface_game_over.interface, 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes_game_over(self):
        y = self.altura_tela * 0.6
        botao_restart = Botao(self.screen, Jogo, ('center', y), (self.interface_game_over.size[0]/2, 60), 'Restart', 40)
        botao_sair = Botao(self.screen, MenuPrincipal, ('center', y + botao_restart.size[1]+20), (self.interface_game_over.size[0]/2, 60), 'Menu', 40)
        return botao_restart, botao_sair
    
    def exibir_txt_pontuacoes(self):
        txt_pontuacao = self.font2.render(str(self.pontuacao), True, (0,255,255))
        txt_recorde_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, (255,255,255))

        x = txt_pontuacao.get_rect(center = self.interface_game_over.interface.get_rect().center).left
        y = self.titulo_game_over.coord[1] + self.titulo_game_over.titulo.get_height() + 20
        self.interface_game_over.blit(txt_pontuacao, (x,y))

        x = txt_recorde_pontuacao.get_rect(center=self.interface_game_over.interface.get_rect().center).left
        self.interface_game_over.blit(txt_recorde_pontuacao, (x,y+txt_pontuacao.get_height()+20))

    def run(self):

        self.nave.exibir()
        for parede in self.paredes:
            parede.exibir()

        if self.pausado:
            self.interface_pause.exibir()
        
        elif self.colidiu():
            
            if not self.salvo:
                pontuacoes = carregar_pontuacao()
                pontuacoes.append(self.pontuacao)
                salvar_pontuacao(pontuacoes)
                self.salvo = True
                self.max_pontuacao = max(pontuacoes)

            self.exibir_txt_pontuacoes()
            self.titulo_game_over.exibir()
            
            self.interface_game_over.exibir()
            for botao in self.botoes_game_over:
                botao.exibir()
            
            
        else:
            self.nave.atualizarPosicao()
            for parede in self.paredes:
                parede.atualizarPosicao()
            self.atualizarPontuacao()

        txt_pontuacao = self.font.render(str(self.pontuacao), True, (255,255,255))
        x = (self.largura_tela - txt_pontuacao.get_width()) / 2
        y = 100
        self.screen.blit(txt_pontuacao, (x,y))

    def loadEvent(self, event: pygame.event.Event):
        for botao in self.botoes_game_over:
            botao.hover()
        if event.type == pygame.KEYDOWN:
            if not self.pausado:
                if event.key == pygame.K_UP:
                    self.nave.mudarDirecao(Nave.CIMA)
                elif event.key == pygame.K_DOWN:
                    self.nave.mudarDirecao(Nave.BAIXO)
                elif event.key == pygame.K_SPACE:
                    self.nave.mudarDirecao(Nave.ESPACO)
            if event.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado
        
        if self.colidiu():
            for botao in self.botoes_game_over:
                if botao.clicked(event):
                    return botao.event
            
    
    def colidiu(self):
        nave_x, nave_y = self.nave.x, self.nave.y

        for parede in self.paredes:
            
            for img_parede in parede.all_paredes:
                x_img, y_img = parede.x, img_parede.y
                parede_offset = (x_img - nave_x, y_img - nave_y)
                if self.nave_mask.overlap(self.img_mask, parede_offset):
                    return True
        return False
    
    def atualizarPontuacao(self):
        for parede in self.paredes:
            if self.nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True

class Interface:

    def __init__(self, screen: pygame.Surface, interface: object):
        self.screen = screen
        self.interface = interface(self.screen)
        self.pontuacao = 0
    
    def run(self):
        '''Executa a interface atual'''
        self.interface.run()

    def loadEvent(self, event):
        '''Carrega o evento e define qual interface será executada.
        
        Retorna False se o usuário clicar em 'sair', se não True'''
        interface = self.interface.loadEvent(event)
        if interface == 'sair':
            # Atualizar a variável rodando em 'main.py' para False para finalizar o loop do jogo
            return False
        elif interface is None:
            # Se nenhum evento for detectado, continuar rodando o jogo na mesma interface
            return True
        
        # Foi retornada alguma interface, portanto executá-la e continuar loop do jogo
        self.interface = interface(self.screen)
        return True