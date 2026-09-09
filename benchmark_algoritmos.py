import hashlib
import bisect

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
