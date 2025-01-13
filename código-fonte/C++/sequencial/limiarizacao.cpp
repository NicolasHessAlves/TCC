#include <opencv2/opencv.hpp>
#include "limiarizacao.hpp"

using namespace cv;

Mat aplicar_limiarizacao(const Mat &imagem_entrada, const uchar k) {
    const int altura = imagem_entrada.rows;
    const int largura = imagem_entrada.cols;

    Mat imagem_saida = Mat::zeros(altura, largura, CV_8UC1); // 8 bits uchar 1 banda

    for (int i = 0; i < altura; i++)
        for (int j = 0; j < largura; j++)
            imagem_saida.at<uchar>(i, j) = (imagem_entrada.at<uchar>(i, j) >= k) ? (uchar)VALOR_MAXIMO_LIMIARIZACAO : (uchar)0;

    return imagem_saida;    
}