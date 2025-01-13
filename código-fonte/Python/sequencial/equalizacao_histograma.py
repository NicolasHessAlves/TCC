import numpy as np

VALOR_MAXIMO_HISTOGRAMA : int = 255

def aplicar_equalizacao_histograma(imagem_entrada : np.ndarray) -> np.ndarray:
    histograma = np.zeros((VALOR_MAXIMO_HISTOGRAMA + 1), dtype=int)
    
    imagem_1D = imagem_entrada.ravel() 
    for pixel in imagem_1D:
        histograma[pixel] += 1
    
    total_pixels : int = imagem_entrada.size
    
    histograma_acumulado = np.cumsum(histograma)
    histograma_acumulado_normalizado = histograma_acumulado / total_pixels  

    transformacao_intensidade = (histograma_acumulado_normalizado * VALOR_MAXIMO_HISTOGRAMA).astype(np.uint8)
    
    return transformacao_intensidade[imagem_entrada]
