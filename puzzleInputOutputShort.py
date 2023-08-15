from z3 import And, Or, Implies, Bool, Not, Solver, sat
from itertools import combinations
from os import system

# PUZZLE: 23 - Schatzsuche

def main():

    # Dimensões do bord
    numLinhas = lerNumNatura("Quantas linhas tem o tabuleiro? ")
    numColunas = lerNumNatura("Quantas colunas tem o tabuleiro? ")

    if numLinhas > 10 or numColunas > 10: return print('\nNão ¯\_(ツ)_/¯')

    # Campo de Diamantes: este código pede ao usuário entradas válida para preencher o tabuleiro
    bord = list()
    for i in range(numLinhas):
        bord.append(list())
        for j in range(numColunas):
            system('cls')

            printBord(bord)
            num = lerNumNatura(f'Digite um valor para ({i + 1}, {j + 1}): ', nadaMenosUm=True)
            bord[i].append(num)

    system('cls')
    printBord(bord)


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

                # 'phi' representas as fómulas para o caso do número achado ser 0
                phi = []
                # 'psi' representa todas as possibilidades encadeadas com o conectivo Or
                psi = []
                for t in combinacoes:
                    # 'comp' representa uma combinação possível das céluas vazias
                    comb = list(t)

                    if len(comb) == 0:
                        # Faz a negação das posições em volta do número 0
                        for var in propFixas:
                            phi.append(Not(var))
                    else:
                        psi.append(And(comb))
                
                formulas.append(And(phi))
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

    # Checando a satisfatibilidade do conjunto de fórmulas criadas
    if s.check() == sat:
        print('Satisfatível')
    else:
        print('Insatisfatível')
        return

    sol = s.model().sexpr()
    # Subtituir as posições nas quais as variáveis do modelo são Verdade pela letra 'D'
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

    printBord(bord)

def lerNumNatura(message: str, nadaMenosUm = False):
    while True:
        num = str(input(message))
        if num.isnumeric():
            num = int(num)
            break
        elif nadaMenosUm and num == '':
            num = -1
            break
        else:
            print("Digite um número natural!")
    return num

def printBord(bord: list[list]):
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
        print('-' * (4 * len(bord[i]) + 1))

if __name__ == '__main__':
    main()
