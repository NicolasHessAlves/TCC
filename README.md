# README - TCC

## Descrição
Este repositório contém os códigos, imagens de entrada e os resultados obtidos na execução de algoritmos de Processamento Digital de Imagens (PDI). Os algoritmos implementados neste projeto são os seguintes:
- **Limiarização**
- **Equalização de Histograma**
- **Correlação Espacial (Filtro da Média)**

As implementações foram realizadas em duas linguagens de programação, tanto em versões sequenciais quanto paralelas:
- **C++** 
- **Python** 

## Compilação e Execução

### C++
Foram realizadas duas compilações diferentes para o código em C++:
- **Sem otimização (O0)**
- **Com otimização (O3)**

#### Comando para Compilação:
Na pasta que contém os arquivos `.cpp`, execute:

**Compilação com O0:**
```bash
g++ main.cpp limiarizacao.cpp equalizacao_histograma.cpp correlacao.cpp -o programa_O0 `pkg-config --cflags --libs opencv4`
```

**Compilação com O3:**
```bash
g++ main.cpp limiarizacao.cpp equalizacao_histograma.cpp correlacao.cpp -o programa_O3 -O3 `pkg-config --cflags --libs opencv4`
```

### Python
Para a implementação em Python, não é necessário compilar o código. Basta executar o script diretamente:
```bash
python3 main.py
```

## Arquivo de Configuração
Para rodar os programas, é necessário fornecer um arquivo de configuração `.txt`, que define:
- Quantidade de threads
- Algoritmo a ser executado (L para Limiarização, H para Equalização de Histograma, C para Correlação)
- Número de execuções
- Salvar ou não a imagem processada
- Caminho da imagem de entrada
- Parâmetros específicos do algoritmo


### Modelo do Arquivo de Configuração:
```text
Threads: <quantidade_threads> Modo: <L|H|C> Execuções: <quantidade> Salvar: <Sim|Não>
<caminho_imagem> <parâmetros>
```

### Exemplos:
**Arquivo de Configuração para Limiarização:**
```text
Threads: 1 Modo: L Execuções: 1 Salvar: Sim
/TCC_Dataset/2K_1.png 128
```
**Arquivo de Configuração para Equalização de Histograma:**
```text
Threads: 2 Modo: H Execuções: 1 Salvar: Sim
/TCC_Dataset/2K_2.png 
```

**Arquivo de Configuração para Correlação:**
```text
Threads: 4 Modo: C Execuções: 1 Salvar: Sim
/TCC_Dataset/2K_3.png 15
```

## Execução dos Programas
Execute o programa passando o arquivo de configuração como argumento.

### C++:
**Execução com O0:**
```bash
./programa_O0 <arquivo_configuracao.txt>
```
**Execução com O3:**
```bash
./programa_O3 <arquivo_configuracao.txt>
```

### Python:
```bash
python3 main.py <arquivo_configuracao.txt>
```

## Coleta de Resultados
Para a obtenção dos resultados, cada arquivo de configuração foi definido para uma única execução e as imagens processadas foram salvas. Foram realizadas 5 execuções do programa para cada arquivo de configuração, os tempos de execução e o uso da CPU foram registrados nos logs.

Para medir o tempo e o uso de CPU, foi utilizado o comando `time` do Linux.

Exemplo de saída:
```text
Execução 1:
Tempo: 9.630s
CPU: 99%

Execução 2:
Tempo: 9.626s
CPU: 99%

Execução 3:
Tempo: 9.623s
CPU: 99%

Execução 4:
Tempo: 9.632s
CPU: 99%

Execução 5:
Tempo: 9.634s
CPU: 99%
```



