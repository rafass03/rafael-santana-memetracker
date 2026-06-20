import networkx as nx
import pandas as pd
import time
import numpy as np
import scipy.stats as st
import random
import sys

def print_and_write(f, text):
    print(text)
    f.write(text + "\n")

def calc_stats(times):
    n = len(times)
    mean = np.mean(times)
    std = np.std(times, ddof=1) if n > 1 else 0.0
    
    # 95% Confidence Interval
    alpha = 0.05
    if n >= 30:
        # Z-distribution
        z = st.norm.ppf(1 - alpha/2)
        margin = z * (std / np.sqrt(n)) if n > 0 else 0
        dist_name = "Normal (Z)"
    else:
        # t-Student
        t = st.t.ppf(1 - alpha/2, n-1) if n > 1 else 0
        margin = t * (std / np.sqrt(n)) if n > 0 else 0
        dist_name = "t-Student"
        
    return mean, std, margin, dist_name, n

def run_experiment(f, name, func, n_runs):
    print_and_write(f, f"Iniciando: {name} ({n_runs} rodadas)")
    times = []
    for i in range(n_runs):
        start = time.time()
        func(i)
        times.append(time.time() - start)
        
    mean, std, margin, dist_name, n = calc_stats(times)
    
    res = (f"[{name}] Concluido.\n"
           f"   Distribuicao: {dist_name} (n={n})\n"
           f"   Media de Tempo: {mean:.5f}s\n"
           f"   Desvio Padrao:  {std:.5f}s\n"
           f"   IC (95%):       {mean:.5f}s +- {margin:.5f}s  [{mean-margin:.5f}s, {mean+margin:.5f}s]\n"
           f"{'-'*50}")
    print_and_write(f, res)

def main():
    out_file = open("relatorio_parte2.txt", "w")
    print_and_write(out_file, "CARREGANDO DADOS...")
    
    # Carrega direcionado
    df = pd.read_csv('data/edges_2days.csv', on_bad_lines='skip')
    G_dir = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())
    print_and_write(out_file, f"Grafo Direcionado Original: {G_dir.number_of_nodes()} V, {G_dir.number_of_edges()} E")
    
    # Converte para nao-direcionado e extrai LCC
    G_undir = G_dir.to_undirected()
    G_undir.remove_edges_from(nx.selfloop_edges(G_undir))
    
    connected_components = list(nx.connected_components(G_undir))
    lcc_nodes = max(connected_components, key=len)
    LCC = G_undir.subgraph(lcc_nodes).copy()
    
    print_and_write(out_file, f"Maior Componente Conexa (LCC): {LCC.number_of_nodes()} V, {LCC.number_of_edges()} E\n")
    print_and_write(out_file, "="*50)
    
    # Preparar fontes aleatorias
    nodes_list = list(LCC.nodes())
    random.seed(42)
    sources_30 = random.sample(nodes_list, 30)
    
    # 1. BFS na LCC
    run_experiment(out_file, "Busca em Largura (BFS)", lambda i: list(nx.bfs_edges(LCC, sources_30[i])), 30)
    
    # 2. DFS na LCC
    run_experiment(out_file, "Busca em Profundidade (DFS)", lambda i: list(nx.dfs_edges(LCC, sources_30[i])), 30)
    
    # 3. Verificacao de Eulerianidade (checa grau e componente)
    # n=30 execuções para ter estatística
    run_experiment(out_file, "Verificacao de Eulerianidade", lambda i: nx.is_eulerian(G_undir), 30)
    
    # 4. Arvore Geradora Minima (Prim e Kruskal na LCC)
    run_experiment(out_file, "AGM - Algoritmo de Prim", lambda i: nx.minimum_spanning_tree(LCC, algorithm='prim'), 30)
    run_experiment(out_file, "AGM - Algoritmo de Kruskal", lambda i: nx.minimum_spanning_tree(LCC, algorithm='kruskal'), 30)
    
    # 5. Tarjan (SCC no grafo Direcionado Original)
    run_experiment(out_file, "Algoritmo de Tarjan (SCC)", lambda i: list(nx.strongly_connected_components(G_dir)), 30)
    
    print_and_write(out_file, "\n--- EXTRAINDO SUBGRAFOS PARA ALGORITMOS MAIS PESADOS ---")
    max_node = max(dict(LCC.degree()).items(), key=lambda x: x[1])[0]
    
    # Subgrafo de 5000 nós para Dijkstra vs Bellman-Ford
    sub_5k_nodes = list(nx.bfs_tree(LCC, max_node, depth_limit=3).nodes())[:5000]
    sub_5k = LCC.subgraph(sub_5k_nodes).copy()
    print_and_write(out_file, f"Subgrafo 5K: {sub_5k.number_of_nodes()} V, {sub_5k.number_of_edges()} E")
    n_runs_5k = min(30, sub_5k.number_of_nodes())
    sources_sub_30 = random.sample(list(sub_5k.nodes()), n_runs_5k)
    
    # Subgrafo de 200 nós para Floyd-Warshall (O(V^3))
    sub_200_nodes = list(nx.bfs_tree(LCC, max_node, depth_limit=2).nodes())[:200]
    sub_200 = LCC.subgraph(sub_200_nodes).copy()
    print_and_write(out_file, f"Subgrafo 200: {sub_200.number_of_nodes()} V, {sub_200.number_of_edges()} E\n")
    
    # 6. Dijkstra vs Bellman-Ford vs BFS no Subgrafo de 5000 nós
    run_experiment(out_file, "Caminhos Minimos: BFS (Baseline 5K)", lambda i: list(nx.bfs_edges(sub_5k, sources_sub_30[i])), n_runs_5k)
    run_experiment(out_file, "Caminhos Minimos: Dijkstra (5K)", lambda i: nx.single_source_dijkstra_path_length(sub_5k, sources_sub_30[i], weight=None), n_runs_5k)
    run_experiment(out_file, "Caminhos Minimos: Bellman-Ford (5K)", lambda i: nx.single_source_bellman_ford_path_length(sub_5k, sources_sub_30[i], weight=None), n_runs_5k)
    
    # 7. Floyd-Warshall no Subgrafo de 200 nós (APSP)
    # Vamos rodar n=10 (amostra pequena) para forçar o uso da t-Student
    n_runs_200 = min(10, sub_200.number_of_nodes())
    run_experiment(out_file, "Floyd-Warshall (APSP 200)", lambda i: nx.floyd_warshall(sub_200, weight=None), n_runs_200)

    print_and_write(out_file, "================ CONCLUIDO ================")
    out_file.close()

if __name__ == "__main__":
    main()
