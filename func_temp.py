from tkinter import Label, PhotoImage, Toplevel, Button, Frame

def custom_messagebox(master,titulo, mensagem):
    """Exibe uma caixa de diálogo modal com mensagem e botão "OK"."""
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
        font=("Poppins", 12),  # A fonte do texto.
        fg="#45312C",  # A cor do texto.
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
        font=("Poppins Black", 12),  # A fonte do botão.
        bg="#45312C",  # A cor de fundo do botão.
        fg="#EADFC8",  # A cor do texto do botão.
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