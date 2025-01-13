from correlacao import *
from equalizacao_histograma import *
from limiarizacao import *
import cv2
import numpy as np
import sys

def main():
    if len(sys.argv) < 2:
        print("Erro: Nome do arquivo não fornecido.", file=sys.stderr)
        print(f"Uso: {sys.argv[0]} <nome_do_arquivo>", file=sys.stderr)
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: Não foi possível abrir o arquivo {nome_arquivo}", file=sys.stderr)
        sys.exit(1)

    primeira_linha = linhas[0].strip().split()
    try:
        threads = int(primeira_linha[1])
        modo = primeira_linha[3]
        quantidade_execucoes = int(primeira_linha[5])
        salvar_imagem = primeira_linha[7]
    except (IndexError, ValueError):
        print("Erro: Configuração inválida na primeira linha.", file=sys.stderr)
        sys.exit(1)

    if modo not in ('L', 'H', 'C'):
        print(f"Erro: Modo inválido '{modo}'. Use 'L', 'H' ou 'C'.", file=sys.stderr)
        sys.exit(1)

    if salvar_imagem not in ('Sim', 'Não'):
        print("Erro: Valor de 'Salvar' inválido. Use 'Sim' ou 'Não'.", file=sys.stderr)
        sys.exit(1)

    salvar = (salvar_imagem == "Sim")
    
    print("Execução sequencial -- Python.")
    
    execucao_atual = 0

    while(execucao_atual < quantidade_execucoes):
        for conteudo_linha in linhas[1:]:
            if execucao_atual >= quantidade_execucoes:
                break

            conteudo_linha = conteudo_linha.strip().split()
            caminho_imagem = conteudo_linha[0]

            imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
            imagem_saida : np.ndarray
            if imagem is None:
                print(f"Erro ao carregar a imagem: {caminho_imagem}", file=sys.stderr)
                continue

            caminho_imagem_saida = caminho_imagem.rsplit('.', 1)[0] + "--out.png"

            if modo == 'L':
                try:
                    valor_limiar = int(conteudo_linha[1])
                except (IndexError, ValueError):
                    print("Erro: Linha mal formatada no modo L.", file=sys.stderr)
                    continue

                imagem_saida = aplicar_limiarizacao(imagem, valor_limiar)

            elif modo == 'H':
                imagem_saida = aplicar_equalizacao_histograma(imagem)

            elif modo == 'C':
                try:
                    tamanho_mascara = int(conteudo_linha[1])
                except (IndexError, ValueError):
                    print("Erro: Linha mal formatada no modo C.", file=sys.stderr)
                    continue

                mascara = gerar_mascara_media(tamanho_mascara)
                imagem_saida = aplicar_correlacao(imagem, mascara)

            if salvar:
                cv2.imwrite(caminho_imagem_saida, imagem_saida)

            execucao_atual += 1

if __name__ == "__main__":
    main()