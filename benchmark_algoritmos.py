import time
import hashlib
import bisect
import pandas as pd
import numpy as np

class DistribuidorDeCarga:
    def __init__(self, num_replicas=20):
        self.num_replicas = num_replicas
        self.anel = {}
        self.chaves_ordenadas = []

    def _gerar_hash(self, chave):
        return int(hashlib.md5(chave.encode('utf-8')).hexdigest(), 16)

    def adicionar_servidores_em_lote(self, nomes_servidores):
        for nome_servidor in nomes_servidores:
            for i in range(self.num_replicas):
                chave_replica = f"{nome_servidor}:{i}"
                hash_replica = self._gerar_hash(chave_replica)
                self.anel[hash_replica] = nome_servidor
                self.chaves_ordenadas.append(hash_replica)
        self.chaves_ordenadas.sort()

    def remover_servidor(self, nome_servidor):
        for i in range(self.num_replicas):
            chave_replica = f"{nome_servidor}:{i}"
            hash_replica = self._gerar_hash(chave_replica)
            if hash_replica in self.anel:
                del self.anel[hash_replica]
                self.chaves_ordenadas.remove(hash_replica)

    def obter_servidor(self, requisicao_id):
        if not self.anel: return None
        hash_requisicao = self._gerar_hash(requisicao_id)
        # Busca binária O(log n)
        indice = bisect.bisect(self.chaves_ordenadas, hash_requisicao)
        if indice == len(self.chaves_ordenadas):
            indice = 0
        return self.anel[self.chaves_ordenadas[indice]]


class DistribuidorRoundRobin:
    def __init__(self):
        self.servidores = []
        self.indice_atual = 0

    def adicionar_servidores_em_lote(self, nomes_servidores):
        self.servidores.extend(nomes_servidores)

    def remover_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            self.servidores.remove(nome_servidor)
            if self.indice_atual >= len(self.servidores):
                self.indice_atual = 0

    def obter_servidor(self, requisicao_id=None):
        if not self.servidores: return None
        # Avanço O(1)
        servidor_alvo = self.servidores[self.indice_atual]
        self.indice_atual = (self.indice_atual + 1) % len(self.servidores)
        return servidor_alvo

if __name__ == "__main__":
    tamanhos_n = [100, 1000, 5000, 10000, 30000, 50000]
    num_reqs = 10000
    repeticoes = 10
    requisicoes = [f"req_{i}" for i in range(num_reqs)]

    tempos_hc, tempos_rr = [], []
    realoc_hc, realoc_rr = [], []

    for n in tamanhos_n:
        print(f"Executando pipeline para n={n} servidores...")
        nomes_servidores = [f"Serv_{i}" for i in range(n)]
        
        hc = DistribuidorDeCarga()
        rr = DistribuidorRoundRobin()
        hc.adicionar_servidores_em_lote(nomes_servidores)
        rr.adicionar_servidores_em_lote(nomes_servidores)
        
        # EXPERIMENTO 1: TEMPO O(log n) vs O(1)
        tempos_hc_run, tempos_rr_run = [], []
        
        for _ in range(repeticoes):
            rr.indice_atual = 0
            
            inicio = time.perf_counter()
            for r in requisicoes: rr.obter_servidor(r)
            tempos_rr_run.append((time.perf_counter() - inicio) * 1000)
            
            inicio = time.perf_counter()
            for r in requisicoes: hc.obter_servidor(r)
            tempos_hc_run.append((time.perf_counter() - inicio) * 1000)
            
        tempos_rr.append(np.mean(tempos_rr_run))
        tempos_hc.append(np.mean(tempos_hc_run))
        
        # EXPERIMENTO 2: TAXA DE REALOCAÇÃO (Estabilidade)
        mapa_rr = {r: rr.obter_servidor(r) for r in requisicoes}
        mapa_hc = {r: hc.obter_servidor(r) for r in requisicoes}
        
        # Queda do servidor posicionado no centro do cluster
        servidor_removido = nomes_servidores[n // 2]
        rr.remover_servidor(servidor_removido)
        hc.remover_servidor(servidor_removido)
        
        rr.indice_atual = 0 
        
        mudancas_rr = sum(1 for r in requisicoes if mapa_rr[r] != rr.obter_servidor(r))
        mudancas_hc = sum(1 for r in requisicoes if mapa_hc[r] != hc.obter_servidor(r))
        
        realoc_rr.append((mudancas_rr / num_reqs) * 100)
        realoc_hc.append((mudancas_hc / num_reqs) * 100)

    print("Salvando DataFrames em .csv...")
    pd.DataFrame({
        'Tamanho_Cluster_n': tamanhos_n,
        'Tempo_RoundRobin_ms': tempos_rr,
        'Tempo_HashingConsistente_ms': tempos_hc
    }).to_csv('resultados_tempo.csv', index=False)

    pd.DataFrame({
        'Tamanho_Cluster_n': tamanhos_n,
        'Realocacao_RoundRobin_pct': realoc_rr,
        'Realocacao_HashingConsistente_pct': realoc_hc
    }).to_csv('resultados_realocacao.csv', index=False)