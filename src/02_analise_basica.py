import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os
import sys

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger("relatorio_parte1.txt")

input_file = "data/edges_2days.csv"
report_dir = "report"
os.makedirs(report_dir, exist_ok=True)

print("Carregando os dados e construindo o grafo direcionado original...")
df = pd.read_csv(input_file, on_bad_lines='skip')
G_orig = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())

num_v_orig = G_orig.number_of_nodes()
num_e_orig = G_orig.number_of_edges()
print(f"Grafo Original:")
print(f"  Vértices: {num_v_orig}")
print(f"  Arestas: {num_e_orig}")

print("\n2. Convertendo para grafo não-direcionado e removendo auto-loops...")
G = G_orig.to_undirected()
G.remove_edges_from(nx.selfloop_edges(G))

num_v = G.number_of_nodes()
num_e = G.number_of_edges()
print(f"Grafo Estático Não-Direcionado (Sem auto-loops):")
print(f"  Vértices: {num_v}")
print(f"  Arestas: {num_e}")

# Distribuição de graus
degrees = [d for n, d in G.degree()]
min_deg = np.min(degrees)
max_deg = np.max(degrees)
avg_deg = np.mean(degrees)
print(f"  Grau Mínimo: {min_deg}")
print(f"  Grau Máximo: {max_deg}")
print(f"  Grau Médio: {avg_deg:.4f}")

density = nx.density(G)
print(f"  Densidade: {density:.6f}")

print("\n3. Calculando Componentes Conexas...")
# Componentes conexas
connected_components = list(nx.connected_components(G))
num_cc = len(connected_components)
print(f"  Número de componentes conexas: {num_cc}")

# Tamanho de cada componente (top 10 maiores para não poluir se houver milhares)
cc_sizes = sorted([len(c) for c in connected_components], reverse=True)
print(f"  Tamanho das 10 maiores componentes: {cc_sizes[:10]}")
if len(cc_sizes) > 10:
    print(f"  Tamanho das demais componentes: as {len(cc_sizes)-10} componentes restantes variam de {min(cc_sizes[10:])} a {max(cc_sizes[10:])} nós.")

# Extraindo a Maior Componente Conexa (LCC)
lcc_nodes = max(connected_components, key=len)
LCC = G.subgraph(lcc_nodes).copy()
print(f"\n4. Analisando a Maior Componente Conexa (LCC)...")
print(f"  Vértices LCC: {LCC.number_of_nodes()} ({(LCC.number_of_nodes()/num_v)*100:.2f}% do total)")
print(f"  Arestas LCC: {LCC.number_of_edges()} ({(LCC.number_of_edges()/num_e)*100:.2f}% do total)")

# Coeficiente de clusterização e triângulos
print("\n5. Calculando Clusterização e Triângulos na LCC...")
t0 = time.time()
avg_clustering = nx.average_clustering(LCC)
print(f"  Coeficiente de clusterização médio: {avg_clustering:.4f}")
triangles = sum(nx.triangles(LCC).values()) // 3
print(f"  Número de triângulos: {triangles} (Tempo: {time.time()-t0:.2f}s)")

# Diâmetro, Raio e Comprimento Médio dos Caminhos
print("\n6. Calculando Diâmetro, Raio e Comprimento Médio dos Caminhos...")
if LCC.number_of_nodes() > 5000:
    print("  Aplicando amostragem em 500 nós escolhidos aleatoriamente para estimar...")
    
    sampled_nodes = random.sample(list(LCC.nodes()), min(500, LCC.number_of_nodes()))
    
    path_lengths = []
    eccentricities = []
    
    for n in sampled_nodes:
        # Menores caminhos a partir do nó n
        lengths = nx.single_source_shortest_path_length(LCC, n)
        if len(lengths) > 1:
            path_lengths.extend(list(lengths.values())[1:]) # Ignora distância 0 para o próprio nó
            eccentricities.append(max(lengths.values()))
    
    avg_path = np.mean(path_lengths) if path_lengths else 0
    approx_diameter = max(eccentricities) if eccentricities else 0
    approx_radius = min(eccentricities) if eccentricities else 0
    
    print(f"  Comprimento médio dos caminhos (Estimado): {avg_path:.4f}")
    print(f"  Diâmetro (Estimado): {approx_diameter}")
    print(f"  Raio (Estimado): {approx_radius}")
else:
    t0 = time.time()
    avg_path = nx.average_shortest_path_length(LCC)
    diameter = nx.diameter(LCC)
    radius = nx.radius(LCC)
    print(f"  Comprimento médio dos caminhos: {avg_path:.4f}")
    print(f"  Diâmetro: {diameter}")
    print(f"  Raio: {radius}")
    print(f"  (Tempo de cálculo: {time.time()-t0:.2f}s)")

print("\n7. Gerando Gráficos...")
# Plot da distribuição de graus (escala Log-Log)
plt.figure(figsize=(8, 6))
degree_counts = nx.degree_histogram(G)
x = range(len(degree_counts))
y = [z / float(sum(degree_counts)) for z in degree_counts]

plt.loglog(x, y, color='b', marker='.')
plt.title("Distribuição de Graus (Grafo Total)")
plt.xlabel("Grau (k)")
plt.ylabel("P(k)")
plt.grid(True, which="both", ls="--")
plt.savefig(os.path.join(report_dir, "distribuicao_graus.png"))
plt.close()

# Visualização reduzida do grafo
print("  Gerando visualização reduzida...")
core_graph = nx.k_core(LCC, k=min(max_deg // 2, 5)) 
if core_graph.number_of_nodes() < 10 or core_graph.number_of_nodes() > 1000:
    # Fallback para amostra ego graph do nó de maior grau
    max_node = max(dict(LCC.degree()).items(), key=lambda x: x[1])[0]
    core_graph = nx.ego_graph(LCC, max_node, radius=1)
    if core_graph.number_of_nodes() > 800:
        neighbors = list(LCC.neighbors(max_node))[:800]
        core_graph = LCC.subgraph([max_node] + neighbors)

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(core_graph, seed=42)
nx.draw(core_graph, pos, node_size=10, node_color='r', edge_color='gray', with_labels=False, alpha=0.6)
plt.title(f"Visualização de uma sub-rede do LCC ({core_graph.number_of_nodes()} nós)")
plt.savefig(os.path.join(report_dir, "visualizacao_grafo.png"))
plt.close()

print("\nAnálise concluída com sucesso! Resultados salvos.")
