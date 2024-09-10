import pygame
from typing import Literal, Union
from objetos import Nave, Parede
from pontuacao import carregar_pontuacao, salvar_pontuacao
from imagens import carregar_imagem
from titulo import Titulo
from botao import Botao
from cores import *
from popup import PopUp


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

    def loadEvent(self, event) -> Literal['sair'] | Union["Jogo", "MenuNaves"] | None:
        for botao in self.botoes:
            botao.hover()    
            if botao.clicked(event):
                if botao.event is None:
                    return 'sair'
                return botao.event

class MenuNaves:


    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.nave_selecionada = Nave.selecionada
        self.criar_botao_voltar()
        self.carregar_imagens()
        self.criar_surface_naves()

    def criar_botao_voltar(self) -> None:
        self.botao_voltar = Botao(self.screen, MenuPrincipal, ('center', self.screen.get_height()*0.8), (200,70), 'Voltar', 40)

    def carregar_imagens(self) -> None:
        self.IMAGENS = [carregar_imagem(f'imagens' ,f'nave{i}.png', size=(100,'auto')) for i in range(1,6)]

    def _criar_surface_naves(self) -> None:
        '''Método interno para criar o Surface onde ficarão os surface das naves'''

        # Criar a superfície onde ficarão todas as 5 naves
        size = (self.screen.get_width() * 0.8, 150)
        self.surface_naves = pygame.Surface(size, pygame.SRCALPHA)
        self.x_surface = self.surface_naves.get_rect(center = self.screen.get_rect().center).left
        self.y_surface = self.altura_tela * 0.5

    def criar_surface_nave(self, img: pygame.Surface,  nave_i: int) -> pygame.Surface:
        '''Cria um Surface onde ficará a imagem da nave. O fundo é cinza transparente caso a nave esteja selecionada'''
        surface_fundo_nave = pygame.Surface((150, 150), pygame.SRCALPHA)
        if nave_i == self.nave_selecionada:
            surface_fundo_nave.fill(CINZA_TRANSPARENTE)
        coord = img.get_rect(center = surface_fundo_nave.get_rect().center).topleft
        surface_fundo_nave.blit(img, coord)
        return surface_fundo_nave

    def criar_imgs_rects(self, img: pygame.Surface, x: int, y: int) -> None:
        '''Cria a lista self.img_rects, que armazena os Rect's de todas as imagens das naves.'''
        self.img_rects = []
        for i, img in enumerate(self.IMAGENS):
            x = self.x_surface + (self.surface_naves.get_width() / 5 * i) + 25
            y = self.y_surface + 25
            rect = img.get_rect(topleft = (x,y), height = img.get_height()+25)
            self.img_rects.append(rect)

    def criar_surface_naves(self) -> None:
        '''Cria a superfície onde aparecem todas as naves do jogo no menu'''
        self._criar_surface_naves()
        for i, img in enumerate(self.IMAGENS):
            # Isso cria o Surface da nave, com um fundo cinza transparente se for a nave selecionada
            surface_fundo_nave = self.criar_surface_nave(img, i+1)

            # Adicionar o Surface da nave ao Surface das naves
            x = self.surface_naves.get_width() / 5 * i
            self.surface_naves.blit(surface_fundo_nave, (x, 0))
        

    def exibir_naves(self) -> None:
        self.screen.blit(self.surface_naves, (self.x_surface, self.y_surface))

    def run(self) -> None:
        self.botao_voltar.exibir()
        if self.nave_selecionada != Nave.selecionada:
            self.nave_selecionada = Nave.selecionada
            self.criar_surface_naves()
        self.exibir_naves()
    
    
    def loadEvent(self, event: pygame.event.Event) -> MenuPrincipal | None:
        self.botao_voltar.hover()
        if self.botao_voltar.clicked(event):
            return self.botao_voltar.event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, nave_rect in enumerate(self.img_rects):
                if nave_rect.collidepoint(event.pos):
                    Nave.selecionada = i+1

class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.nave = Nave(screen)
        self.paredes = self.criar_paredes()
        self.criar_titulo_game_over()
        self.criar_botoes_game_over()
        self.interface_pause = self.criar_popup()
        self.interface_game_over = self.criar_popup()
        self.nave_mask = self.nave.getMask()
        
        # Só é necessário pegar o Mask de um fragmento, pois todos os fragmentos são iguais
        self.fragmento_mask = self.get_fragmento_mask()
        self.fragmento_mask = pygame.mask.from_surface(self.paredes[0].fragmentos[0].img)

        self.pausado = False

        self.pontuacao = 0
        self.max_pontuacao = 0
        self.salvo = False

        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)

    def get_fragmento_mask(self):
        return self.paredes.fragmentos[0].getMask()

    def criar_paredes(self, screen: pygame.Surface) -> list[Parede]:
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


    def criar_popup(self):
        largura = self.screen.get_width() * 0.4
        altura = self.screen.get_height() * 0.7
        size_interfaces = (largura, altura)
        interface = PopUp(self.screen, size_interfaces, CINZA_TRANSPARENTE)
        return interface

    def criar_titulo_game_over(self) -> None:
        self.titulo_game_over = Titulo(self.interface_game_over.interface, 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes_game_over(self):
        y = self.screen.get_height() * 0.6
        botao_restart = Botao(self.screen, Jogo, ('center', y), (self.interface_game_over.size[0]/2, 60), 'Restart', 40)
        botao_sair = Botao(self.screen, MenuPrincipal, ('center', y + botao_restart.size[1]+20), (self.interface_game_over.size[0]/2, 60), 'Menu', 40)
        self.botoes_game_over = (botao_restart, botao_sair)
    
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
        for parede in self.criar_paredes:
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
            for parede in self.criar_paredes:
                parede.atualizarPosicao()
            self.atualizarPontuacao()

        txt_pontuacao = self.font.render(str(self.pontuacao), True, (255,255,255))
        x = (self.largura_tela - txt_pontuacao.get_width()) / 2
        y = 100
        self.screen.blit(txt_pontuacao, (x,y))

    def loadEvent(self, event: pygame.event.Event) -> MenuPrincipal | MenuNaves | None:
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

        for parede in self.criar_paredes:
            
            for img_parede in parede.all_paredes:
                x_img, y_img = parede.x, img_parede.y
                parede_offset = (x_img - nave_x, y_img - nave_y)
                if self.nave_mask.overlap(self.img_mask, parede_offset):
                    return True
        return False
    
    def atualizarPontuacao(self):
        for parede in self.criar_paredes:
            if self.nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True

