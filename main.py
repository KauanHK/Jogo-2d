import pygame
from utils.imagens import carregar_imagem
from interfaces.jogo_manager import JogoManager
from interfaces.menu_principal_manager import MenuPrincipalManager
from interfaces.menu_naves_manager import MenuNavesManager
from typing import Union, Literal

class Manager:

    INTERFACES = {
        "Jogo": JogoManager,
        "MenuPrincipal": MenuPrincipalManager,
        "MenuNaves": MenuNavesManager,
    }

    def __init__(self, interface: Union[JogoManager, MenuPrincipalManager, MenuNavesManager] = MenuPrincipalManager):
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

        self.interface = self.interface(self.screen.get_size())
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
            self.interface.run(self.screen)
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        print('\nObrigado por jogar meu jogo :)')
        print('https://github.com/KauanHK/Jogo-2d.git')
        pygame.quit()
    

    def loadEvent(self, event) -> None:
        '''Gerencia um pygame.Event. 
        Pode atualizar o valor de self.rodando para finalizar o jogo, 
        alternar o valor de self.interface, 
        ou não fazer nada, dependendo do evento.'''
        interface = self.interface.load_event(event)
        if event.type == pygame.QUIT or interface == 'sair':
            self.rodando = False
        elif interface is not None:
            self.interface = self.nova_interface(interface)

    def nova_interface(self, interface: Literal["Jogo", "MenuPrincipal", "MenuNaves", "sair"]):
        if interface == "sair":
            self.rodando = False
        return self.INTERFACES[interface](self.screen.get_size())

if __name__ == '__main__':
    manager = Manager()
    manager.run()