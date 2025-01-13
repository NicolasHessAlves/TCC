import numpy as np

def aplicar_correlacao(imagem_entrada : np.ndarray, mascara : np.ndarray) -> np.ndarray:
    altura_imagem, largura_imagem = imagem_entrada.shape
    altura_mascara, largura_mascara = mascara.shape

    centro_largura = largura_mascara // 2
    centro_altura = altura_mascara // 2
    
    altura_mascara_par = (altura_mascara % 2 == 0)
    largura_mascara_par = (largura_mascara % 2 == 0)

    imagem_saida = np.zeros((altura_imagem, largura_imagem), dtype=np.uint8)

    for i in range(altura_imagem):
        for j in range(largura_imagem):
            regiao = imagem_entrada[max(0, i-centro_altura):min(altura_imagem, i+centro_altura if altura_mascara_par else i+centro_altura+1),
                        max(0, j-centro_largura):min(largura_imagem, j+centro_largura if largura_mascara_par else j+centro_largura+1)]
            
            imagem_saida[i, j] = np.sum(regiao * mascara[max(0, centro_altura - i):min(altura_mascara, altura_imagem - (i - centro_altura)),
                                        max(0, centro_largura - j):min(largura_mascara, largura_imagem - (j - centro_largura))]).astype(np.uint8)
    
    return imagem_saida

def gerar_mascara_media(dimensao : int):
    mascara = np.zeros((dimensao, dimensao), dtype=np.float32)
    
    media : float = 1 / float(dimensao * dimensao)
    
    mascara[:,:] = media
    
    return mascara