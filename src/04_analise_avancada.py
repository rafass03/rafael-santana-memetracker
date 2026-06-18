import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import random
import os
import collections

report_dir = "report"
os.makedirs(report_dir, exist_ok=True)

def print_and_write(f, text):
    print(text)
    f.write(text + "\n")

def approx_average_path_length(G, sample_size=50):
    if G.number_of_nodes() == 0:
        return 0
    sampled_nodes = random.sample(list(G.nodes()), min(sample_size, G.number_of_nodes()))
    path_lengths = []
    for n in sampled_nodes:
        lengths = nx.single_source_shortest_path_length(G, n)
        if len(lengths) > 1:
            path_lengths.extend(list(lengths.values())[1:])
    return np.mean(path_lengths) if path_lengths else 0

def main():
    out_file = open(os.path.join(report_dir, "relatorio_parte3.txt"), "w")
    print_and_write(out_file, "1. CARREGANDO DADOS E LCC...")
    df = pd.read_csv('data/edges_2days.csv', on_bad_lines='skip')
    G_dir = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())
    G_undir = G_dir.to_undirected()
    G_undir.remove_edges_from(nx.selfloop_edges(G_undir))
    
    connected_components = list(nx.connected_components(G_undir))
    lcc_nodes = max(connected_components, key=len)
    LCC = G_undir.subgraph(lcc_nodes).copy()
    
    N = LCC.number_of_nodes()
    E = LCC.number_of_edges()
    print_and_write(out_file, f"LCC: {N} Vertices, {E} Arestas")
    
    # SMALL-WORLD
    print_and_write(out_file, "\n2. ANALISANDO SMALL-WORLD...")
    k_avg = 2 * E / N
    print_and_write(out_file, f"Grau medio <k>: {k_avg:.4f}")
    
    # Valores do Grafo Real (Amostragem para C e L devido ao tamanho massivo)
    print("Amostrando LCC para Clusterização (10k nós)...")
    sampled_cluster_nodes = random.sample(list(LCC.nodes()), min(10000, N))
    C_real = nx.average_clustering(LCC, nodes=sampled_cluster_nodes)
    print("Amostrando LCC para Caminho Medio (50 nós)...")
    L_real = approx_average_path_length(LCC, 50)
    
    # Valores do Grafo Aleatorio Teorico (Erdos-Renyi Equivalente)
    C_rand = k_avg / N
    L_rand = np.log(N) / np.log(k_avg) if k_avg > 1 else 0
    
    sigma = (C_real / C_rand) / (L_real / L_rand) if C_rand > 0 and L_rand > 0 else 0
    
    print_and_write(out_file, f"Clusterizacao Real (C): {C_real:.6f}")
    print_and_write(out_file, f"Clusterizacao Random (C_rand): {C_rand:.6f}")
    print_and_write(out_file, f"Caminho Medio Real (L): {L_real:.4f}")
    print_and_write(out_file, f"Caminho Medio Random (L_rand): {L_rand:.4f}")
    print_and_write(out_file, f"Indice Sigma (Small-worldness): {sigma:.4f} (Se > 1, eh small-world)")
    
    # LEI DE POTENCIA
    print_and_write(out_file, "\n3. ANALISANDO POWER LAW...")
    degree_sequence = [d for n, d in G_undir.degree()]
    counts = collections.Counter(degree_sequence)
    
    # Prepara para Log-Log
    x_k = []
    y_pk = []
    total_nodes = G_undir.number_of_nodes()
    
    for k, freq in counts.items():
        if k > 0:
            x_k.append(np.log10(k))
            y_pk.append(np.log10(freq / total_nodes))
            
    slope, intercept, r_value, p_value, std_err = st.linregress(x_k, y_pk)
    gamma = -slope
    
    print_and_write(out_file, f"Expoente Gamma (gamma): {gamma:.4f}")
    print_and_write(out_file, f"R-squared: {r_value**2:.4f}")
    
    # Plotting Power Law
    plt.figure(figsize=(8,6))
    plt.scatter(x_k, y_pk, alpha=0.5, label='Dados reais', color='b', marker='.')
    plt.plot(x_k, intercept + slope * np.array(x_k), 'r', label=f'Reta Linear (gamma={gamma:.2f})')
    plt.title("Distribuicao de Graus (Escala Log-Log)")
    plt.xlabel("log10(Grau k)")
    plt.ylabel("log10(P(k))")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(report_dir, "power_law.png"))
    plt.close()
    
    # ROBUSTEZ
    print_and_write(out_file, "\n4. INICIANDO TESTE DE ROBUSTEZ...")
    r = int(0.05 * N)
    T = 30
    print_and_write(out_file, f"Tamanho da LCC: {N}")
    print_and_write(out_file, f"Nós a serem removidos (5%): {r}")
    
    metrics_rand = {'A': [], 'B': [], 'C': [], 'D': []}
    
    print_and_write(out_file, f"Iniciando {T} repeticoes de ataque ALEATORIO...")
    nodes_list = list(LCC.nodes())
    
    for t in range(T):
        if t % 5 == 0: print(f" Repeticao {t}/{T}")
        G_fail = LCC.copy()
        to_remove = random.sample(nodes_list, r)
        G_fail.remove_nodes_from(to_remove)
        
        cc = list(nx.connected_components(G_fail))
        if cc:
            lcc_fail = max(cc, key=len)
            A = len(lcc_fail)
            G_fail_lcc = G_fail.subgraph(lcc_fail)
            C = approx_average_path_length(G_fail_lcc, 20)
        else:
            A = 0; C = 0
            
        B = len(cc)
        D = sum(1 for n in G_fail.nodes() if G_fail.degree(n) == 0) / G_fail.number_of_nodes() if G_fail.number_of_nodes() > 0 else 0
        
        metrics_rand['A'].append(A)
        metrics_rand['B'].append(B)
        metrics_rand['C'].append(C)
        metrics_rand['D'].append(D)
        
    print_and_write(out_file, "Ataque DIRECIONADO (Top 5% Hubs)...")
    sorted_nodes = sorted(LCC.degree(), key=lambda x: x[1], reverse=True)
    hubs_to_remove = [n for n, d in sorted_nodes[:r]]
    
    G_attack = LCC.copy()
    G_attack.remove_nodes_from(hubs_to_remove)
    
    cc_attack = list(nx.connected_components(G_attack))
    if cc_attack:
        lcc_attack = max(cc_attack, key=len)
        A_att = len(lcc_attack)
        C_att = approx_average_path_length(G_attack.subgraph(lcc_attack), 20)
    else:
        A_att = 0; C_att = 0
        
    B_att = len(cc_attack)
    D_att = sum(1 for n in G_attack.nodes() if G_attack.degree(n) == 0) / G_attack.number_of_nodes() if G_attack.number_of_nodes() > 0 else 0
    
    print_and_write(out_file, "\n--- RESULTADOS ROBUSTEZ ---")
    print_and_write(out_file, f"Métrica A (Tam. LCC) - Aleatorio: {np.mean(metrics_rand['A']):.1f} +- {np.std(metrics_rand['A']):.1f} | Direcionado: {A_att}")
    print_and_write(out_file, f"Métrica B (Num. CC)  - Aleatorio: {np.mean(metrics_rand['B']):.1f} +- {np.std(metrics_rand['B']):.1f} | Direcionado: {B_att}")
    print_and_write(out_file, f"Métrica C (Caminhos) - Aleatorio: {np.mean(metrics_rand['C']):.3f} +- {np.std(metrics_rand['C']):.3f} | Direcionado: {C_att:.3f}")
    print_and_write(out_file, f"Métrica D (Isolados) - Aleatorio: {np.mean(metrics_rand['D'])*100:.2f}% +- {np.std(metrics_rand['D'])*100:.2f}% | Direcionado: {D_att*100:.2f}%")
    
    # Plotting Boxplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Robustez: Falhas Aleatorias vs Ataque Direcionado")
    
    def plot_box(ax, data, attack_val, title, ylabel):
        ax.boxplot(data, vert=True, patch_artist=True)
        ax.scatter([1], [attack_val], color='red', marker='*', s=150, zorder=5, label='Ataque Hubs')
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticks([1])
        ax.set_xticklabels(['Aleatorio (30x)'])
        ax.legend()

    plot_box(axes[0,0], metrics_rand['A'], A_att, 'A: Tamanho da Maior Componente', 'Vertices')
    plot_box(axes[0,1], metrics_rand['B'], B_att, 'B: Num de Componentes', 'Componentes')
    plot_box(axes[1,0], metrics_rand['C'], C_att, 'C: Comprimento Medio dos Caminhos', 'Passos')
    plot_box(axes[1,1], metrics_rand['D'], D_att, 'D: Fracao de Nos Isolados', 'Fracao')
    
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, "robustness_boxplot.png"))
    plt.close()

    print_and_write(out_file, "\nScript FINALIZADO COM SUCESSO!")
    out_file.close()

if __name__ == "__main__":
    main()
