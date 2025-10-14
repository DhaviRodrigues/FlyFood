<div align="center">

## FlyFood

### Projeto Interdisciplinar – Sistemas de Informação II  
**Universidade Federal Rural de Pernambuco (UFRPE)** • 2025.2


## Sobre o Projeto

O **FlyFood** é uma aplicação acadêmica desenvolvida para **gerar soluções de caminhos satisfatórios** a partir de uma **matriz de entrada**.  
A ideia central é simular o planejamento de rotas para entregas aéreas (como drones), aplicando **algoritmos de busca e otimização** para encontrar o trajeto mais eficiente.

Este projeto integra conhecimentos de **estrutura de dados**, **algoritmos heurísticos** e **interface gráfica em Python**.

---

</div>

## Funcionalidades

- Leitura de arquivos de entrada `.txt` ou `.xxx` contendo a matriz de dados.  
- Identificação automática de **origem e destino**.  
- Geração e exibição de caminhos válidos.  
- Cálculo de custo total e distância percorrida.  
- Interface gráfica em **Tkinter** para visualização.  
- Comparação entre diferentes algoritmos de busca.

---

## Biblotecas Necessárias

- TkExtraFont
- pathlib 
- webbrowser
- itertools
- numpy
- Tkinter

## 🗂️ Estrutura do Projeto

```text
FlyFood/
│
├── assets/               # Imagens e ícones usados pela interface
├── fonts/                # Fontes personalizadas
├── .vscode/             
│
├── gui.py                # Interface gráfica principal
├── main.py               # Funções de Busca
├── requisitos.txt        # Lista de dependências
└── README.md
