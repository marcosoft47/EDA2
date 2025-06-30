from __future__ import annotations
from typing import Optional
from numpy import ndarray, array, uint32

class NoAVL:
    def __init__(self, chave: int, cor = array([0,0,0])):
        self.chave: int = chave
        self.cor: ndarray = cor
        self.altura: int = 1
        self.esquerda: Optional[NoAVL] = None
        self.direita: Optional[NoAVL] = None

class ArvoreAVL:
    def __init__(self):
        self.raiz: Optional[NoAVL] = None
    
    def __str__(self) -> str:
        def _preencher(no: NoAVL | None, linha: int, coluna: int, matriz: list[list[str]], largura: int) -> None:
            if no is None:
                return
            meio = coluna + largura // 2
            chaveStr = str(no.chave)
            for i, c in enumerate(chaveStr):
                matriz[linha][meio - len(chaveStr)//2 + i] = c
            if no.esquerda:
                _preencher(no.esquerda, linha + 2, coluna, matriz, largura // 2)
            if no.direita:
                _preencher(no.direita, linha + 2, coluna + largura // 2, matriz, largura // 2)

        if self.vazia():
            return "(árvore vazia)"

        altura = self._altura(self.raiz)
        largura = 2 ** (altura + 1)
        linhas = altura * 2 - 1
        matriz = [[" " for _ in range(largura)] for _ in range(linhas)]

        _preencher(self.raiz, 0, 0, matriz, largura)

        return "\n".join("".join(linha).rstrip() for linha in matriz)
    
    def vazia(self) -> bool:
        return self.raiz is None
    
    def inserir(self, chave: int, cor: ndarray) -> None:
        def _inserir(no: Optional[NoAVL], chave: int, cor: ndarray) -> NoAVL:
            if no is None:
                return NoAVL(chave, cor=cor)
            if chave < no.chave:
                no.esquerda = _inserir(no.esquerda, chave, cor)
            elif chave > no.chave:
                no.direita = _inserir(no.direita, chave, cor)
            else:
                return no  # Ignora chaves duplicadas

            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
            return self._balancear(no)

        self.raiz = _inserir(self.raiz, chave, cor)


    def remover(self, chave: int) -> None:
        def _remover(no: Optional[NoAVL], chave: int) -> Optional[NoAVL]:
            if no is None:
                return None
            if chave < no.chave:
                no.esquerda = _remover(no.esquerda, chave)
            elif chave > no.chave:
                no.direita = _remover(no.direita, chave)
            else:
                if no.esquerda is None:
                    return no.direita
                elif no.direita is None:
                    return no.esquerda
                temp = self._minimo(no.direita)
                no.chave = temp.chave
                no.direita = _remover(no.direita, temp.chave)

            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
            return self._balancear(no)

        self.raiz = _remover(self.raiz, chave)

    def buscar(self, chave: int) -> ndarray:
        def _buscar(no: Optional[NoAVL], chave: int) -> ndarray:
            if no is None:
                print(f'Erro! Não foi encontrado entrada com chave {chave}')
                return array([0,0,0])
            if chave == no.chave:
                return no.cor
            if chave < no.chave:
                return _buscar(no.esquerda, chave)
            return _buscar(no.direita, chave)

        return _buscar(self.raiz, chave)

    def listarEmOrdem(self) -> list[int]:
        def _emOrdem(no: Optional[NoAVL], resultado: list[int]) -> None:
            if no:
                _emOrdem(no.esquerda, resultado)
                resultado.append(no.chave)
                _emOrdem(no.direita, resultado)

        resultado: list[int] = []
        _emOrdem(self.raiz, resultado)
        return resultado

    # ===== Métodos auxiliares de AVL =====

    def _altura(self, no: Optional[NoAVL]) -> int:
        return no.altura if no else 0

    def _fatorBalanceamento(self, no: Optional[NoAVL]) -> int:
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _rotacaoDireita(self, y: NoAVL) -> NoAVL:
        x = y.esquerda
        t2 = x.direita if x else None

        if x:
            x.direita = y
        y.esquerda = t2

        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        if x:
            x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))

        return x if x else y

    def _rotacaoEsquerda(self, x: NoAVL) -> NoAVL:
        y = x.direita
        t2 = y.esquerda if y else None

        if y:
            y.esquerda = x
        x.direita = t2

        x.altura = 1 + max(self._altura(x.esquerda), self._altura(x.direita))
        if y:
            y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))

        return y if y else x

    def _balancear(self, no: NoAVL) -> NoAVL:
        balanceamento = self._fatorBalanceamento(no)

        # Caso de desbalanceamento à esquerda
        if balanceamento > 1:
            if no.esquerda and self._fatorBalanceamento(no.esquerda) < 0:
                no.esquerda = self._rotacaoEsquerda(no.esquerda)
            return self._rotacaoDireita(no)

        # Caso de desbalanceamento à direita
        if balanceamento < -1:
            if no.direita and self._fatorBalanceamento(no.direita) > 0:
                no.direita = self._rotacaoDireita(no.direita)
            return self._rotacaoEsquerda(no)

        return no


    def _minimo(self, no: NoAVL) -> NoAVL:
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual



# if __name__ == '__main__':
#     arvore = ArvoreAVL()

#     # Inserindo múltiplos nós
#     for valor in [30, 20, 40, 10, 25, 35, 50]:
#         arvore.inserir(valor)

#     # Exibe árvore inicial
#     print("Árvore inicial:")
#     print(arvore)

#     # 1 - Remover um nó folha (ex: 10)
#     print("\nRemovendo nó folha (10):")
#     arvore.remover(10)
#     print(arvore)

#     # 2 - Remover o nó raiz (30)
#     print("\nRemovendo nó raiz (30):")
#     arvore.remover(30)
#     print(arvore)

#     # 3 - Remover um nó central (ex: 40 - que não é folha nem raiz)
#     print("\nRemovendo nó central (40):")
#     arvore.remover(40)
#     print(arvore)