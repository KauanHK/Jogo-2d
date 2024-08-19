import pygame
import os

def carregar_imagem(*path, size: tuple[int,int] | None = None):
    try:
        imagem = pygame.image.load(os.path.join(*path))
    except:
        print(*path)
        raise TypeError(f'Erro ao carregar imagem {path}')
    if size:
        largura, altura = size

        largura_original, altura_original = imagem.get_size()
        razao = largura_original / altura_original
        if largura == 'auto':
            largura = altura * razao
        elif altura == 'auto':
            altura = largura / razao

        size = (largura,altura)
        imagem = pygame.transform.scale(imagem, size)
    return imagem