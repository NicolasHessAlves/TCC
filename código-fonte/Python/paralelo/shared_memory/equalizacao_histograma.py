from memoria_compartilhada import *
from multiprocessing import Process, Lock
import numpy as np

VALOR_MAXIMO_HISTOGRAMA : int = 255

__NOME_HISTOGRAMA : str = "histograma"

def __processar_linhas_histograma(altura : int, largura : int, slicing, lock):
    shm_entrada, imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura, largura)
    imagem_entrada = imagem_entrada[slicing, :]
    shm_hist = shared_memory.SharedMemory(name=__NOME_HISTOGRAMA)
    histograma = np.ndarray((VALOR_MAXIMO_HISTOGRAMA + 1), dtype=np.int32, buffer=shm_hist.buf)
    histograma_local = np.zeros((VALOR_MAXIMO_HISTOGRAMA + 1), dtype=np.int32)
    
    imagem_1D = imagem_entrada.ravel() 
    for pixel in imagem_1D:
        histograma_local[pixel] += 1
        
    with lock:
        histograma += histograma_local
    
    shm_entrada.close()
    shm_hist.close()

            
def __processar_linhas_equalizacao(altura : int, largura : int, slicing, transformacao_intensidade):
    shm_entrada, imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura, largura)
    shm_saida, imagem_saida = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_SAIDA, altura, largura)
    
    imagem_saida[slicing, :] = transformacao_intensidade[imagem_entrada[slicing, :]]
    
    shm_entrada.close()
    shm_saida.close()
        
def aplicar_equalizacao_histograma(shm_entrada, imagem_entrada : np.ndarray, num_processo : int):
    altura, largura = imagem_entrada.shape
    
    shm_hist = shared_memory.SharedMemory(create=True, name=__NOME_HISTOGRAMA, size=(VALOR_MAXIMO_HISTOGRAMA + 1) * np.dtype(np.int32).itemsize)
    
    histograma = np.ndarray((VALOR_MAXIMO_HISTOGRAMA + 1), dtype=np.int32, buffer=shm_hist.buf)
    
    linhas_por_processo : int = int(altura / num_processo)
    lock = Lock()

    processos = [Process(target=__processar_linhas_histograma,
                         args=(altura,
                               largura,
                               slice(p * linhas_por_processo, altura if (p == num_processo - 1) else (p + 1) * linhas_por_processo),
                               lock)) for p in range(num_processo)]
    
    for p in processos:
        p.start()
        
    for p in processos:
        p.join()

    shm_saida, imagem_saida = criar_imagem_saida(altura, largura)
    
    total_pixels : int = imagem_entrada.size
    
    histograma_acumulado = np.cumsum(histograma)
    
    shm_hist.close()
    shm_hist.unlink()
    
    histograma_acumulado_normalizado = histograma_acumulado / total_pixels  

    transformacao_intensidade = (histograma_acumulado_normalizado * VALOR_MAXIMO_HISTOGRAMA).astype(np.uint8)
    
    processos = [Process(target=__processar_linhas_equalizacao,
                         args=(altura,
                               largura,
                               slice(p * linhas_por_processo, altura if (p == num_processo - 1) else (p + 1) * linhas_por_processo),
                               transformacao_intensidade)) for p in range(num_processo)]
    
    for p in processos:
        p.start()
        
    for p in processos:
        p.join()
        
    shm_entrada.close()
    shm_entrada.unlink()
    
    return shm_saida, imagem_saida
