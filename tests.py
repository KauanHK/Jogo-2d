# import pygame

# def run(test, load_event = None):
#     rodando = True
#     while rodando:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 rodando = False
#             elif load_event is not None:
#                 load_event(event)
        
#         test()

#         pygame.display.flip()

#     pygame.quit()


# def load_event(event: pygame.event.Event):
#     pass

# def test(screen, surface):
#     screen.fill((255,255,255))
#     coord = surface.get_rect(center = screen.get_rect().center).topleft
#     screen.blit(surface, coord)

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800,600))
#     surface = pygame.Surface((400,400), pygame.SRCALPHA)
#     surface.fill((200,200,200,100))
#     run(
#         test = lambda: test(screen, surface)
#     )

# if __name__ == '__main__':
#     main()


def func1():
    print('func1')
    return True

def func2():
    print('func2')
    return True

if not func1() or not func2():
    pass