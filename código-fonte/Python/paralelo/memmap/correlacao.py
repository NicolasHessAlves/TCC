from multiprocessing import Process
from memoria_compartilhada import *
import numpy as np

def __aplicar_correlacao_parcial(altura_imagem : int, largura_imagem : int, inicio : int, fim : int, mascara):
    imagem_entrada = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_ENTRADA, altura_imagem, largura_imagem)
    imagem_saida = get_memoria_compartilhada(MemoriaCompartilhada.IMAGEM_SAIDA, altura_imagem, largura_imagem)
    
    altura_mascara, largura_mascara = mascara.shape
    
    centro_largura = largura_mascara // 2
    centro_altura = altura_mascara // 2
    
    altura_mascara_par = (altura_mascara % 2 == 0)
    largura_mascara_par = (largura_mascara % 2 == 0)
    
    for i in range(inicio, fim):
        for j in range(largura_imagem):
            regiao = imagem_entrada[max(0, i-centro_altura):min(altura_imagem, i+centro_altura if altura_mascara_par else i+centro_altura+1),
                        max(0, j-centro_largura):min(largura_imagem, j+centro_largura if largura_mascara_par else j+centro_largura+1)]
            
            imagem_saida[i, j] = np.sum(regiao * mascara[max(0, centro_altura - i):min(altura_mascara, altura_imagem - (i - centro_altura)),
                                        max(0, centro_largura - j):min(largura_mascara, largura_imagem - (j - centro_largura))]).astype(np.uint8)    

def aplicar_correlacao(imagem_entrada : np.ndarray, mascara : np.ndarray, num_processo : int) -> np.ndarray:
    altura_imagem, largura_imagem = imagem_entrada.shape
    
    imagem_saida = criar_imagem_saida(altura_imagem, largura_imagem)

    linhas_por_processo : int = int(altura_imagem / num_processo)
    
    processos = [Process(target=__aplicar_correlacao_parcial,
                         args=(altura_imagem,
                               largura_imagem,
                               p * linhas_por_processo,
                               altura_imagem if (p == num_processo - 1) else (p + 1) * linhas_por_processo,
                               mascara)) for p in range(num_processo)]
    
    for p in processos:
        p.start()
        
    for p in processos:
        p.join()
        
    return imagem_saida

def gerar_mascara_media(dimensao : int):
    mascara = np.zeros((dimensao, dimensao), dtype=np.float32)
    
    media : float = 1 / float(dimensao * dimensao)
    
    mascara[:,:] = media
    
    return mascara