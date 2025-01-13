#include <opencv2/opencv.hpp>
#include <thread>
#include <mutex>
#include "equalizacao_histograma.hpp"

using namespace std;
using namespace cv;

void processar_linhas_histograma(const Mat &imagem, const int inicio, const int fim, int (&hist)[(VALOR_MAXIMO_HISTOGRAMA + 1)], mutex &mtx) {
    int hist_local[(VALOR_MAXIMO_HISTOGRAMA + 1)] = {0};  

    for (int i = inicio; i < fim; i++)
        for (int j = 0; j < imagem.cols; j++)
            hist_local[imagem.at<uchar>(i, j)]++;

    // Combinar o histograma local ao global
    mtx.lock();

    for (int i = 0; i < (VALOR_MAXIMO_HISTOGRAMA + 1); ++i) 
        hist[i] += hist_local[i];

    mtx.unlock();
}

void processar_linhas_equalizacao(const Mat &imagem_entrada, Mat &imagem_saida, const int inicio, const int fim, const uchar (&transformacao_intensidade)[(VALOR_MAXIMO_HISTOGRAMA + 1)]) {
    for (int i = inicio; i < fim; i++)
        for (int j = 0; j < imagem_entrada.cols; j++)
            imagem_saida.at<uchar>(i, j) = transformacao_intensidade[imagem_entrada.at<uchar>(i, j)];
}


Mat aplicar_equalizacao_histograma(const Mat &imagem_entrada, const int num_threads){
    const int altura = imagem_entrada.rows;
    const int largura = imagem_entrada.cols;

    int histograma[(VALOR_MAXIMO_HISTOGRAMA + 1)] = {0};    
    mutex mtx_histograma;

    const int linhas_por_thread = altura / num_threads;
    thread threads[num_threads];

    // Calcular o histograma da imagem
    for (int t = 0; t < num_threads; t++) {
        int inicio = t * linhas_por_thread;
        int fim = (t == num_threads - 1) ? altura : (t + 1) * linhas_por_thread; // A última thread processa o restante
        threads[t] = thread(processar_linhas_histograma, ref(imagem_entrada), inicio, fim, ref(histograma), ref(mtx_histograma));
    }

    for (int t = 0; t < num_threads; t++) 
        threads[t].join();  

    /*
    * Calcular o histograma acumulado,
    * o histograma acumulado normalizado e 
    * a transformação de intensidade.
    */

    const int total_pixels = altura * largura;
    int histograma_acumulado = 0;
    float histograma_acumulado_normalizado;
    uchar transformacao_intensidade[(VALOR_MAXIMO_HISTOGRAMA + 1)];

    for (int i = 0; i < (VALOR_MAXIMO_HISTOGRAMA + 1); i++)
    {
        histograma_acumulado += histograma[i];

        histograma_acumulado_normalizado = (float)histograma_acumulado / total_pixels;

        transformacao_intensidade[i] = (uchar)(histograma_acumulado_normalizado * VALOR_MAXIMO_HISTOGRAMA);
    }


    // Aplicar a equalização de histograma na imagem
    Mat imagem_saida = Mat::zeros(altura, largura, CV_8UC1); // 8 bits uchar 1 banda

    for (int t = 0; t < num_threads; t++) {
        int inicio = t * linhas_por_thread;
        int fim = (t == num_threads - 1) ? altura : (t + 1) * linhas_por_thread; // A última thread processa o restante
        threads[t] = thread(processar_linhas_equalizacao, ref(imagem_entrada), ref(imagem_saida), inicio, fim, ref(transformacao_intensidade));
    }

    for (int t = 0; t < num_threads; t++) 
        threads[t].join();  
    
    return imagem_saida;
}