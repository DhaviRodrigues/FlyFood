import itertools as it
from tkinter import Label, PhotoImage, Toplevel, Button, Frame, filedialog
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

        return f"{' '.join(melhor_rota)}"
    

    def leitura_da_matriz(arquivo_matriz, window):
        if arquivo_matriz is None:
            GuiTools.custom_messagebox(window, "Erro na seleção de arquivo", "Nenhum arquivo foi selecionado. Por favor, selecione um arquivo válido.")
        else:

            with open(arquivo_matriz, "r", encoding="utf-8") as f:
                linhas_arquivo = f.read().splitlines()

            linhas, colunas = map(int, linhas_arquivo[0].split())
            matriz = [linha.split() for linha in linhas_arquivo[1:]]

            drone = RotasDrone(linhas, colunas, matriz)
            resultado = drone.calcularMelhorRota()
            print(resultado)

class GuiTools:
    def selecionar_arquivo():
    #Abre uma janela para o usuário selecionar um arquivo de arquivo txt.
        arquivo_matriz = None
        arquivo_matriz = filedialog.askopenfilename( # Abre a janela de seleção de arquivo.
            title="Selecione o caminho",
            filetypes=[("Ficheiros de Texto", "*.txt")] #Exemplo "*.txt"
        )

        if not arquivo_matriz: # Se o usuário cancelar a seleção, a função termina.
            return
        else:
            return arquivo_matriz
        
    def custom_messagebox(master,titulo, mensagem):
        """Exibe uma caixa de diálogo modal com mensagem e botão "OK".
        
        Exemplo dos parâmetros:
        master: SEMPRE será a variável window
        titulo: "Erro na seleção de arquivo"
        mensagem: "O Arquivo selecionado não é compatível com o programa, selecione outro formato."
        """

        dialog = Toplevel(master)  # Cria uma nova janela (Toplevel) que pertence à janela 'master'.
        dialog.title(titulo)  # Define o texto da barra de título.
        dialog.configure(bg="#EADFC8")  # Define a cor de fundo da janela.
        dialog.resizable(False, False)  # Impede que o usuário redimensione a caixa de diálogo.

        dialog.update_idletasks()  # Força o Tkinter a renderizar a janela para que suas dimensões sejam conhecidas.
        
        width = 400  # Define a largura fixa da caixa.
        height = 200  # Define a altura fixa da caixa.
        x = master.winfo_x() + (master.winfo_width() - width) // 2  # Calcula a coordenada X para centralizar a caixa.
        y = master.winfo_y() + (master.winfo_height() - height) // 2  # Calcula a coordenada Y para centralizar a caixa.
        dialog.geometry(f'{width}x{height}+{x}+{y}')  # Aplica o tamanho e a posição calculados.

        label = Label(
            dialog,
            text=mensagem,  # O texto a ser exibido.
            font=("Lemon Milk Negrito", 12),  # A fonte do texto.
            fg="#7B6052",  # A cor do texto.
            bg="#EADFC8",  # A cor de fundo do label.
            wraplength=350,  # Quebra a linha do texto após 350 pixels.
            justify='center'  # Centraliza o texto com quebra de linha.
        )

        label.pack(
            pady=(20, 10),  # Adiciona espaçamento vertical (20 em cima, 10 embaixo).
            padx=10  # Adiciona espaçamento horizontal.
        )

        ok_button = Button( # Cria um botão "OK" na caixa de diálogo.
            dialog,
            text="OK",  # O texto do botão.
            font=("Lemon Milk Negrito", 12),  # A fonte do botão.
            bg="#7B6052",  # A cor de fundo do botão.
            fg="#B3A298",  # A cor do texto do botão.
            borderwidth=0,  # A largura da borda.
            relief="raised",  # O estilo de relevo do botão.
            padx=10,
            pady=3,
            width=6,  # A largura do botão.
            command=dialog.destroy  # Define que o comando do botão é fechar a própria caixa.
        )

        ok_button.pack(
            pady=15  # Adiciona espaçamento vertical.
        )
        
        dialog.transient(master)  # Associa a caixa à janela mestre (exemplo minimiza junto).
        dialog.grab_set()  # Torna a caixa de diálogo modal (bloqueia a janela de trás).
        dialog.wait_window()  # Pausa o código aqui até que a 'dialog' seja fechada.
