import pygame
from components.nave import Nave
from pontuacao import carregar_pontuacao, salvar_pontuacao
from interfaces.ui_jogo import Interface, Paredes


class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.nave = Nave(screen)
        self.paredes = Paredes(self.screen)
        self.interface = Interface(self.screen)
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

    def exibir_txt_pontuacoes(self) -> None:
        txt_pontuacao = self.font2.render(str(self.pontuacao), True, (0,255,255))
        txt_recorde_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, (255,255,255))

        x = txt_pontuacao.get_rect(center = self.interface.game_over.interface.get_rect().center).left
        y = self.titulo_game_over.coord[1] + self.titulo_game_over.titulo.get_height() + 20
        self.interface_game_over.blit(txt_pontuacao, (x,y))

        x = txt_recorde_pontuacao.get_rect(center=self.interface_game_over.interface.get_rect().center).left
        self.interface_game_over.blit(txt_recorde_pontuacao, (x,y+txt_pontuacao.get_height()+20))

    def exibir_naves(self):
        self.nave.exibir()
        for parede in self.paredes:
            print(parede)
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
            for botao in self.interface.botoes_game_over:
                if botao.clicked(event):
                    return botao.get_event()
            
    
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