import pygame
from components.nave import Nave
from pontuacao import carregar_pontuacao, salvar_pontuacao
from utils.imagens import carregar_imagem
from interfaces.ui_jogo import Interface, Paredes


class Jogo:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        screen_size = self.screen.get_size()
        self.interface = Interface(screen_size)
        self.nave_mask = self.nave.getMask()
        self.fragmento_mask = self.paredes.get_mask()

        self.font = pygame.font.Font(size=80)
        self.font2 = pygame.font.Font(size=120)

        self.pausado = False
        self.pontuacao = 0
        self.max_pontuacao = 0
        self.salvo = False

    


    def get_mask(self) -> pygame.Mask:
        '''Retorna o Mask de um fragmento'''
        return pygame.mask.from_surface(self.img)

    def exibir_txt_pontuacoes(self) -> None:
        txt_pontuacao = self.font2.render(str(self.pontuacao), True, (0,255,255))
        txt_recorde_pontuacao = self.font.render(f'Recorde: {self.max_pontuacao}', True, (255,255,255))

        x = txt_pontuacao.get_rect(center = self.interface.game_over.popup.interface.get_rect().center).left
        y = self.interface.game_over.titulo.coord[1] + self.interface.game_over.titulo.surface.get_height() + 20
        self.interface.game_over.popup.interface.blit(txt_pontuacao, (x,y))

        x = txt_recorde_pontuacao.get_rect(center=self.interface.game_over.popup.interface.get_rect().center).left
        self.interface.game_over.popup.interface.blit(txt_recorde_pontuacao, (x,y+txt_pontuacao.get_height()+20))


    def salvar_pontuacao(self):
        pontuacoes = carregar_pontuacao()
        pontuacoes.append(self.pontuacao)
        salvar_pontuacao(pontuacoes)
        self.salvo = True
        self.max_pontuacao = max(pontuacoes)

    def exibir_pontuacao(self):
        txt_pontuacao = self.font.render(str(self.pontuacao), True, (255,255,255))
        x = (self.screen.get_width() - txt_pontuacao.get_width()) / 2
        y = 100
        self.screen.blit(txt_pontuacao, (x,y))

    def run(self) -> None:
        '''Executa um frame do jogo'''
        self.interface.update(self.pausado, self.colidiu())
        self.interface.exibir()

        # Exibir o básico na tela
        self.nave.exibir(self.screen)
        for parede in self.paredes:
            parede.exibir(self.screen)
        self.exibir_pontuacao()

        
        
        
            
        else:
            self.nave.atualizarPosicao()
            for parede in self.paredes:
                parede.atualizarPosicao()
            self.atualizarPontuacao()

        

    def load_event(self, event: pygame.event.Event):
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
            for botao in self.interface.game_over.botoes:
                if botao.clicked(event):
                    return botao.get_event()
            
    
    def colidiu(self) -> bool:
        nave_x, nave_y = self.nave.x, self.nave.y

        for parede in self.paredes:
            x_fragmento = parede.x
            for y_fragmento in parede.tops:
                fragmento_offset = (x_fragmento - nave_x, y_fragmento - nave_y)
                if self.nave_mask.overlap(self.fragmento_mask, fragmento_offset):
                    return True
        return False
    
    def atualizarPontuacao(self) -> None:
        for parede in self.paredes:
            if self.nave.x > parede.x and not parede.pontuou:
                self.pontuacao += 1
                parede.pontuou = True