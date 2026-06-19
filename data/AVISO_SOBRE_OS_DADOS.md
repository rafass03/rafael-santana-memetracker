=================================================
 AVISO IMPORTANTE SOBRE OS DADOS!
=================================================

Os arquivos de dados brutos (`quotes_2008-08.txt.gz e quotes_2008-08.txt`) NÃO foram incluídos neste repositório devido ao seu tamanho massivo (4 GB e 1,1GB), o que excede os limites do GitHub.

O dado processado resultante do 01 do Jupyter ou Script (`edges_2days.csv`) possui 188 MB e também não pôde ser incluído de forma direta. Em vez disso, ele está disponibilizado aqui nesta pasta de forma compactada: **`edges_2days.zip`**.

### INSTRUÇÕES:

**Se você for rodar os Notebooks 02, 03 e 04 (ou os respectivos scripts):**
Você só precisa descompactar o arquivo `edges_2days.zip` aqui dentro da pasta `data/`. Com o `edges_2days.csv` gerado, as análises funcionarão perfeitamente.

**Se você for testar a extração do zero (Notebook 01 / Script 01):**
1. Faça o download do dataset original (`quotes_2008-08.txt.gz`) no site do SNAP (https://snap.stanford.edu/data/memetracker9.html).
2. Descompacte o arquivo.
3. Coloque o arquivo de texto resultante COM O NOME EXATO de `quotes_2008-08.txt` NESTA pasta (`data/`).
4. Após isso, você poderá rodar a etapa 1 de extração temporal sem problemas!