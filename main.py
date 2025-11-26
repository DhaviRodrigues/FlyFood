import itertools as it
from tkinter import Label, PhotoImage, Toplevel, Button, Frame, filedialog
import random
import time
import matplotlib.pyplot as plt

class LeituraTsp:
    def __init__(self, num_cidades, arquivo_tsp):
        """
        Inicializa o leitor do arquivo TSP.

        Parâmetros:
            num_cidades (int): Quantidade de cidades a serem lidas.
            arquivo (str): Arquivo TSP.

        Atributos:
            valores_linhas (list[list[int]]): Linhas do formato triangular superior.
            distancias (dict): Dicionário {(i,j): custo} simétrico.
        """
        self.n = num_cidades
        self.valores_linhas, self.distancias = self.lerArquivoTsp(arquivo_tsp)

    def lerArquivoTsp(self, arquivo_tsp):
        """
        Lê um arquivo TSP no formato UPPER_ROW (apenas números).

        Retorna:
            tuple:
                - valores_linhas (list[list[int]]): Linhas do arquivo representando
                  os valores acima da diagonal principal.
                - distancias (dict): Dicionário contendo a matriz de distâncias
                  completa no formato {(i, j): valor}.
        """

        with open(arquivo_tsp, "r") as f:
            espacos = f.read().split()

        numeros = [int(elemento) for elemento in espacos] #Converte cada elemento string da matriz em inteiro
        # calcula quantos números deveriam existir para uma matriz triangular superior n x n
        numeros_esperados = self.n * (self.n - 1) // 2
        if len(numeros) < numeros_esperados:
            raise ValueError("Arquivo tem menos números que o esperado.")

        valores_linhas = [] # lista que conterá cada linha do triângulo superior (lista de listas)
        idx = 0
                

        for i in range(self.n): # para cada linha i do triângulo superior (i = 0 .. n-1)
            tam = self.n - i - 1
            linha = numeros[idx: idx + tam] # extrai a fatia correspondente à linha i para cada linha da matriz
            valores_linhas.append(linha) # adiciona a linha à lista de linhas
            idx += tam #Incrementa o indice para avançar para as outras fatias de linha

        distancias = {} #Dicionário completo com as distâncias, incluindo as simétricas
        # percorre cada linha construída e preenche distancias[(i,j)] e distancias[(j,i)] que seria a distância simétrica
        for i in range(self.n):
            # distância da cidade para ela mesma = 0
            distancias[(i, i)] = 0
            for k, val in enumerate(valores_linhas[i]):
                j = i + 1 + k
                distancias[(i, j)] = val # preenche a distância (i,j)
                distancias[(j, i)] = val # Distância simétrica

        return valores_linhas, distancias

class AlgoritmoGenetico:
    def __init__(self, dados_matriz: LeituraTsp,
                 tamanho_populacao=120,
                 geracoes=30000,
                 taxa_mutacao=0.1,
                 elitismo=True,
                 torneio_k=3):
        """
        Inicializa um algoritmo genético configurado para resolver o TSP.

        Parâmetros:
            dados_matriz (LeituraTsp): Objeto contendo matriz de distâncias.
            tamanho_populacao (int): Quantidade de indivíduos na população.
            geracoes (int): Número de gerações.
            taxa_mutacao (float): Probabilidade de mutação.
            elitismo (bool): Se True, preserva o melhor_individuo de cada geração.
            torneio_k (int): Número de competidores na seleção por torneio.
        """
        self.dist = dados_matriz.distancias # dicionário {(i,j): custo}
        self.n = dados_matriz.n # número de cidades

        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao
        self.elitismo = elitismo
        self.torneio_k = torneio_k

    def calcularCusto(self, perm):
        """
        Calcula o custo total de um percurso TSP fechado.

        Parâmetros:
            perm (list[int]): Permutação representando uma solução TSP.

        Retorna:
            int: Custo total do caminho.
        """
        total = 0
        # soma os custos entre pares de cidades consecutivas
        for i in range(len(perm) - 1):
            # adiciona o custo do último para o primeiro (fechamento do ciclo)
            total += self.dist[(perm[i], perm[i+1])]
        total += self.dist[(perm[-1], perm[0])]
        return total

    def calcularFitness(self, individuo): #Quanto menor o custo, então maior será o fitness
        """
        Calcula o fitness do indivíduo como 1 / (1 + custo).

        Parâmetros:
            individuo (list[int]): Permutação representando uma solução.

        Retorna:
            float: Fitness (quanto maior, melhor_individuo).
        """
        return 1.0 / (1.0 + self.calcularCusto(individuo))

    def inicializarPopulacao(self):
        """
        Cria a população inicial embaralhando permutações das cidades.

        Retorna:
            list[list[int]]: População inicial com indivíduos aleatórios.
        """
        cidades = list(range(self.n))
        populacao = []
        for _ in range(self.tamanho_populacao):
            individuo = cidades[:] #copia a lista de cidades
            random.shuffle(individuo) # embaralha para criar uma permutação
            populacao.append(individuo) # adiciona à população
        return populacao

    def selecaoTorneio(self, populacao):
        """
        Seleciona um indivíduo por torneio.

        Parâmetros:
            populacao (list[list[int]]): População atual.

        Retorna:
            list[int]: Indivíduo vencedor do torneio.
        """
        # escolhe K competidores distintos da população
        competidores = random.sample(populacao, self.torneio_k)
        # calculamos (fitness, individuo) para cada e pegamos o maior pela tupla
        return max((self.calcularFitness(ind), ind) for ind in competidores)[1]

    def crossoverOx(self, p1, p2):
        """
        Aplica o operador de crossover OX (Order Crossover).

        Parâmetros:
            p1 (list[int]): Pai 1.
            p2 (list[int]): Pai 2.

        Retorna:
            list[int]: Novo indivíduo gerado pelo crossover.
        """
        n = len(p1)

        a, b = sorted(random.sample(range(n), 2)) # sorteia dois índices e os ordena para obter o segmento contínuo

        filho = [None] * n   # cria o filho com posições vazias (None)


        for i in range(a, b + 1):
            filho[i] = p1[i]

        idx = (b + 1) % n # posição de inserção no filho (a seguir ao segmento copiado)

        for gene in p2[b + 1:] + p2[:b + 1]: # percorre os genes do pai2 a partir de b+1 (circular)
            if gene not in filho:
                filho[idx] = gene
                idx = (idx + 1) % n

        return filho

    def mutacaoSwap(self, individuo):
        """
        Aplica mutação do tipo swap entre duas posições do indivíduo.

        Parâmetros:
            individuo (list[int]): Indivíduo a ser mutado.

        Retorna:
            list[int]: Indivíduo possivelmente mutado.
        """
        if random.random() < self.taxa_mutacao:
            i, j = random.sample(range(len(individuo)), 2)
            individuo[i], individuo[j] = individuo[j], individuo[i]
        return individuo

    def executarAg(self):
        """
        Executa o Algoritmo Genético completo:
        - Inicializa população
        - Faz seleção por torneio
        - Aplica crossover OX
        - Aplica mutação swap
        - Mantém elitismo
        - Atualiza o melhor indivíduo

        Retorna:
            tuple:
                melhor_individuo (list[int]): Melhor rota encontrada.
                melhor_custo (int): Custo da melhor rota.
        """
        populacao = self.inicializarPopulacao()

        melhor_individuo = min(
                                ((self.calcularCusto(individuo), individuo) for individuo in populacao))[1]
        melhor_custo = self.calcularCusto(melhor_individuo)

        historico_custo= []

        for g in range(1, self.geracoes + 1):

            nova = []

            if self.elitismo: # se elitismo ativado, preserva o melhor indivíduo da geração anterior
                nova.append(melhor_individuo[:])

            while len(nova) < self.tamanho_populacao:    # gera filhos até completar o tamanho da população


                # seleciona dois pais via torneio
                p1 = self.selecaoTorneio(populacao)
                p2 = self.selecaoTorneio(populacao)
                #Realiza o cruzamento
                filho1 = self.crossoverOx(p1, p2)
                filho2 = self.crossoverOx(p2, p1)
                #aplica mutação swap no filho
                filho1 = self.mutacaoSwap(filho1)
                filho2 = self.mutacaoSwap(filho2)
                # adiciona filho à nova população
                #nova.append(filho1)
                #nova.append(filho2)

                if random.random() <= 0.9:      # 90% de chance
                    filho1 = self.mutacaoSwap(filho1)
                    filho2 = self.mutacaoSwap(filho2)
                    nova.append(filho1)    # entra o filho mutado
                    nova.append(filho2)
                else:
                    nova.append(p1[:])  # entra o pai como sobrevivente
                    nova.append(p2[:])                
            
            populacao = nova

            candidato = min((self.calcularCusto(ind), ind) for ind in populacao)[1] #Encontra o candidato(melhor indivíduo da nova geração)
            custo_cand = self.calcularCusto(candidato)

            if custo_cand < melhor_custo:
                melhor_individuo = candidato[:]
                melhor_custo = custo_cand
            historico_custo.append(melhor_custo)


        return melhor_individuo, melhor_custo, historico_custo

    def selecionar_arquivo(window):
    #Abre uma janela para o usuário selecionar um arquivo de arquivo tsp.
        arquivo = None
        arquivo = filedialog.askopenfilename( # Abre a janela de seleção de arquivo.
            title="Selecione o caminho",
            filetypes=[("Ficheiros de Texto", "*.tsp")] #Exemplo "*.tsp"
        )

        if not arquivo: # Se o usuário cancelar a seleção, a função termina.
            return None, None, None

        GuiTools.custom_messagebox(window, "Arquivo Carregado",'Arquivo carregado. Selecione "Gerar Caminho" para iniciar o cálculo.')

        return arquivo
    
    def gerar_caminho(window, arquivo, melhor_individuo, calcular_Custo, tempo_total, label_rota, label_custo, label_tempo):
        melhor_individuo, calcular_Custo, tempo_total, historico_calculo = AlgoritmoGenetico.calcular_caminho(window, arquivo, label_rota)

        AlgoritmoGenetico.imprimir_caminho(window, melhor_individuo, calcular_Custo, tempo_total, label_rota, label_custo, label_tempo)

        return melhor_individuo, calcular_Custo, tempo_total, historico_calculo
        
    def calcular_caminho(window, arquivo, label_rota):
        label_rota.config(text="CALCULANDO CAMINHO...", font=("LEMONMILK-Bold", 18))
        GuiTools.custom_messagebox(window, "Calculando Rota", "O cálculo da melhor rota pode levar alguns segundos. Por favor, aguarde.")
        
        inicio=time.time()

        tsp=LeituraTsp(num_cidades=58, arquivo_tsp = arquivo)
        ag = AlgoritmoGenetico(tsp,
                          tamanho_populacao=120,
                          geracoes=8000,
                          taxa_mutacao=0.31,
                          elitismo=True,
                          torneio_k=3)

        melhor_individuo, calcularCusto, historico_custo = ag.executarAg()

        fim=time.time()
        tempo=(fim-inicio)
        tempo_total=f"{tempo:.2f}s"

        if melhor_individuo:
            return melhor_individuo, calcularCusto, tempo_total, historico_custo
        
        GuiTools.custom_messagebox(window, "Erro na seleção de arquivo", "Nenhum arquivo foi selecionado. Por favor, selecione um arquivo válido.")


    def imprimir_caminho(window, melhor_individuo, calcular_Custo, tempo_total, label_rota, label_custo, label_tempo):
        print(melhor_individuo)

        label_rota.config(text=melhor_individuo, font=("LEMONMILK-Bold", 14))
        label_custo.config(text=calcular_Custo, font=("LEMONMILK-Bold", 12))
        label_tempo.config(text=tempo_total, font=("LEMONMILK-Bold", 12))
    
class GuiTools:
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
        height = 170  # Define a altura fixa da caixa.
        x = master.winfo_x() + (master.winfo_width() - width) // 2  # Calcula a coordenada X para centralizar a caixa.
        y = master.winfo_y() + (master.winfo_height() - height) // 2  # Calcula a coordenada Y para centralizar a caixa.
        dialog.geometry(f'{width}x{height}+{x}+{y}')  # Aplica o tamanho e a posição calculados.

        label = Label(
            dialog,
            text=mensagem,  # O texto a ser exibido.
            font=("LEMONMILK-Bold", 11),  # A fonte do texto.
            fg="#372115",  # A cor do texto.
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
            font=("LEMONMILK-Bold", 12),  # A fonte do botão.
            bg="#372115",  # A cor de fundo do botão.
            fg="#B3A298",  # A cor do texto do botão.
            borderwidth=0,  # A largura da borda.
            relief="raised",  # O estilo de relevo do botão.
            padx=10,
            pady=6,
            width=3,  # A largura do botão.
            command=dialog.destroy  # Define que o comando do botão é fechar a própria caixa.
        )

        ok_button.pack(
            pady=15  # Adiciona espaçamento vertical.
        )
        
        dialog.transient(master)  # Associa a caixa à janela mestre (exemplo minimiza junto).
        dialog.grab_set()  # Torna a caixa de diálogo modal (bloqueia a janela de trás).
        dialog.wait_window()  # Pausa o código aqui até que a 'dialog' seja fechada.

    def sim_ou_nao(dialog, resultado):
        """
        Função auxiliar que define o resultado e fecha a janela.
        """
        dialog.result = resultado  # Atribui o resultado a um atributo da janela de diálogo.
        dialog.destroy()  # Fecha a janela de diálogo.

    def custom_yn(master, titulo, mensagem):
        """
        Cria uma caixa de diálogo Sim/Não, para confirmar decisões importantes do usuário.
        """
        dialog = Toplevel(master)  # Cria a janela de diálogo.
        dialog.title(titulo)  # Define seu título.
        dialog.configure(bg="#EADFC8")  # Define sua cor de fundo.
        dialog.resizable(False, False)  # Impede seu redimensionamento.

        dialog.result = False  # Define um resultado padrão (será alterado se "Sim" for clicado).

        dialog.update_idletasks()  # Força a renderização para obter as dimensões corretas.
        
        width = 400  # Largura fixa.
        height = 150  # Altura inicial.
        x = master.winfo_x() + (master.winfo_width() - width) // 2  # Calcula a posição X.
        y = master.winfo_y() + (master.winfo_height() - height) // 2  # Calcula a posição Y.
        dialog.geometry(f'{width}x{height}+{x}+{y}')  # Aplica a geometria inicial.

        label = Label(
            dialog,
            text=mensagem,  # O texto a ser exibido.
            font=("LEMONMILK-Bold", 11),  # A fonte do texto.
            fg="#372115",  # A cor do texto.
            bg="#EADFC8",  # A cor de fundo do label.
            wraplength=350,  # Quebra a linha do texto após 350 pixels.
            justify='center'  # Centraliza o texto com quebra de linha.
        )

        label.pack(pady=(20, 10), padx=20, expand=True, fill='both')  # Adiciona o label.

        button_frame = Frame(dialog, bg="#EADFC8")  # Cria um Frame para agrupar os botões horizontalmente.
        button_frame.pack(pady=(0, 20))  # Adiciona o frame à janela.

        sim_button = Button(
            button_frame,
            text="Sim", # Define o texto do botão "Sim".
            font=("LEMONMILK-Bold", 12),  # A fonte do botão.
            bg="#372115",  # A cor de fundo do botão.
            fg="#B3A298",  # A cor do texto do botão.
            borderwidth=0,  # A largura da borda.
            relief="raised",  # O estilo de relevo do botão.
            padx=10,
            pady=6,
            width=3,
            command=lambda: GuiTools.sim_ou_nao(dialog, True)  # Ao clicar, chama a função auxiliar com o resultado True.
        )

        sim_button.pack(side='left', padx=(0, 15))  # Posiciona o botão à esquerda dentro do frame.

        nao_button = Button(
            button_frame,
            text="Não", # Define o texto do botão "Não".
            font=("LEMONMILK-Bold", 12),  # A fonte do botão.
            bg="#372115",  # A cor de fundo do botão.
            fg="#B3A298",  # A cor do texto do botão.
            borderwidth=0,  # A largura da borda.
            relief="raised",  # O estilo de relevo do botão.
            padx=10,
            pady=6,
            width=3,
            command=lambda: GuiTools.sim_ou_nao(dialog, False)  # Ao clicar, chama a função auxiliar com o resultado False.
        )
        nao_button.pack(side='left')  # Posiciona o botão à esquerda, ao lado do botão "Sim".

        width = 400  # Define a largura novamente para o cálculo final.
        height = dialog.winfo_reqheight()  # Pega a altura mínima requerida pelos widgets para um ajuste perfeito.
        
        x = master.winfo_x() + (master.winfo_width() - width) // 2  # Recalcula a posição X.
        y = master.winfo_y() + (master.winfo_height() - height) // 2  # Recalcula a posição Y com a nova altura.
        
        dialog.geometry(f'{width}x{height}+{x}+{y}')  # Aplica a nova geometria com a altura ajustada.
        
        dialog.transient(master)  # Associa a caixa à janela mestre.
        dialog.grab_set()  # Bloqueia a janela de trás.
        master.wait_window(dialog)  # Pausa a janela mestre até que esta seja fechada.
        
        return dialog.result  # Retorna o resultado (True ou False) que foi definido.
    
    def tamanho_caminho(resultado):
        tamanho = 32
        if resultado:
            resultado_sem_espacos = resultado.replace(" ", "")
            comprimento = len(resultado_sem_espacos)
            if comprimento <= 5:
                tamanho = 32
            elif 5 < comprimento <= 8:
                tamanho = 20
            elif 8 < comprimento <= 12:
                tamanho = 12
            elif comprimento > 12:
                tamanho = 8
        return tamanho

    def gerar_grafico(historico_custos):
        y = historico_custos
        x = [i + 1 for i in range(len(historico_custos))]
        plt.figure(figsize=(10, 5))

        plt.plot(x, y, color='blue', linewidth=2)
        
        plt.title('Evolução do Custo por Geração')
        plt.xlabel('Geração')
        plt.ylabel('Custo (Distância Total)')
        plt.grid(True)
        plt.show()

    def mostrar_grafico(window, arquivo, melhor_individuo, historico_custos):
        if historico_custos:
            GuiTools.gerar_grafico(historico_custos)
        else:
            GuiTools.custom_messagebox(window, "Erro", "Nenhum histórico disponível.")

if __name__ == "__main__":
    caminho = "edgesBrasil58.tsp"
    num_cidades = 58 # Número de cidades da intância

    tsp = LeituraTsp(caminho, num_cidades)
    ag = AlgoritmoGenetico(tsp,
                            tamanho_populacao=120,
                            geracoes=200,
                            taxa_mutacao=0.1,
                            elitismo=True,
                            torneio_k=3)

    melhor_individuo, calcularCusto = ag.executarAg()