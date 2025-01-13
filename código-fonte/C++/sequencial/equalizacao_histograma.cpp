#include <opencv2/opencv.hpp>
#include "equalizacao_histograma.hpp"

using namespace cv;


Mat aplicar_equalizacao_histograma(const Mat &imagem_entrada){
    
    // Calcular o histograma da imagem
    const int altura = imagem_entrada.rows;
    const int largura = imagem_entrada.cols;
    int histograma[(VALOR_MAXIMO_HISTOGRAMA + 1)] = {0};    

    
    for (int i = 0; i < altura; i++)
        for (int j = 0; j < largura; j++)
            histograma[imagem_entrada.at<uchar>(i, j)]++;

    /*
    * Calcular o histograma acumulado,
    * o histograma acumulado normalizado e 
    * a transformação de intensidade.
    */

    const int total_pixels = altura * largura;
    int histograma_acumulado = 0;
    float histograma_acumulado_normalizado;
    uchar transformacao_intensidade[(VALOR_MAXIMO_HISTOGRAMA + 1)];

    for (int i = 0; i <= VALOR_MAXIMO_HISTOGRAMA; i++)
    {
        histograma_acumulado += histograma[i];

        histograma_acumulado_normalizado = (float)histograma_acumulado / total_pixels;

        transformacao_intensidade[i] = (uchar)(histograma_acumulado_normalizado * VALOR_MAXIMO_HISTOGRAMA);
    }


    // Aplicar a equalização de histograma na imagem
    Mat imagem_saida = Mat::zeros(altura, largura, CV_8UC1); // 8 bits uchar 1 banda

    for (int i = 0; i < altura; i++)
        for (int j = 0; j < largura; j++)
            imagem_saida.at<uchar>(i, j) = transformacao_intensidade[imagem_entrada.at<uchar>(i, j)];
    
    return imagem_saida;
}