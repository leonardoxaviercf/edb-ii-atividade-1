import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotar_grafico_tempo():
    df = pd.read_csv('resultados_tempo.csv')
    
    n_vals = df['Tamanho_Cluster_n']
    t_rr = df['Tempo_RoundRobin_ms']
    t_hc = df['Tempo_HashingConsistente_ms']

    constante_o1 = np.mean(t_rr)
    teorico_o1 = [constante_o1] * len(n_vals)

    n_first, n_last = n_vals.iloc[0], n_vals.iloc[-1]
    t_first, t_last = t_hc.iloc[0], t_hc.iloc[-1]
    
    a = (t_last - t_first) / (np.log(n_last) - np.log(n_first))
    b = t_first - a * np.log(n_first)
    teorico_ologn = a * np.log(n_vals) + b

    plt.figure(figsize=(10, 6))
    
    plt.plot(n_vals, teorico_o1, linestyle='--', color='#922B21', alpha=0.6, label='Curva Teórica O(1)')
    plt.plot(n_vals, teorico_ologn, linestyle='--', color='#154360', alpha=0.6, label='Curva Teórica O(log n)')
    
    plt.plot(n_vals, t_rr, marker='o', color='#E74C3C', label='Empírico (Round-Robin)', linewidth=2)
    plt.plot(n_vals, t_hc, marker='s', color='#3498DB', label='Empírico (Hashing Consistente)', linewidth=2)
    
    plt.title('Tempo de Roteamento de 10.000 Requisições (Teoria vs Prática)')
    plt.xlabel('Tamanho da Entrada (n) - Número de Servidores')
    plt.ylabel('Tempo de Execução (Milissegundos)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('grafico_tempo.png', dpi=300, bbox_inches='tight')
    print("Gráfico de Tempo salvo como 'grafico_tempo.png'")

def plotar_grafico_realocacao():
    df = pd.read_csv('resultados_realocacao.csv')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Tamanho_Cluster_n'], df['Realocacao_RoundRobin_pct'], 
             marker='o', color='#E74C3C', label='Round-Robin (~100%)', linewidth=2)
    plt.plot(df['Tamanho_Cluster_n'], df['Realocacao_HashingConsistente_pct'], 
             marker='s', color='#2980B9', label='Hashing Consistente O(1/n)', linewidth=2)
    
    plt.title('Estabilidade: Impacto da Queda de 1 Servidor')
    plt.xlabel('Tamanho da Entrada (n) - Número de Servidores')
    plt.ylabel('Taxa de Realocação de Requisições (%)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('grafico_realocacao.png', dpi=300, bbox_inches='tight')
    print("Gráfico de Realocação salvo como 'grafico_realocacao.png'")

if __name__ == "__main__":
    plotar_grafico_tempo()
    plotar_grafico_realocacao()