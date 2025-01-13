#ifndef CORRELACAO
    #define CORRELACAO

    #include <opencv2/opencv.hpp>

    using namespace cv;

    Mat aplicar_correlacao(const Mat &imagem_entrada, const Mat &mascara, const int num_threads);

    Mat gerar_mascara_media(int const dimensao);

#endif