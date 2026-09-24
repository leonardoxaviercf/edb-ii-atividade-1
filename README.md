# Análise Empírica de Algoritmos: Hashing Consistente vs. Round-Robin

Este repositório contém a implementação e a análise empírica de dois algoritmos de distribuição de carga (*load balancing*) em servidores web:

* **Hashing Consistente (*Consistent Hashing*)**
* **Round-Robin (Rodízio Circular)**

O objetivo do experimento é investigar, empiricamente, como o tempo de roteamento varia conforme o número de servidores do cluster e comparar esse comportamento com a análise assintótica das implementações utilizadas.

Além do tempo de execução, o experimento avalia a **taxa de realocação de requisições** após a remoção de um servidor, buscando analisar a estabilidade da distribuição de carga diante de uma alteração na composição do cluster.

> **Observação:** o experimento utiliza uma implementação simplificada de Hashing Consistente inspirada nos princípios apresentados por Karger et al. (1997). Portanto, os resultados não constituem uma reprodução integral do protocolo de caching descrito no artigo.

O projeto foi desenvolvido como parte das atividades da disciplina de **Estruturas de Dados Básicas II**, do **Instituto Metrópole Digital (IMD/UFRN)**.

---

## Algoritmos analisados

### Hashing Consistente

A implementação representa os servidores em um anel lógico (*hash ring*), utilizando **20 réplicas virtuais por servidor**.

As requisições são convertidas em valores de hash utilizando MD5 e, posteriormente, uma **busca binária** é realizada sobre os pontos ordenados do anel para determinar o servidor responsável pela requisição.

Para a implementação utilizada neste experimento, o custo da consulta é:

$$
O(\log n)
$$

onde `n` representa o número de servidores do cluster.

### Round-Robin

O Round-Robin distribui as requisições sequencialmente entre os servidores disponíveis, utilizando um índice circular.

A operação de obtenção do próximo servidor utiliza acesso direto à lista e atualização do índice, apresentando custo:

$$
O(1)
$$

em relação ao número de servidores.

---

## Metodologia

O experimento considera diferentes tamanhos de cluster:

```text
100
1.000
5.000
10.000
30.000
50.000
```

Para cada configuração são processadas **10.000 requisições**.

O tempo de execução é medido utilizando `time.perf_counter()`, considerando apenas a etapa de roteamento das requisições, sem incluir a construção inicial das estruturas dos algoritmos.

Os resultados são obtidos por meio de múltiplas execuções para cada tamanho de entrada e posteriormente é calculada a média dos tempos observados.

### Experimento de estabilidade

Para avaliar a estabilidade da distribuição, um servidor localizado no centro da lista de servidores é removido do cluster.

Antes e depois da remoção, as requisições são roteadas e seus servidores de destino são comparados. A taxa de realocação corresponde à proporção de requisições cujo servidor de destino foi alterado após a remoção.

Essa análise permite observar empiricamente a diferença de comportamento entre uma distribuição sequencial e uma distribuição baseada em hashing consistente diante de uma alteração na composição do cluster.

---

## Estrutura do repositório

```text
.
├── benchmark_algoritmos.py
├── plotar_graficos.py
├── resultados_tempo.csv
├── resultados_realocacao.csv
├── grafico_tempo.png
├── grafico_realocacao.png
└── README.md
```

### `benchmark_algoritmos.py`

Responsável pela execução dos experimentos.

O arquivo:

* implementa o Hashing Consistente;
* implementa o Round-Robin;
* gera os diferentes tamanhos de cluster;
* processa as requisições;
* mede os tempos de execução;
* calcula as taxas de realocação;
* exporta os resultados para arquivos CSV.

### `plotar_graficos.py`

Responsável pela visualização dos resultados experimentais.

O script lê os arquivos CSV e gera os gráficos utilizados na análise, permitindo comparar os resultados observados com as tendências teóricas de crescimento assintótico.

### `resultados_tempo.csv`

Contém os tempos médios de execução obtidos para cada tamanho de cluster.

### `resultados_realocacao.csv`

Contém as taxas de realocação observadas após a remoção de um servidor.

### `grafico_tempo.png`

Representa graficamente a relação entre o número de servidores e o tempo de execução dos algoritmos.

### `grafico_realocacao.png`

Representa a taxa de realocação observada após a remoção de um servidor.

---

## Requisitos

O experimento requer:

* **Python 3**
* `NumPy`
* `Pandas`
* `Matplotlib`

Recomenda-se a utilização de um ambiente virtual.

### Instalação

```bash
pip install numpy pandas matplotlib
```

---

## Execução

### 1. Executar os benchmarks

Execute:

```bash
python benchmark_algoritmos.py
```

Esse comando executará as baterias de testes e produzirá:

```text
resultados_tempo.csv
resultados_realocacao.csv
```

### 2. Gerar os gráficos

Após a conclusão do benchmark, execute:

```bash
python plotar_graficos.py
```

Os gráficos serão gerados no diretório do projeto:

```text
grafico_tempo.png
grafico_realocacao.png
```

---

## Reprodutibilidade

Para reproduzir os resultados, execute os scripts na ordem apresentada acima.

O experimento utiliza uma quantidade fixa de **10.000 requisições** e avalia os seguintes tamanhos de cluster:

```text
n = {100, 1000, 5000, 10000, 30000, 50000}
```

Os resultados podem variar ligeiramente entre execuções devido às características do ambiente de execução, do sistema operacional e da máquina utilizada para realizar as medições.

A análise de complexidade deve ser interpretada em conjunto com essas limitações: a notação Big-O descreve o comportamento assintótico de crescimento, enquanto os tempos medidos representam o desempenho da implementação em um ambiente específico.

---

## Referência principal

A implementação do Hashing Consistente foi desenvolvida com base nos princípios apresentados em:

> KARGER, D. et al. **Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web.** Proceedings of the 29th Annual ACM Symposium on Theory of Computing (STOC), 1997.

O trabalho original apresenta os fundamentos do Hashing Consistente e suas propriedades relacionadas à distribuição e à estabilidade das atribuições quando a composição dos servidores é modificada.

O experimento deste repositório constitui uma **adaptação simplificada desses princípios para um cenário de distribuição de requisições**, permitindo a comparação experimental com o algoritmo Round-Robin.

--- 

## Relatório Final

Para uma análise detalhada da pesquisa, acesse o [Relatório Final em PDF](./EDB2_ Análise Empírica - Hashing Consistente vs Round-Robin.pdf).
