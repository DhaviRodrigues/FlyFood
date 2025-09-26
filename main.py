import itertools as it
import numpy as np

class PontoEntrega:

    def __init__(self, nome_ponto, x, y):
        self.nome_ponto = nome_ponto # Representa os possíveis nomes: A,B,C,D ou R dos objetos pontos criados
        self.x = x #Distância Horizontal
        self.y = y #Distância Vertical

        """
        Representa um ponto de entrega ou o ponto inicial (R) dentro da matriz.

        Atributos:
        nome_ponto (str): Identificação do ponto (ex: A, B, C, D, R).
        x (int): Coordenada da linha na matriz.
        y (int): Coordenada da coluna na matriz.
        """

    def distanciaManhattan(self, outro_ponto):
        """
        Calcula a distância Manhattan até outro ponto.

        A distância de Manhattan:
        |x1 - x2| + |y1 - y2|, ou seja, apenas movimentos horizontais e verticais.

        Args:
            outro_ponto (PontoEntrega): Outro ponto da matriz.

        Returns:
            int: Distância de Manhattan entre este ponto e o outro.
        """
        #Garante que as linhas com pesos sejam calculadas em distância manhattan e como inteiros >= 0 e cálcula quantos passos horizontais e verticais são necessários para percorrer os caminhos
        dx = self.x - outro_ponto.x
        if dx < 0:
            dx = -dx
        dy = self.y - outro_ponto.y
        if dy < 0:
            dy = -dy
        return dx + dy

class RotasDrone:

    def __init__(self, linhas, colunas, matriz):
        """
        Inicializa o problema do drone a partir da matriz.

        Args:
            linhas (int): Número de linhas da matriz.
            colunas (int): Número de colunas da matriz.
            matriz (list[list[str]]): Matriz com pontos de entrega e ponto inicial.
        """
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = matriz
        self.pontos = self.encontrarPontos()
        self.inicio = self.pontos["R"]

    def encontrarPontos(self):
        """
        Localiza todos os pontos de interesse na matriz e os armazena em um dicionário.

        Returns:
            dict: Mapeamento {nome_ponto: PontoEntrega}.
        """
        pontos = {}
        matriz_modelada = np.array(self.matriz) # transforma a matriz em um array do numpy
        for (i,j), valor in np.ndenumerate(matriz_modelada):  # retorna pares (i,j) em cada elemento matricial
            if valor != "0":
                pontos[valor] = PontoEntrega(valor, i, j)
        return pontos

    def calcularMelhorRota(self):
        """
        Calcula a melhor rota de entregas, minimizando o custo total em distância Manhattan.

        O drone deve:
        - Sair do ponto inicial R
        - Visitar todos os pontos de entrega em alguma ordem
        - Retornar ao ponto R no final

        Returns:
            str: Sequência de pontos de entrega na ordem ótima.
        """
        pontos_entregas = [p for p in self.pontos if p != "R"]
        menor_custo = float("inf")
        melhor_rota = None

        for permut in it.permutations(pontos_entregas): #Permuta todos os possíveis caminhos dentre os pontos de entrega
            custo = 0
            atual = self.inicio #O primeiro ponto é o ponto inicial

            for p in permut:
                custo += atual.distanciaManhattan(self.pontos[p])
                atual = self.pontos[p]

            custo += atual.distanciaManhattan(self.inicio)  # retornar ao R

            if custo < menor_custo:
                menor_custo = custo
                melhor_rota = permut

        return f"{" ".join(melhor_rota)}"

with open("arquivo_matriz", "r", encoding="utf-8") as f:
    linhas_arquivo = f.read().splitlines()

linhas, colunas = map(int, linhas_arquivo[0].split())
matriz = [linha.split() for linha in linhas_arquivo[1:]]

drone = RotasDrone(linhas, colunas, matriz)
resultado = drone.calcularMelhorRota()
print(resultado)
