#include <thread>
#include <opencv2/opencv.hpp>
#include "limiarizacao.hpp"

using namespace cv;
using namespace std;

void processar_linhas(const Mat &imagem_entrada, Mat &imagem_saida, const int inicio, const int fim, const uchar k) {
    const int largura = imagem_entrada.cols;
    
    for (int i = inicio; i < fim; i++) 
        for (int j = 0; j < largura; j++) 
            imagem_saida.at<uchar>(i, j) = (imagem_entrada.at<uchar>(i, j) >= k) ? (uchar)VALOR_MAXIMO_LIMIARIZACAO : (uchar)0;
}

Mat aplicar_limiarizacao(const Mat &imagem_entrada, const uchar k, const int num_threads) {
    const int altura = imagem_entrada.rows;
    const int largura = imagem_entrada.cols;

    // Criar imagem de saída
    Mat imagem_saida = Mat::zeros(altura, largura, CV_8UC1); // 8 bits uchar 1 banda

    // Definir o número de threads e a divisão do trabalho
    const int linhas_por_thread = altura / num_threads;
    thread threads[num_threads];

    // Criar as threads
    for (int t = 0; t < num_threads; t++) {
        int inicio = t * linhas_por_thread;
        int fim = (t == num_threads - 1) ? altura : (t + 1) * linhas_por_thread; // A última thread processa o restante
        threads[t] = thread(processar_linhas, ref(imagem_entrada), ref(imagem_saida), inicio, fim, k);
    }

    // Esperar todas as threads terminarem
    for (int t = 0; t < num_threads; t++) 
        threads[t].join();  

    return imagem_saida;
}