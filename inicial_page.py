import tkinter as tk
import subprocess

# Funções


def run_mostrar_ingredientes():
    subprocess.run(['python', 'mostrar_ingredientes.py'])


def run_cadastrar_receita():
    subprocess.run(['python', 'cadastrar_receita.py'])


def run_relatorio():
    subprocess.run(['python', 'relatorio.py'])


def run_mostrar_estoque():
    subprocess.run(['python', 'mostrar_estoque.py'])

# Função estilo do botão ao passar o mouse


def on_enter(event):
    event.widget['background'] = 'white'
    event.widget['font'] = ('Arial', 12, 'bold')

# Função para restaurar o estilo original quando o mouse sair do botão


def on_leave(event):
    event.widget['background'] = 'gray'
    event.widget['font'] = ('Arial', 12)


# Função para criar botões e aplicar o efeito hover


def create_button(text, command, row, column):
    btn = tk.Button(root, text=text, command=command, width=20,
                    height=2, font=('Arial', 12), bg="grey", fg="white")
    btn.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    return btn


# Criação da Interface Gráfica
root = tk.Tk()
root.title("Menu de Páginas")
root.geometry("800x600")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)


# Criação dos botões
create_button("Estoque", run_mostrar_estoque, 0, 1)
create_button("cadastrar novas receitas", run_cadastrar_receita, 1, 1)
create_button("Receitas", run_mostrar_ingredientes, 2, 1)
create_button("Relatório de Consumo", run_relatorio, 3, 1)
create_button("Fechar", root.quit, 4, 1)  # Botão para fechar o programa

# Loop
root.mainloop()
