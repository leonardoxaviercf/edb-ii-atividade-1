import pandas as pd
import matplotlib.pyplot as plt

def plotar_grafico_tempo():
    df = pd.read_csv('resultados_tempo.csv')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Tamanho_Cluster_n'], df['Tempo_RoundRobin_ms'], 
             marker='o', color='#E74C3C', label='Round-Robin O(1)', linewidth=2)
    plt.plot(df['Tamanho_Cluster_n'], df['Tempo_HashingConsistente_ms'], 
             marker='s', color='#2980B9', label='Hashing Consistente O(log n)', linewidth=2)
    
    plt.title('Tempo de Roteamento de 10.000 Requisições (Tempo Médio)')
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