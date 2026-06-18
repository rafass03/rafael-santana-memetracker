import os

input_file = "data/quotes_2008-08.txt"
output_file = "data/edges_2days.csv"
os.makedirs("data", exist_ok=True)

# Vamos filtrar para os dias 01 e 02 de Agosto.
# Como o arquivo está ordenado por tempo, podemos parar de ler quando chegar no dia 03.
valid_days = ["2008-08-01", "2008-08-02"]
stop_day = "2008-08-03"

current_p = None
in_valid_time = False

edges_count = 0

print(f"Lendo {input_file} e extraindo arestas para {output_file}...")

with open(input_file, 'rt', encoding='utf-8', errors='ignore') as fin, \
     open(output_file, 'wt', encoding='utf-8') as fout:
    
    # Escrever cabeçalho
    fout.write("source,target\n")
    
    for line in fin:
        line = line.strip()
        if not line:
            continue
            
        prefix = line[0]
        
        if prefix == 'P':
            parts = line.split('\t')
            if len(parts) > 1:
                current_p = parts[1]
                in_valid_time = False # Reset para a nova postagem
                
        elif prefix == 'T':
            parts = line.split('\t')
            if len(parts) > 1:
                time_str = parts[1]
                
                if any(time_str.startswith(day) for day in valid_days):
                    in_valid_time = True
                elif time_str.startswith(stop_day):
                    # Como o arquivo é cronológico, podemos parar a leitura totalmente aqui e poupar tempo
                    print(f"Chegamos ao dia {stop_day}. Parando a extração.")
                    break
                else:
                    in_valid_time = False
                    
        elif prefix == 'L':
            if in_valid_time and current_p:
                parts = line.split('\t')
                if len(parts) > 1:
                    target_l = parts[1]
                    fout.write(f"{current_p},{target_l}\n")
                    edges_count += 1
                    
                    if edges_count % 100000 == 0:
                        print(f"Extraídas {edges_count} arestas...")

print(f"Extração concluída! Total de arestas encontradas nos 2 dias: {edges_count}")
