#ifndef EQUALIZACAO_HISTOGRAMA
    #define EQUALIZACAO_HISTOGRAMA

    #include <opencv2/opencv.hpp>

    #define VALOR_MAXIMO_HISTOGRAMA 255

    using namespace cv;

    Mat aplicar_equalizacao_histograma(const Mat &imagem_entrada);

#endif