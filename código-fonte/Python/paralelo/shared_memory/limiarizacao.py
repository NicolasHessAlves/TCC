from multiprocessing import Process
from memoria_compartilhada import *
import numpy as np

VALOR_MAXIMO_LIMIARIZACAO : int = 255

def __processar_linhas(altura : int, largura : int, slicing, k : int):
    shm_entrada, imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura, largura)
    shm_saida, imagem_saida = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_SAIDA, altura, largura)
    
    imagem_saida[slicing, :] = np.where(imagem_entrada[slicing, :] < k, 0, VALOR_MAXIMO_LIMIARIZACAO).astype(np.uint8)
    
    shm_entrada.close()
    shm_saida.close()

def aplicar_limiarizacao(shm_entrada, imagem_entrada : np.ndarray, k : int, num_processo : int):
    altura, largura = imagem_entrada.shape
    
    shm_saida, imagem_saida = criar_imagem_saida(altura, largura)
    
    linhas_por_processo : int = int(altura / num_processo)

    processos = [Process(target=__processar_linhas,
                         args=(altura,
                               largura,
                               slice(p * linhas_por_processo, altura if (p == num_processo - 1) else (p + 1) * linhas_por_processo),
                               k)) for p in range(num_processo)]
    
    for p in processos:
        p.start()
        
    for p in processos:
        p.join()
        
    shm_entrada.close()
    shm_entrada.unlink()
    
    return shm_saida, imagem_saida    