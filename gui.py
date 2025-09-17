from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


def relative_to_assets(path: str) -> Path:
    """Monta um caminho absoluto para um arquivo de asset, facilitando o acesso."""
    output_path = Path(__file__).parent  # Pega o caminho do diretório onde este script está localizado.
    assets_path = output_path / "assets" / "frame0"  # Constrói o caminho para a subpasta de assets especificada.
    return assets_path / Path(path)  # Retorna o caminho completo para o arquivo de asset final.


window = Tk() # Cria a janela principal da aplicação.
window.title("FlyFood") # Define o título da janela.
window.geometry("720x350") # Define o tamanho fixo da janela em pixels.

icon_path = Path(__file__).parent / "assets" / "256_icon.png" # Define o caminho para o ícone da janela.

icon = PhotoImage(file=icon_path) # Carrega a imagem do ícone em um formato compatível com o Tkinter.

window.iconphoto(True,icon)# Define a imagem carregada como o ícone da janela.

window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 350,
    width = 720,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    360.0,
    175.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=103.0,
    y=226.0,
    width=150.0,
    height=62.97467803955078
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=491.0,
    y=226.0,
    width=150.0,
    height=62.97467803955078
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    360.0,
    188.0,
    image=image_image_2
)

#image_image_3 = PhotoImage(
#    file=relative_to_assets("image_3.png"))
#image_3 = canvas.create_image(
#    109.0,
#    43.0,
#    image=image_image_3
#)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    565.0,
    163.0,
    image=image_image_4
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    565.5,
    163.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=484.0,
    y=114.0,
    width=163.0,
    height=97.0
)

#image_image_5 = PhotoImage(
#    file=relative_to_assets("image_5.png"))
#image_5 = canvas.create_image(
#    55.0,
#    43.0,
#    image=image_image_5
#)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=260.0,
    y=322.0,
    width=199.0,
    height=16.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    360.0,
    67.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    178.0,
    165.0,
    image=image_image_7
)
window.resizable(False, False)
window.mainloop()
