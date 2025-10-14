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

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    540.0,
    281.0,
    image=image_image_1
)

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
    x=92.0,
    y=343.33331298828125,
    width=230.0,
    height=96.56117248535156
)

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
    x=740.0,
    y=343.0,
    width=230.0,
    height=96.56117248535156
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    529.0,
    279.27044677734375,
    image=image_image_2
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    855.0,
    239.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#B3A298",
    fg="#372115",
    highlightthickness=0,
    font=("LEMONMILK-Bold", 32),
)
entry_1.place(
    x=730.0,
    y=180.0,
    width=250.0,
    height=125.0
)

entry_1.tag_configure("center", justify="center")
entry_1.config(state="disabled")

label_1 = Label(
    bd=0,
    bg="#B3A298",
    fg="#372115",
    highlightthickness=0,
    font=("LEMONMILK-Bold", 32),
    text="",  # O texto começa vazio
)
label_1.place(
    x=730.0,
    y=180.0,
    width=250.0,
    height=125.0,
)

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

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: abrir_link_github(),
    relief="flat",
    activebackground="#7B6052"
)
button_4.place(
    x=790.0,
    y=430.0,
    width=136.0,
    height=57.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    540.0,
    77.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    206.0,
    249.0,
    image=image_image_5
)
texto_fantasma = Label(window, font=("LEMONMILK-Bold", 1))
window.resizable(False, False)
window.mainloop()
