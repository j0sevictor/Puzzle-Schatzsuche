from z3 import And, Or, Implies, Bool, Not, Solver
from itertools import combinations

# PUZZLE: 23 - Schatzsuche

# Campo de Diamantes: especificamente esse caso deve gerar uma saída satisfatível
'''bord = [
    [-1, -1, -1, -1, -1, -1,  2, -1, -1,  2],
    [ 2,  2,  2, -1, -1,  2,  2, -1, -1,  2],
    [-1,  0, -1, -1,  1, -1,  3,  4,  5, -1],
    [-1, -1, -1, -1,  2, -1, -1, -1, -1, -1],
    [-1, -1,  1, -1, -1, -1, -1, -1, -1, -1],
    [-1,  1, -1,  2, -1, -1,  3, -1, -1,  0],
    [-1,  1, -1, -1,  1,  3, -1, -1,  0, -1],
    [-1, -1,  1, -1, -1,  4, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1,  5, -1, -1,  0, -1],
    [-1,  0,  2, -1, -1,  3, -1,  1, -1, -1],
]'''
bord = [
    [-1,  1, -1, -1, -1],
    [-1, -1,  3,  3, -1],
    [ 3, -1,  4,  2, -1],
    [-1, -1, -1, -1,  0],
    [-1,  2, -1, -1, -1]
]

# Criando uma matriz de mesmo tamanho de 'bord', em que cada entrada é uma variável proposicional
listaProps = [ [ Bool('d' + str(i) + str(j)) for j in range(len(bord[i]))] for i in range(len(bord))]

# Coloca números naturais correspondentes do 'bord' no lugar das variáveis proposicionais 
for i in range(len(bord)):
    for j in range(len(bord[i])):
        if bord[i][j] != -1:
            listaProps[i][j] = bord[i][j]

formulas = []
for i in range(len(listaProps)):
    for j in range(len(listaProps[i])):

        if type(listaProps[i][j]) == int:
            # Faz a leitura das variáveis proposicionais ao redor do número achado e as armazena em "propFixas"
            propFixas = []
            for k in range(i - 1, i +  2):
                for h in range(j - 1, j + 2):
                    if 0 <= k < len(listaProps):
                        if 0 <= h < len(listaProps[i]):
                            if type(listaProps[k][h]) != int:
                                propFixas.append(listaProps[k][h])

            # Calcula todas as combinações possíveis de diamantes relativo ao número achado e as células disponíveis
            combinacoes = combinations(propFixas, listaProps[i][j])

            # Iterando sobre as combinações para criar as fómulas proposicionais 'phi'
            phi = []
            # 'psi' representa todas as possibilidades encadeadas com o conectivo Or
            psi = []
            for t in combinacoes:
                # Defina uma possibilidades de posição para os diamantes
                pre = list(t)

                # Faz a negação das posições em que o diamante não está
                conclusao = []
                for var in propFixas:
                    if var not in pre:
                        conclusao.append(Not(var))
                conclusao = And(conclusao)

                # Se os diamantes estão na posição pre, então eles n estrão nas outras posições
                if len(pre) == 0:
                    phi.append(conclusao)
                elif len(pre) == 1:
                    phi.append(Implies(pre[0], conclusao))
                    psi.append(pre[0])
                else:
                    phi.append(Implies(And(pre), conclusao))
                    psi.append(And(pre))
            
            formulas.append(Or(phi))
            # Uma das possibilidades de escolha da posição dos diamantes tem que ser verdade
            if len(psi) > 0: formulas.append(Or(psi))

            if len(psi) > 1:
                # Como todas as possibilidades de 'psi' estão encadeadas com Or inclusivo, falta definir que só um deles pode ser verdade
                posicao1 = 0
                for precedente in psi:
                    conclusao = []
                    posicao2 = 0
                    for formula in psi[:]:
                        if posicao1 != posicao2:
                            conclusao.append(Not(formula))
                        posicao2 += 1
                    conclusao = And(conclusao)
                    formulas.append(Implies(precedente, conclusao))
                    posicao1 += 1


gama = And(formulas)

s = Solver()
s.add(gama)
print(s.check())
sol = s.model().sexpr()

for string in sol.split(')\n'):
    linha = True
    i_linha = -1
    j_coluna = -1
    for sub in string:
        if sub.isnumeric() and linha:
            i_linha = int(sub)
            linha = False
        elif sub.isnumeric():
            j_coluna = int(sub)
            break
    
    if 'true' in string:
        bord[i_linha][j_coluna] = 'D'


for i in range(len(bord)):
    for j in range(len(bord[i])):
        if type(bord[i][j]) == int:
            if bord[i][j] < 0:
                print('|   ', end='')
            else:
                print('| \033[1;32m{}\033[m '.format(bord[i][j]), end='')
        else:
            print('| \033[1;34mD\033[m ', end='')
    print('|')
    print('-' * (5 * j + 1))
    

'''solucaoLista = solucao.decls()
print(solucaoLista[1].__ne__)'''
'''
for item in solucao:
    if (solucao[item]):
        print(item)
'''

