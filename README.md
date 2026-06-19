# Memetracker

Este repositório contém o código fonte e as análises de uma rede complexa extraída a partir de um grande conjunto de dados de citações. Esse códigos foram utilizados como base do relatório.

### Aluno: Rafael Silva Santana
### SNAP: [96 million memes from Memetracker](https://snap.stanford.edu/data/memetracker9.html)


## Estrutura do Projeto

- **`src/`**: Contém os scripts Python originais com a lógica da aplicação.
- **`notebooks/`**: Contém a execução do projeto em formato Jupyter Notebook. Ideal para visualizar o passo a passo, a documentação (Markdown) e os gráficos gerados de forma interativa.
- **`data/`**: Contém o grafo extraído e tratado (`edges_2days.zip`). O arquivo bruto gigante de 4GB (`quotes_2008-08.txt`) é muito grande para o  GitHub.

## Como Executar

### 1. Pré-requisitos
1. Certifique-se de ter o Python 3 instalado. Além disso, é altamente recomendável o uso de um ambiente virtual.
2. Para baixar os pacotes necessários, instale as bibliotecas padrão de ciência de dados:
```bash
pip install pandas networkx matplotlib scipy numpy jupyter
```
3. Sobre os dados:
- 3.1. O arquivo original bruto e extraído (`quotes_2008-08.txt.gz` e `quotes_2008-08.txt`) tem 4GB e 1,1GB, consequentemente não podem ser incluídos no repositório devido ao seu tamanho. A filtragem desse dado bruto (redução para uma janela de 2 dias visando caber na memória RAM) foi o **Cálculo de determinação do grafo** utilizado neste trabalho, detalhado no Notebook 01.
3.2. O dado resultante tratado (`edges_2days.csv`) ainda sim possui 188 MB (acima do limite do GitHub). Por conta disso, ele foi zipado. **Antes de executar os Notebooks, vá até a pasta `data/` e descompacte o arquivo `edges_2days.zip`.**

### 2. Execução via Jupyter Notebook
A forma mais didática de visualizar as análises é rodando os Notebooks, pois os gráficos e os resultados ficam salvos logo abaixo de cada bloco de código.

1. Na pasta `notebooks/` tem os 4 arquivos Jupyter Notebook, começando por `01_extracao_grafo.ipynb` e terminando em `04_analise_avancada.ipynb`.
2. Execute-os sequencialmente para ver os resultados. Além disso, execute as células sequencialmente também.

### 3. Execução via Scripts
Há também a possibilidade de rodar os códigos, bastando acessar a pasta `src/`. Certifique-se de que o arquivo de dados `quotes_2008-08.txt` esteja presente na pasta `data/`. Em seguida, rode os scripts na ordem numérica de `01_extracao_grafo.py` até `04_analise_avancada.py`.