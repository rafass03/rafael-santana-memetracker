# Memetracker

Este repositório contém o código fonte e as análises de uma rede complexa extraída a partir de um grande conjunto de dados de citações. Esse códigos foram utilizados como base do relatório.

### Aluno: Rafael Silva Santana
### SNAP: [96 million memes from Memetracker](https://snap.stanford.edu/data/memetracker9.html)


## Estrutura do Projeto

- **`src/`**: Contém os scripts Python originais com a lógica da aplicação.
- **`notebooks/`**: Contém a execução do projeto em formato Jupyter Notebook. Ideal para visualizar o passo a passo, a documentação (Markdown) e os gráficos gerados de forma interativa.
- **`data/`**: Contém o grafo extraído e tratado (`edges_2days.zip`), ou seja, a parte 1 do Script ou Jupyter feito. Contudo, você pode baixar o arquivo bruto na pagina do SNAP e extrair na pasta `data/` e excecutar normalmente os Notebooks e Scripts.

## Como Executar

### 1. Pré-requisitos
1. Certifique-se de ter o Python 3 instalado. Além disso, é altamente recomendável o uso de um ambiente virtual.
2. Para baixar os pacotes necessários, instale as bibliotecas padrão de ciência de dados:
```bash
pip install pandas networkx matplotlib scipy numpy jupyter
```
3. Sobre os dados:
- O arquivo original bruto e extraído (`quotes_2008-08.txt.gz` e `quotes_2008-08.txt`) tem 4GB e 1,1GB, consequentemente não podem ser incluídos no repositório devido ao seu tamanho. A filtragem desse dado bruto (redução para uma janela de 2 dias visando otimizar) foi o cálculo de determinação do grafo utilizado neste trabalho.
- O dado resultante tratado (`edges_2days.csv`) ainda sim possui 188 MB (acima do limite do GitHub). Por conta disso, ele foi zipado antes de subir para o GitHub. Para prosseguir na execução dos códigos, vá até a pasta `data/` e descompacte o arquivo `edges_2days.zip` e depois execute os Notebooks ou Scripts 02 em diante.

### 2. Execução via Jupyter Notebook
A forma mais didática de visualizar as análises é rodando os Notebooks, pois os gráficos e os resultados ficam salvos logo abaixo de cada bloco de código.

1. Na pasta `notebooks/` tem os 4 arquivos Jupyter Notebook, começando por `01_extracao_grafo.ipynb` e terminando em `04_analise_avancada.ipynb`. Eexecute o `01_extracao_grafo.ipynb` se baixou o arquivo bruto na pagina do SNAP e extraiu na pasta `data/`, caso contrário comece do `02_analise_estrutura_grafo.ipynb` se só extraiu o `edges_2days.csv`.
2. Execute os Notebooks na ordem númerica e as células sequencialmente para ver os resultados.

### 3. Execução via Scripts
Há também a possibilidade de rodar os códigos, bastando acessar a pasta `src/`. Certifique-se de que o arquivo de dados `quotes_2008-08.txt` (ou `edges_2days.csv` descompactado) esteja presente na pasta `data/`.

1. Rode os scripts na ordem numérica de `01_extracao_grafo.py` até `04_analise_avancada.py`. Eexecute o `01_extracao_grafo.py` se baixou o arquivo bruto na pagina do SNAP e extraiu na pasta `data/`, caso contrário comece do `02_analise_estrutura_grafo.py` se só extraiu o `edges_2days.csv`.
2. Rode os scripts na ordem numérica.