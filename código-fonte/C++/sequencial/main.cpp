#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include "limiarizacao.hpp"
#include "equalizacao_histograma.hpp"
#include "correlacao.hpp"

using namespace std;

int main(int argumentos_contagem, char *argumentos_valores[])
{
    // Verifica se o nome do arquivo foi passado
    if (argumentos_contagem < 2)
    {
        cerr << "Erro: Nome do arquivo não fornecido.\n";
        cerr << "Uso: " << argumentos_valores[0] << " <nome_do_arquivo>\n";
        return 1;
    }

    // Nome do arquivo passado por linha de comando
    string nome_arquivo = argumentos_valores[1];

    // Abre o arquivo para leitura
    ifstream arquivo(nome_arquivo);
    if (!arquivo.is_open())
    {
        cerr << "Erro: Não foi possível abrir o arquivo " << nome_arquivo << "\n";
        return 1;
    }

    // Lê a primeira linha (modo e quantidade de execuções)
    string primeira_linha;
    getline(arquivo, primeira_linha);
    istringstream fluxo_primeira_linha(primeira_linha);

    int threads = 0;
    char modo;
    int quantidade_execucoes = 0;
    string salvar_imagem;
    bool salvar = false;

    // Parse da linha
    string temp;

    fluxo_primeira_linha >> temp >> threads; // Threads
    if (temp != "Threads:") {
        cerr << "Erro: Número configuração inválida.\n";
        return 1;
    }

    fluxo_primeira_linha >> temp >> modo; // Modo
    if (temp != "Modo:" || (modo != 'L' && modo != 'H' && modo != 'C')) {
        cerr << "Erro: Modo inválido '" << modo << "'. Use 'L', 'H' ou 'C'.\n";
        return 1;
    }

    fluxo_primeira_linha >> temp >> quantidade_execucoes; // Execuções
    if (temp != "Execuções:" || quantidade_execucoes <= 0) {
        cerr << "Erro: A quantidade de execuções deve ser maior que zero.\n";
        return 1;
    }

    fluxo_primeira_linha >> temp >> salvar_imagem; // Salvar
    if (temp != "Salvar:" || (salvar_imagem != "Sim" && salvar_imagem != "Não")) {
        cerr << "Erro: Valor de 'Salvar' inválido. Use 'Sim' ou 'Não'.\n";
        return 1;
    }

    // Definir o valor de salvar
    salvar = (salvar_imagem == "Sim");

    cout << "Execução sequencial -- C++." << endl;

    // Itera sobre as linhas restantes do arquivo
    string linha;
    vector<string> linhas; // Para armazenamento e reutilização por execuções
    while (getline(arquivo, linha))
    {
        linhas.push_back(linha);
    }

    arquivo.close();

    int execucao_atual = 0;
    // Executa as ações conforme o modo e quantidade de execuções
    for (const string &conteudo_linha : linhas)
    {
        while (execucao_atual < quantidade_execucoes)
        {
            istringstream fluxo_linha(conteudo_linha);

            string caminho_imagem;
            fluxo_linha >> caminho_imagem;

            cv::Mat imagem = cv::imread(caminho_imagem, cv::IMREAD_GRAYSCALE);
            cv::Mat imagem_saida;

            // Verifica se a imagem foi carregada com sucesso
            if (imagem.empty())
            {
                cerr << "Erro ao carregar a imagem!" << std::endl;
                return -1;
            }

            string caminho_imagem_saida = caminho_imagem.substr(0, caminho_imagem.size() - 4) + "--out.png";

            switch (modo)
            {
            case 'L':
            {
                int valor_limiar;
                fluxo_linha >> valor_limiar;
                if (fluxo_linha.fail())
                {
                    cerr << "Erro: Linha mal formatada no modo L.\n";
                    continue;
                }
                imagem_saida = aplicar_limiarizacao(imagem, (uchar)valor_limiar);
                break;
            }
            case 'H':
            {
                imagem_saida = aplicar_equalizacao_histograma(imagem);
                break;
            }
            case 'C':
            {
                int tamanho_mascara;
                fluxo_linha >> tamanho_mascara;
                if (fluxo_linha.fail())
                {
                    cerr << "Erro: Linha mal formatada no modo C.\n";
                    continue;
                }
                cv::Mat mascara = gerar_mascara_media(tamanho_mascara);
                imagem_saida = aplicar_correlacao(imagem, mascara);
                break;
            }
            }

            if (salvar)
                cv::imwrite(caminho_imagem_saida, imagem_saida);

            execucao_atual++;
        }
    }

    return 0;
}
