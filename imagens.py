import pygame
import os

def razao(largura, altura):
    return largura / altura

def calcular_size(imagem: pygame.Surface, size: tuple[int,int]):
    largura, altura = size
    largura_original, altura_original = imagem.get_size()
    if largura == 'auto':
        largura = altura * largura_original / altura_original
    elif altura == 'auto':
        altura = largura / largura_original / altura_original
    return largura, altura


def carregar_imagem(*path, size: tuple[int,int] | None = None):
    try:
        imagem = pygame.image.load(os.path.join(*path))
    except:
        print(*path)
        raise TypeError(f'Erro ao carregar imagem {path}')
    
    if size is not None:
        size = calcular_size(imagem, size)
        imagem = pygame.transform.scale(imagem, size)
    return imagem

def mudar_tamanho(img: pygame.Surface, size: tuple[int,int]):
    return pygame.transform.scale(img, calcular_size(img, size))