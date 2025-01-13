#ifndef LIMIARIZACAO
    #define LIMIARIZACAO

    #include <opencv2/opencv.hpp>

    #define VALOR_MAXIMO_LIMIARIZACAO 255

    using namespace cv;

    Mat aplicar_limiarizacao(const Mat &imagem_entrada, const uchar k);

#endif