#ifndef CORRELACAO
    #define CORRELACAO

    #include <opencv2/opencv.hpp>

    using namespace cv;

    Mat aplicar_correlacao(const Mat &imagem_entrada, const Mat &mascara);

    Mat gerar_mascara_media(const int dimensao);

#endif