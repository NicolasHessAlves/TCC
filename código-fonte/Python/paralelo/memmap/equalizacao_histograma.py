from memoria_compartilhada import *
from multiprocessing import Process, Lock
import numpy as np

VALOR_MAXIMO_HISTOGRAMA : int = 255

__CAMINHO_ARQUIVO_HISTOGRAMA : str = "/tmp/histograma.dat"

def __processar_linhas_histograma(altura : int, largura : int, slicing, lock):
    imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura, largura)[slicing, :]
    histograma = np.memmap(__CAMINHO_ARQUIVO_HISTOGRAMA, dtype=np.int32, mode='w+', shape=(VALOR_MAXIMO_HISTOGRAMA + 1))
    histograma_local = np.zeros((VALOR_MAXIMO_HISTOGRAMA + 1), dtype=np.int32)
    
    imagem_1D = imagem_entrada.ravel() 
    for pixel in imagem_1D:
        histograma_local[pixel] += 1
        
    with lock:
        histograma += histograma_local
            
def __processar_linhas_equalizacao(altura : int, largura : int, slicing, transformacao_intensidade):
    imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura, largura)
    imagem_saida = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_SAIDA, altura, largura)
    
    imagem_saida[slicing, :] = transformacao_intensidade[imagem_entrada[slicing, :]]
        
def aplicar_equalizacao_histograma(imagem_entrada : np.ndarray, num_processo : int) -> np.ndarray:
    altura, largura = imagem_entrada.shape
    
    histograma = np.memmap(__CAMINHO_ARQUIVO_HISTOGRAMA, dtype=np.int32, mode='w+', shape=(VALOR_MAXIMO_HISTOGRAMA + 1))
    
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

    imagem_saida = imagem_saida = criar_imagem_saida(altura, largura)
    
    total_pixels : int = imagem_entrada.size
    
    histograma_acumulado = np.cumsum(histograma)
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
    
    return imagem_saida
