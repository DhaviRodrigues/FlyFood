from tkinter import Label, PhotoImage, Toplevel, Button, Frame, filedialog

def selecionar_arquivo():
    
    """Abre uma janela para o usuário selecionar um arquivo de imagem e exibe um preview na tela."""
    matriz = None
    matriz = filedialog.askopenfilename( # Abre a janela de seleção de arquivo.
        title="Selecione o caminho",
        filetypes=[("Ficheiros de Imagem", "*.txt")] #Exemplo "*.txt"
    )

    if not matriz: # Se o usuário cancelar a seleção, a função termina.
        return
    else:
        return matriz
    
def custom_messagebox(master,titulo, mensagem):
    """Exibe uma caixa de diálogo modal com mensagem e botão "OK".
    
    Exemplo dos parâmetros:
    master: SEMPRE será a variável window
    titulo: Erro na seleção de arquivo
    mensagem: O Arquivo selecionado não é compatível com o programa, selecione outro formato."""

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
        bg="#B3A298",  # A cor de fundo do label.
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