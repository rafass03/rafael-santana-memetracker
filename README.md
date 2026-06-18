# Análise de Redes

Este repositório contém o código fonte e as análises de uma rede complexa extraída a partir de um grande conjunto de dados de citações.

## Estrutura do Projeto

- **`src/`**: Contém os scripts Python originais com a lógica da aplicação.
- **`notebooks/`**: Contém a execução do projeto em formato Jupyter Notebook. Ideal para visualizar o passo a passo, a documentação (Markdown) e os gráficos gerados de forma interativa.
- **`data/`**: Contém o grafo extraído e tratado (`edges_2days.zip`). O arquivo bruto gigante de 4GB (`quotes_2008-08.txt`) é ignorado pelo Git.

## Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python 3 instalado. É recomendável o uso de um ambiente virtual.
Para baixar os pacotes necessários, instale as bibliotecas padrão de ciência de dados:

```bash
pip install pandas networkx matplotlib scipy numpy jupyter
```

> [!WARNING]
> **Onde estão os dados?** 
> 1. O arquivo original bruto (`quotes_2008-08.txt`) tem 4 GB e não pôde ser incluído no repositório devido ao seu tamanho massivo. A filtragem desse dado bruto (redução para uma janela de 2 dias visando caber na memória RAM) foi o **Cálculo de determinação do grafo** utilizado neste trabalho, detalhado no Notebook 01.
> 2. O dado resultante tratado (`edges_2days.csv`) ainda sim possui 188 MB (acima do limite do GitHub). Por conta disso, ele foi zipado. **Antes de executar os Notebooks, vá até a pasta `data/` e descompacte o arquivo `edges_2days.zip`.**

### 2. Execução via Jupyter Notebook (Recomendado)
A forma mais didática de visualizar as análises é rodando os Notebooks, pois os gráficos e os resultados ficam salvos logo abaixo de cada bloco de código.

1. No terminal, na raiz do projeto, digite:
```bash
jupyter notebook
```
2. O seu navegador irá abrir. Navegue até a pasta `notebooks/` e abra o arquivo `01_extracao_grafo.ipynb`.
3. Execute as células sequencialmente.

### 3. Execução via Terminal (Modo Script)
Caso prefira rodar os códigos originais de uma vez só no terminal para gerar as saídas e arquivos finais:

Certifique-se de que o arquivo de dados `quotes_2008-08.txt` esteja presente na raiz do projeto. Em seguida, rode os scripts na ordem numérica:

```bash
# 1. Extração da rede para os dias desejados
python src/01_extracao_grafo.py

# 2. Análise básica das propriedades do grafo
python src/02_analise_basica.py

# 3. Teste de desempenho de diferentes algoritmos
python src/03_desempenho_algoritmos.py

# 4. Análise avançada (robustez, ataques, etc.)
python src/04_analise_avancada.py
```
