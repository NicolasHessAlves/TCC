#include <opencv2/opencv.hpp>
#include <thread>
#include "correlacao.hpp"

using namespace std;
using namespace cv;

void correlacao_parcial(const Mat &imagem_entrada, const Mat &mascara, Mat &imagem_saida, 
                        const int inicio, const int fim) {
    const int altura_imagem = imagem_entrada.rows;
    const int largura_imagem = imagem_entrada.cols;

    const int altura_mascara = mascara.rows;
    const int largura_mascara = mascara.cols;

    const int centro_altura = altura_mascara / 2;
    const int centro_largura = largura_mascara / 2;

    for (int i = inicio; i < fim; i++) {
        for (int j = 0; j < largura_imagem; j++) {
            float soma = 0;

            for (int m = 0; m < altura_mascara; m++) {
                for (int n = 0; n < largura_mascara; n++) {
                    int y = i - centro_altura + m;
                    int x = j - centro_largura + n;

                    if ((0 <= y && y < altura_imagem) && (0 <= x && x < largura_imagem)) {
                        soma += imagem_entrada.at<uchar>(y, x) * mascara.at<float>(m, n);
                    }
                }
            }
            imagem_saida.at<uchar>(i, j) = (uchar) soma;
        }
    }
}

Mat aplicar_correlacao(const Mat &imagem_entrada, const Mat &mascara, const int num_threads) {
    const int altura_imagem = imagem_entrada.rows;
    const int largura_imagem = imagem_entrada.cols;

    const int linhas_por_thread = altura_imagem / num_threads;
    thread threads[num_threads];

    Mat imagem_saida = Mat::zeros(altura_imagem, largura_imagem, CV_8UC1); // 8 bits uchar 1 banda

     // Calcular o histograma da imagem
    for (int t = 0; t < num_threads; t++) {
        int inicio = t * linhas_por_thread;
        int fim = (t == num_threads - 1) ? altura_imagem : (t + 1) * linhas_por_thread; // A última thread processa o restante
        threads[t] = thread(correlacao_parcial, ref(imagem_entrada), ref(mascara), ref(imagem_saida), inicio, fim);
    }

    for (int t = 0; t < num_threads; t++) 
        threads[t].join();
    
    return imagem_saida;
}

Mat gerar_mascara_media(const int dimensao) {
    Mat mascara = Mat::zeros(dimensao, dimensao, CV_32F); 

    const float media = 1/(float)(dimensao * dimensao);

    for (int i = 0; i < dimensao; i++)
        for (int j = 0; j < dimensao; j++)
            mascara.at<float>(i, j) = media;

    return mascara; 
}