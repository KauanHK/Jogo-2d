import pygame
from interfaces import Interface, MenuPrincipal
from imagens import carregar_imagem

def main():

    pygame.init()

    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    FUNDO = carregar_imagem('imagens', 'fundo.jpg', size=screen.get_size())
    pygame.display.set_caption('Jogo')

    interface = Interface(screen, MenuPrincipal)
    clock = pygame.time.Clock()
    fps = 60
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                break

            if not interface.loadEvent(event):
                rodando = False
                break
            
        screen.blit(FUNDO, (0,0))
        interface.run()
        
        pygame.display.flip()
        clock.tick(fps)
    
    print('\nObrigado por jogar meu jogo :)')
    print('Desenvolvido por Kauan Henrique Kaestner')
    pygame.quit()

if __name__ == '__main__':
    main()
