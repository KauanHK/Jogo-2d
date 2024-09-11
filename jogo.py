import pygame
from imagens import carregar_imagem
import interfaces
from typing import Union

class Manager:


    def __init__(self, interface: Union[interfaces.Jogo, interfaces.MenuPrincipal, interfaces.MenuNaves] = interfaces.MenuPrincipal):
        '''
        Parâmetro
        ---------
        interface (Jogo, MenuPrincipal, MenuNaves) opcional: Interface inicial do jogo, por padrão MenuPrincipal.

        '''
        self.interface = interface

    def _setup(self) -> None:
        '''Cria os princiapis atributos para executar o jogo'''

        pygame.init()
        pygame.display.set_caption('Jogo da Nave')

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((500,400))

        self.interface = self.interface(self.screen)
        self.FUNDO = carregar_imagem('imagens', 'fundo.jpg', size=self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self) -> None:
        '''Executa o jogo'''
        
        self._setup()
        self.rodando = True
        while self.rodando:
            for event in pygame.event.get():
                self.loadEvent(event)

            self.screen.blit(self.FUNDO, (0,0))
            self.interface.run()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        print('\nObrigado por jogar meu jogo :)')
        print('Desenvolvido por Kauan Henrique Kaestner')
        pygame.quit()
    

    def loadEvent(self, event) -> None:
        '''Gerencia um pygame.Event. 
        Pode atualizar o valor de self.rodando para finalizar o jogo, 
        alternar o valor de self.interface, 
        ou não fazer nada, dependendo do evento.'''
        if event.type == pygame.QUIT:
            self.rodando = False
            return
        
        interface = self.interface.loadEvent(event)
        if interface is not None:
            if interface == 'sair':
                self.rodando = False
                return
            self.interface = interface(self.screen)