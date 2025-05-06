'''
    1. Ler $M$ registros do arquivo para a memória
    2. Selecionar no vetor em memória o registro r com menor chave
    3. Gravar o registro $r$ na partição de saída
    4. Substituir no vetor em memória o registro $r$ pelo próximo registro do arquivo de entrada
    5. Se a chave deste último for menor do que a chave recém gravada, considerá-lo **congelado** e ignorá-lo no restante do processamento
    6. Caso existam em memória registros **não congelados**, voltar ao passo 2
    7. Caso contrário
        1. Fechar a partição de saída
        2. Descongelar os registros congelados
        3. Abrir nova partição de saída
        4. Voltar ao passo 2
'''
def selecaoSubstituicao(arquivo, M):
    memoria = []
    particoes = []
    i = 0  # índice para percorrer o "arquivo"
    ultima_chave = -float('inf')  # Menor valor possível no início

    # Passo 1: Ler M registros do arquivo para a memória
    while i < len(arquivo) and len(memoria) < M:
        memoria.append(arquivo[i])
        i += 1

    congelado_flags = [False] * len(memoria)  # Flags de congelamento por índice
    particao_atual = []

    while memoria:
        # Passo 2: Selecionar o menor registro **não congelado**
        candidatos = [(val, idx) for idx, val in enumerate(memoria) if not congelado_flags[idx]]
        if not candidatos:
            # Passo 7: Todos congelados
            particoes.append(particao_atual)
            particao_atual = []
            congelado_flags = [False] * len(memoria)
            ultima_chave = -float('inf')
            continue

        # Encontrar menor valor entre não congelados
        val, idx = min(candidatos, key=lambda x: x[0])

        # Passo 3: Gravar registro na partição de saída
        particao_atual.append(val)
        ultima_chave = val

        # Passo 4: Substituir pelo próximo registro do arquivo
        if i < len(arquivo):
            proximo = arquivo[i]
            i += 1
            if proximo < ultima_chave:
                congelado_flags[idx] = True  # Passo 5: Congelar
            memoria[idx] = proximo
        else:
            # Se não há mais no arquivo, remove da memória
            memoria.pop(idx)
            congelado_flags.pop(idx)

    # Salvar última partição
    if particao_atual:
        particoes.append(particao_atual)

    return particoes

'''
    1. Colocar em memória o primeiro registro de cada partição em um nó folha da árvore
    2. Criar um nó raiz para os pares de nós folha, sendo a raiz o menor dos dois valores
    3. Repetir o passo 2 até chegar na raiz da árvore
    4. Retirar a raiz da árvore e inserir no arquivo classificado
    5. Atualizar o caminho do nó retirado
    6. Adicionar um novo valor ao nó folha vazio (apenas caso esteja vazio o nó)
    7. Repetir o passo 2, até encerrar as partições
'''
class NoArvore:
    def __init__(self, valor=None, indice_particao=None, folha=False):
        self.valor = valor
        self.indice_particao = indice_particao  # apenas em folhas
        self.folha = folha
        self.esq = None
        self.dir = None

    def __repr__(self):
        return f"{self.valor}"
    
# Construir a árvore de baixo para cima
def construirNo(nos):
    if len(nos) == 1:
        return nos[0]
    novos_nos = []
    for i in range(0, len(nos), 2):
        no_esq = nos[i]
        no_dir = nos[i + 1]
        vencedor = no_esq if no_esq.valor <= no_dir.valor else no_dir
        pai = NoArvore(vencedor.valor)
        pai.esq = no_esq
        pai.dir = no_dir
        novos_nos.append(pai)
    return construirNo(novos_nos)

def construirArvore(particoes):
    folhas = []

    # Criar nós folha com o primeiro valor de cada partição
    for i, part in enumerate(particoes):
        if part:
            valor = part.pop(0)
            no = NoArvore(valor, i, folha=True)
            folhas.append(no)

    # Se necessário, adicionar folhas "vazias" para completar a árvore binária completa
    while len(folhas) & (len(folhas) - 1):  # enquanto não for potência de 2
        folhas.append(NoArvore(float('inf'), folha=True))

    raiz = construirNo(folhas)
    return raiz, folhas

def recalcular(no):
        if no.folha:
            return no.valor
        no.valor = min(recalcular(no.esq), recalcular(no.dir))
        return no.valor

def atualizarArvore(raiz, folha_alvo):
    # Recalcular valores do caminho folha → raiz
    recalcular(raiz)


def arvoreBinariaVencedores(particoes: list[list[int]]):
    particoes = [p.copy() for p in particoes]  # evitar modificar original
    resultado = []

    raiz, folhas = construirArvore(particoes)

    while True:
        menor = raiz.valor
        if menor == float('inf'):
            break  # todos esvaziaram

        resultado.append(menor)

        # Encontrar qual folha tinha esse valor e atualizar
        for folha in folhas:
            if folha.valor == menor:
                idx = folha.indice_particao
                if particoes[idx]:
                    folha.valor = particoes[idx].pop(0)
                else:
                    folha.valor = float('inf')  # esvaziou
                atualizarArvore(raiz, folha)
                break

    return resultado


lista = [29, 14, 76, 75, 59, 6, 7, 74, 48, 46,
10, 18, 56, 20, 26, 4, 21, 65, 22, 49,
11, 16, 8, 15, 5, 19, 50, 55, 25, 66,
57, 77, 12, 30, 17, 9, 54, 78, 43, 38,
51, 32, 58, 13, 73, 79, 27, 1, 3, 60]
selecao  = selecaoSubstituicao(lista, 6)

print(arvoreBinariaVencedores(selecao))

