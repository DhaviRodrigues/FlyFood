from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label
from tkextrafont import Font
import main
import webbrowser

resultado = None

def abrir_link_github():
    """Abre o link do repositório do projeto no GitHub em uma nova aba do navegador."""
    url = "https://github.com/DhaviRodrigues/FlyFood" # Define a URL do repositório.
    webbrowser.open_new_tab(url) # Abre a URL em uma nova aba.

def armazenar_resultado(window):
    global resultado
    resultado = main.RotasDrone.selecionar_arquivo(window)

def relative_to_assets(path: str) -> Path:
    """Monta um caminho absoluto para um arquivo de asset, facilitando o acesso."""
    output_path = Path(__file__).parent  # Pega o caminho do diretório onde este script está localizado.
    assets_path = output_path / "assets" / "frame0"  # Constrói o caminho para a subpasta de assets especificada.
    return assets_path / Path(path)  # Retorna o caminho completo para o arquivo de asset final.


window = Tk() # Cria a janela principal da aplicação.
window.title("FlyFood") # Define o título da janela.
window.geometry("1080x560") # Define o tamanho fixo da janela em pixels.

icon_path = Path(__file__).parent / "assets" / "256_icon.png" # Define o caminho para o ícone da janela.

icon = PhotoImage(file=icon_path) # Carrega a imagem do ícone em um formato compatível com o Tkinter.

window.iconphoto(True,icon)# Define a imagem carregada como o ícone da janela.

window.configure(bg = "#FFFFFF")

# Este bloco 'try...except' carrega fontes customizadas de forma segura.
try:
    # Define os caminhos para os arquivos de fonte.
    font_path_light_italic = Path(__file__).parent / "fonts" / "LEMONMILK-LightItalic.otf"
    font_path_negrito = Path(__file__).parent / "fonts" / "LEMONMILK-Bold.otf"
    
    Font(file=font_path_light_italic)
    Font(file=font_path_negrito)
    
    print("Fontes carregadas com sucesso.")

except Exception as e:
    print(f"Erro ao carregar fontes: {e}. A usar fontes padrão.")
    # E define fontes do padrão do sistema para garantir que a aplicação continue funcionando.
    window.font_lemonmilk_light_italic = ("Arial", 18)
    window.font_lemonmilk_bold = ("Arial", 24, "bold")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 560,
    width = 1080,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

#fundo
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    540.0,
    281.0,
    image=image_image_1
)

#botão escolha o arquivo
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: armazenar_resultado(window),
    relief="flat",
    activebackground="#7B6052"
)
button_1.place(
    x=471.0,
    y=126.0,
    width=137.0,
    height=57.0
)

#botão gerar resultado
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: main.RotasDrone.imprimir_caminho(resultado, window, label_1),
    relief="flat",
    activebackground="#7B6052"
)
button_2.place(
    x=469.0,
    y=312.0,
    width=137.0,
    height=57.0
)

#svg arquivo
image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    539.113525390625,
    70.0,
    image=image_image_5
)

#seta
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    538.0,
    246.0,
    image=image_image_2
)

#retangulo melhor rota
image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    540.0,
    400.0,
    image=image_image_6
)

#retangulo tempo total
image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    670.0,
    475.0,
    image=image_image_7
)

#retangulo distancia total
image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    380.0,
    475.0,
    image=image_image_8
)

#Label para a melhor rota
label_1 = Label(
    bd=0,
    bg="#B3A298",
    fg="#372115",
    highlightthickness=0,
    font=("LEMONMILK-Bold", 32),
    text="",  # O texto começa vazio
)
label_1.place(
    x=150.0,
    y=374.0,
    width=780.0,
    height=46.0,
)

#Label para a distância total
label_2 = Label(
    bd=0,
    bg="#B3A298",
    fg="#372115",
    highlightthickness=0,
    font=("LEMONMILK-Bold", 32),
    text="",  # O texto começa vazio
)
label_2.place(
    x=430.0,
    y=450.0,
    width=76.0,
    height=46.0,
)

#Label para o tempo total
label_3 = Label(
    bd=0,
    bg="#B3A298",
    fg="#372115",
    highlightthickness=0,
    font=("LEMONMILK-Bold", 32),
    text="",  # O texto começa vazio
)
label_3.place(
    x=690.0,
    y=450.0,
    width=76.0,
    height=46.0,
)

#botão do github
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: abrir_link_github(),
    relief="flat",
    activebackground="#7B6052"
)
button_3.place(
    x=432.0,
    y=523.0,
    width=216.0,
    height=16.0
)

#logo flyfood
image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_3 = canvas.create_image(
    90.0,
    153.0,
    image=image_image_4
)

#texto tempo total
canvas.create_text(
    552.0,
    462.0,
    anchor="nw",
    text="tempo total:",
    fill="#372115",
    font=("LEMONMILK-Bold", 16 * -1)
)

#texto distância total
canvas.create_text(
    260.0,
    462.0,
    anchor="nw",
    text="DISTÂNCIA TOTAL:",
    fill="#372115",
    font=("LEMONMILK-Bold", 16 * -1)
)

window.resizable(False, False)
window.mainloop()
