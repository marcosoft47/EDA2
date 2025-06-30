class No():
    def __init__(self, chave: int):
        self.chave = chave
        self.esquerda: No | None = None
        self.direita: No | None = None

class Arvore():
    def __init__(self):
        self.raiz: No | None = None

    def __str__(self) -> str:
        def _preencher(no: No | None, linha: int, coluna: int, matriz: list[list[str]], largura: int) -> None:
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

        altura = self.altura(self.raiz)
        largura = 2 ** (altura + 1)
        linhas = altura * 2 - 1
        matriz = [[" " for _ in range(largura)] for _ in range(linhas)]

        _preencher(self.raiz, 0, 0, matriz, largura)

        return "\n".join("".join(linha).rstrip() for linha in matriz)


    ######################### Primeira parte #########################
    def inserir(self, chave: int):
        def _inserir(no: No | None, chave: int) -> No:
            if no is None:
                return No(chave)
            if chave < no.chave:
                no.esquerda = _inserir(no.esquerda, chave)
            elif chave > no.chave:
                no.direita = _inserir(no.direita, chave)
            return no
                
        self.raiz = _inserir(self.raiz, chave)


    def remover(self, chave:int ):
        def _minimo(no: No) -> No:
            atual = no
            while atual.esquerda is not None:
                atual = atual.esquerda
            return atual
        def _remover(no: No | None, chave: int):
            if no is None:
                return None
            
            # Começa a buscar o Nó desejado
            if chave < no.chave:
                no.esquerda = _remover(no.esquerda, chave)
            elif chave > no.chave:
                no.direita = _remover(no.direita, chave)

            else:
                # Nó com 1 ou nenhum filho
                if no.esquerda is None:
                    return no.direita
                elif no.direita is None:
                    return no.esquerda
                # Nó com dois filhos
                sucessor = _minimo(no.direita)
                no.chave = sucessor.chave
                no.direita = _remover(no.direita, sucessor.chave)
            return no
        
        self.raiz = _remover(self.raiz, chave)

    def buscar(self, chave: int) -> bool:
        def _buscar(no: No | None, chave:int) -> bool:
            if no is None:
                return False
            if chave == no.chave:
                return True
            if chave < no.chave:
                return _buscar(no.esquerda, chave)
            else:
                return _buscar(no.direita, chave)
        
        return _buscar(self.raiz, chave)

    def listar(self) -> list:
        def ordenar(no: No | None, elementos: list[int]):
            if no:
                ordenar(no.esquerda, elementos)
                elementos.append(no.chave)
                ordenar(no.direita, elementos)
        elementos = []
        ordenar(self.raiz, elementos)
        return elementos


    ######################### Segunda parte #########################
    def vazia(self) -> bool:
        return self.raiz is None
    
    def tamanho(self) -> int:
        return len(self.listar())
    
    def altura(self, no: No | None) -> int:
        if no is None:
            return 0
        return 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def larguraNivel(self) -> list[int]:
        if self.raiz is None:
            return []

        fila = [self.raiz]
        larguras = []

        while fila:
            nivelTamanho = len(fila)
            larguras.append(nivelTamanho)
            novaFila = []

            for no in fila:
                if no.esquerda:
                    novaFila.append(no.esquerda)
                if no.direita:
                    novaFila.append(no.direita)

            fila = novaFila

        return larguras
    
    def estaCompleta(self) -> bool:
        if self.raiz is None:
            return True

        fila = [self.raiz]
        encontrouFolhaIncompleta = False

        while fila:
            proximaFila = []

            for no in fila:
                if no.esquerda:
                    if encontrouFolhaIncompleta:
                        return False
                    proximaFila.append(no.esquerda)
                else:
                    encontrouFolhaIncompleta = True

                if no.direita:
                    if encontrouFolhaIncompleta:
                        return False
                    proximaFila.append(no.direita)
                else:
                    encontrouFolhaIncompleta = True

            fila = proximaFila

        return True


    def cheia(self) -> bool:
        def _verificar(no: No | None) -> bool:
            if no is None:
                return True
            if (no.esquerda is None) != (no.direita is None):  # XOR implícito
                return False
            return _verificar(no.esquerda) and _verificar(no.direita)

        return _verificar(self.raiz)
    



    ######################### Terceira parte #########################

    def preOrdem(self) -> list[int]:
        def visitar(no: No | None, resultado: list[int]) -> None:
            if no:
                resultado.append(no.chave)
                visitar(no.esquerda, resultado)
                visitar(no.direita, resultado)

        resultado: list[int] = []
        visitar(self.raiz, resultado)
        return resultado


    def emOrdem(self) -> list[int]:
        def visitar(no: No | None, resultado: list[int]) -> None:
            if no:
                visitar(no.esquerda, resultado)
                resultado.append(no.chave)
                visitar(no.direita, resultado)

        resultado: list[int] = []
        visitar(self.raiz, resultado)
        return resultado


    def posOrdem(self) -> list[int]:
        def visitar(no: No | None, resultado: list[int]) -> None:
            if no:
                visitar(no.esquerda, resultado)
                visitar(no.direita, resultado)
                resultado.append(no.chave)

        resultado: list[int] = []
        visitar(self.raiz, resultado)
        return resultado

if __name__ == '__main__':
    arvore = Arvore()
    for valor in [4, 2, 1, 3, 8, 6, 5, 7, 9, 10]:
        arvore.inserir(valor)
    arvore.remover(10)

    print("Pré-ordem:", arvore.preOrdem())  # [8, 3, 1, 6, 10, 14]
    print("Em-ordem:", arvore.emOrdem())    # [1, 3, 6, 8, 10, 14]
    print("Pós-ordem:", arvore.posOrdem())  # [1, 6, 3, 14, 10, 8]
    print(arvore)
