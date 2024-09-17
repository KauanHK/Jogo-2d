import pygame
from interfaces.jogo import JogoManager

def run(test, load_event = None):

    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif load_event is not None:
                load_event(event)
        
        test()

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


def load_event(event: pygame.event.Event, manager: JogoManager):
    manager.load_event(event)

def test(screen, manager: JogoManager):
    screen.fill((0,0,0))
    manager.update()
    manager.exibir(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    manager = JogoManager(screen.get_size())
    run(
        test = lambda: test(screen, manager),
        load_event = lambda event: load_event(event, manager)
    )

if __name__ == '__main__':
    main()
