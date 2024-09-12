import pygame
from components.nave import Nave
from pontuacao import carregar_pontuacao, salvar_pontuacao
from utils.imagens import carregar_imagem
from interfaces.ui_jogo import Interface
from components.parede import Parede


class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.nave = Nave(screen)
        self.paredes = self.criar_paredes()
        self.interface = Interface(self.screen)
        self.nave_mask = self.nave.getMask()
        self.fragmento_mask = self.get_fragmento_mask()

        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)

        self.pausado = False
        self.pontuacao = 0
        self.max_pontuacao = 0
        self.salvo = False

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

    def get_fragmento_mask(self) -> pygame.Mask:
        '''Retorna o Mask de um fragmento'''
        return self.paredes[0].fragmentos[0].getMask()  # Só é necessário pegar o Mask de um fragmento, pois todos os fragmentos são iguais

    def exibir_txt_pontuacoes(self) -> None:
        txt_pontuacao = self.font2.render(str(self.pontuacao), True, (0,255,255))
        txt_recorde_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, (255,255,255))

        x = txt_pontuacao.get_rect(center = self.interface_game_over.interface.get_rect().center).left
        y = self.titulo_game_over.coord[1] + self.titulo_game_over.titulo.get_height() + 20
        self.interface_game_over.blit(txt_pontuacao, (x,y))

        x = txt_recorde_pontuacao.get_rect(center=self.interface_game_over.interface.get_rect().center).left
        self.interface_game_over.blit(txt_recorde_pontuacao, (x,y+txt_pontuacao.get_height()+20))

    def exibir_naves(self):
        self.nave.exibir()
        for parede in self.paredes:
            parede.exibir()

    def salvar_pontuacao(self):
        pontuacoes = carregar_pontuacao()
        pontuacoes.append(self.pontuacao)
        salvar_pontuacao(pontuacoes)
        self.salvo = True
        self.max_pontuacao = max(pontuacoes)

    def run(self) -> None:
        '''Executa um frame do jogo'''
        self.exibir_naves()

        if self.pausado:
            self.interface.pause.exibir()
        
        elif self.colidiu():
            self.interface.game_over.exibir()
            if not self.salvo:
                self.salvar_pontuacao()

            self.exibir_txt_pontuacoes()
            self.interface.titulo_game_over.exibir()
            
        else:
            self.nave.atualizarPosicao()
            for parede in self.paredes:
                parede.atualizarPosicao()
            self.atualizarPontuacao()

        txt_pontuacao = self.font.render(str(self.pontuacao), True, (255,255,255))
        x = (self.screen.get_width() - txt_pontuacao.get_width()) / 2
        y = 100
        self.screen.blit(txt_pontuacao, (x,y))

    def loadEvent(self, event: pygame.event.Event):
        for botao in self.interface.botoes_game_over:
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