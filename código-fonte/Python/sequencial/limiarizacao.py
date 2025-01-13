import numpy as np

VALOR_MAXIMO_LIMIARIZACAO : int = 255

def aplicar_limiarizacao(imagem_entrada : np.ndarray, k : int) -> np.ndarray:
    return np.where(imagem_entrada < k, 0, VALOR_MAXIMO_LIMIARIZACAO).astype(np.uint8)
    
    
    
    