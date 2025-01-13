from enum import Enum
import cv2
import numpy as np

__CAMINHO_ARQUIVO_IMAGEM_SAIDA = "/tmp/imagem_saida.dat"
__CAMINHO_ARQUIVO_IMAGEM_ENTRADA = "/tmp/imagem_entrada.dat"

class MemoriaCompartilhada(Enum):
    IMAGEM_ENTRADA = 0
    IMAGEM_SAIDA = 1

def ler_imagem_entrada(caminho_imagem : str):
    imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
    imagem_entrada = np.memmap(__CAMINHO_ARQUIVO_IMAGEM_ENTRADA, dtype=np.uint8, mode='w+', shape=imagem.shape)
    imagem_entrada[:] = imagem[:]
    return imagem_entrada

def criar_imagem_saida(altura, largura):
    return np.memmap(__CAMINHO_ARQUIVO_IMAGEM_SAIDA, dtype=np.uint8, mode='w+', shape=(altura, largura))

def get_memoria_compartilhada(mem : MemoriaCompartilhada, altura, largura):
    if mem == MemoriaCompartilhada.IMAGEM_ENTRADA:
        return np.memmap(__CAMINHO_ARQUIVO_IMAGEM_ENTRADA, dtype=np.uint8, mode='r+', shape=(altura, largura))
    elif mem == MemoriaCompartilhada.IMAGEM_SAIDA:
        return np.memmap(__CAMINHO_ARQUIVO_IMAGEM_SAIDA, dtype=np.uint8, mode='r+', shape=(altura, largura))
    else:
        raise MemoryError("Erro na memória compartilhada.")