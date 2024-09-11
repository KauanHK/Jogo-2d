import pygame
from typing import Literal, Union
from objetos import Nave, Parede
from pontuacao import carregar_pontuacao, salvar_pontuacao
from imagens import carregar_imagem, mudar_tamanho
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
        self.botao_voltar = self.criar_botao_voltar()
        self.IMAGENS = self.carregar_imagens()
        self.surface_naves = self.criar_surface_naves()
        self.coord_surface_naves = self.calcular_coord_surf_naves()
        self.atualizar_surface_naves()
        self.img_rects = self.criar_imgs_rects()


    def criar_botao_voltar(self) -> Botao:
        return Botao(self.screen, MenuPrincipal, ('center', self.screen.get_height()*0.8), (200,70), 'Voltar', 40)

    def carregar_imagens(self) -> list[pygame.Surface]:
        return [carregar_imagem(f'imagens' ,f'nave{i}.png', size=(100,'auto')) for i in range(1,6)]
    
    def criar_surface_naves(self) -> pygame.Surface:
        '''Cria a superfície onde aparecem todas as naves do jogo no menu'''
        size = (self.screen.get_width() * 0.8, 150)
        return pygame.Surface(size, pygame.SRCALPHA)

    def atualizar_surface_naves(self):
        self.surface_naves = self.criar_surface_naves()
        self.fundos = self.criar_fundos_naves()
        self.lefts_fundos = self.calcular_x_fundos()
        self.inserir_imgs_naves_nos_fundos()
        self.inserir_fundos()

    def calcular_coord_surf_naves(self) -> tuple[int]:
        x = self.surface_naves.get_rect(center = self.screen.get_rect().center).left
        y = self.screen.get_height() * 0.5
        return x,y
    
    def criar_fundos_naves(self) -> list[pygame.Surface]:
        '''Retorna uma lista de Surface's que correspondem ao fundo das imagens das naves.
        Um fundo é cinza transparente, correspondente à nave que está selecionada.'''
        fundos = []
        for i in range(len(self.IMAGENS)):
            fundo = pygame.Surface((150,150), pygame.SRCALPHA)
            if self.nave_selecionada == i+1:
                fundo.fill(CINZA_TRANSPARENTE)
            fundos.append(fundo)
        return fundos
    
    def calcular_x_fundos(self) -> list[int]:
        coords = []
        largura_surface = self.surface_naves.get_width()
        num_imgs = len(self.IMAGENS)
        x_aumento = largura_surface / (num_imgs - 1)
        for i, fundo in enumerate(self.fundos):
            x = x_aumento * i - fundo.get_width() / 2
            if x < 0:
                x = 0
            elif x + fundo.get_width() > largura_surface:
                x = largura_surface - fundo.get_width()
            coords.append(x)
        return coords

    def hover_naves(self, fundos: list[pygame.Surface]):
        y = self.coord_surface_naves[1]
        mouse_pos = pygame.mouse.get_pos()
        imgs = []
        for x, img_nave in zip(self.lefts_fundos, fundos):
            if img_nave.get_rect(topleft = (x, y)).collidepoint(mouse_pos):
                size = img_nave.get_size()
                if size[0] < self.IMAGENS[0].get_width() * 1.5:
                    size = (s * 1.05 for s in size)
                img_nave = mudar_tamanho(img_nave, size)
            imgs.append(img_nave)
        return imgs

    def inserir_imgs_naves_nos_fundos(self) -> None:
        '''Insere as imagens das naves nos seus fundos. Retorna None'''
        imgs_naves = self.hover_naves(self.IMAGENS)
        for fundo, img_nave in zip(self.fundos, imgs_naves):
            x,y = img_nave.get_rect(center = fundo.get_rect().center).topleft
            fundo.blit(img_nave, (x,y))
    
    def criar_imgs_rects(self) -> list[pygame.Rect]:
        '''Cria a lista self.img_rects, que armazena os Rect's de todas as imagens das naves. 
        Depende do Surface self.coord_surface_naves, que deve ser criado antes de executar este método.'''
        y = self.coord_surface_naves[1]
        rects = []
        for fundo, left in zip(self.fundos, self.lefts_fundos):
            x = self.coord_surface_naves[0] + left
            rect = fundo.get_rect(topleft = (x, y))
            rects.append(rect)
        return rects

    def inserir_fundos(self):
        for x, fundo in zip(self.lefts_fundos, self.fundos):
            self.surface_naves.blit(fundo, (x,0))
            

    def exibir_naves(self) -> None:
        self.screen.blit(self.surface_naves, self.coord_surface_naves)

    def run(self) -> None:
        self.botao_voltar.exibir()
        if self.nave_selecionada != Nave.selecionada:
            self.nave_selecionada = Nave.selecionada
            self.atualizar_surface_naves()
        self.exibir_naves()
    
    
    def loadEvent(self, event: pygame.event.Event) -> MenuPrincipal | None:
        self.botao_voltar.hover()
        if self.botao_voltar.clicked(event):
            return self.botao_voltar.event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, nave_rect in enumerate(self.img_rects):
                if nave_rect.collidepoint(event.pos):
                    Nave.selecionada = i+1
                    break

class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.nave = Nave(screen)
        self.paredes = self.criar_paredes()
        self.interface_pause = self.criar_popup()
        self.interface_game_over = self.criar_popup()
        self.titulo_game_over = self.criar_titulo_game_over()
        self.botoes_game_over = self.criar_botoes_game_over()
        self.nave_mask = self.nave.getMask()
        self.fragmento_mask = self.get_fragmento_mask()

        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)

        self.pausado = False
        self.pontuacao = 0
        self.max_pontuacao = 0
        self.salvo = False

    def get_fragmento_mask(self) -> pygame.Mask:
        '''Retorna o Mask de um fragmento'''
        return self.paredes[0].fragmentos[0].getMask()  # Só é necessário pegar o Mask de um fragmento, pois todos os fragmentos são iguais

    def criar_paredes(self) -> list[Parede]:
        largura_tela = self.screen.get_width()
        largura_parede = largura_tela / 10
        largura_parede = 80 if largura_parede > 80 else largura_parede
        x = largura_tela * 0.95
        x_aumento = largura_tela / 4
        img = carregar_imagem('imagens', 'obstaculo.jpg', size=(largura_parede,'auto'))
        paredes = []
        for i in range(4):
            paredes.append(Parede(self.screen, img, x))
            x += x_aumento
        return paredes

    def criar_popup(self) -> PopUp:
        largura = self.screen.get_width() * 0.4
        altura = self.screen.get_height() * 0.7
        size = (largura, altura)
        interface = PopUp(self.screen, size, CINZA_TRANSPARENTE)
        return interface

    def criar_titulo_game_over(self) -> Titulo:
        return Titulo(self.interface_game_over.interface, 'center', 50, 'Game Over', VERMELHO, 100)

    def criar_botoes_game_over(self) -> list[Botao]:
        y = self.screen.get_height() * 0.6
        botao_restart = Botao(self.screen, Jogo, ('center', y), (self.interface_game_over.size[0]/2, 60), 'Restart', 40)
        botao_sair = Botao(self.screen, MenuPrincipal, ('center', y + botao_restart.size[1]+20), (self.interface_game_over.size[0]/2, 60), 'Menu', 40)
        return botao_restart, botao_sair
    
    def exibir_txt_pontuacoes(self) -> None:
        txt_pontuacao = self.font2.render(str(self.pontuacao), True, (0,255,255))
        txt_recorde_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, (255,255,255))

        x = txt_pontuacao.get_rect(center = self.interface_game_over.interface.get_rect().center).left
        y = self.titulo_game_over.coord[1] + self.titulo_game_over.titulo.get_height() + 20
        self.interface_game_over.blit(txt_pontuacao, (x,y))

        x = txt_recorde_pontuacao.get_rect(center=self.interface_game_over.interface.get_rect().center).left
        self.interface_game_over.blit(txt_recorde_pontuacao, (x,y+txt_pontuacao.get_height()+20))

    def run(self) -> None:
        '''Executa um frame do jogo'''
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
        x = (self.screen.get_width() - txt_pontuacao.get_width()) / 2
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
            
    
    def colidiu(self) -> bool:
        nave_x, nave_y = self.nave.x, self.nave.y

        for parede in self.paredes:
            
            for fragmento in parede.fragmentos:
                x_img, y_img = parede.x, fragmento.y
                parede_offset = (x_img - nave_x, y_img - nave_y)
                if self.nave_mask.overlap(self.fragmento_mask, parede_offset):
                    return True
        return False
    
    def atualizarPontuacao(self) -> None:
        for parede in self.paredes:
            if self.nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True

