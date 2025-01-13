from enum import Enum
from multiprocessing import shared_memory
import cv2
import numpy as np

__NOME_IMAGEM_SAIDA = "imagem_saida"
__NOME_IMAGEM_ENTRADA = "imagem_entrada"

class MemoriaCompartilhada(Enum):
    IMAGEM_ENTRADA = 0
    IMAGEM_SAIDA = 1

def ler_imagem_entrada(caminho_imagem : str):
    imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
    shm_entrada = shared_memory.SharedMemory(create=True, name=__NOME_IMAGEM_ENTRADA, size=imagem.nbytes)
    imagem_entrada = np.ndarray(imagem.shape, dtype=np.uint8, buffer=shm_entrada.buf)
    imagem_entrada[:] = imagem[:]
    return shm_entrada, imagem_entrada

def criar_imagem_saida(altura, largura):
    shm_saida = shared_memory.SharedMemory(create=True, name=__NOME_IMAGEM_SAIDA, size=altura*largura)
    return shm_saida, np.ndarray((altura, largura), dtype=np.uint8, buffer=shm_saida.buf)

def get_memoria_compartilhada(mem : MemoriaCompartilhada, altura, largura):
    if mem == MemoriaCompartilhada.IMAGEM_ENTRADA:
        shm_entrada = shared_memory.SharedMemory(name=__NOME_IMAGEM_ENTRADA)
        return shm_entrada, np.ndarray((altura, largura), dtype=np.uint8, buffer=shm_entrada.buf)
    elif mem == MemoriaCompartilhada.IMAGEM_SAIDA:
        shm_saida = shared_memory.SharedMemory(name=__NOME_IMAGEM_SAIDA)
        return shm_saida, np.ndarray((altura, largura), dtype=np.uint8, buffer=shm_saida.buf)
    else:
        raise MemoryError("Erro na memória compartilhada.")