import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess

# Função para carregar dados do banco de dados


def run_cadastrar_produto():
    subprocess.run(['python', 'cadastrar_produto.py'])

# Função para rodar o script page2.py


def run_atualizar_estoque():
    subprocess.run(['python', 'atualizar_estoque.py'])


def carregar_dados():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT produto, quantidade FROM estoque ORDER BY produto ASC")
    dados = cursor.fetchall()  # Busca todos os dados da tabela
    conn.close()
    return dados


# Criação da janela principal
root = tk.Tk()
root.title("Mostrar Estoque")
root.geometry("800x600")

# Criação da Treeview para exibir os dados
tree = ttk.Treeview(root, columns=('Produto', 'Quantidade'),
                    show='headings', height=15)
tree.heading('Produto', text='Produto')
tree.heading('Quantidade', text='Quantidade')
tree.column('Produto', anchor='center', width=200)
tree.column('Quantidade', anchor='center', width=100)
tree.pack(pady=20)

# Carrega os dados e insere na Treeview
dados = carregar_dados()
for produto, quantidade in dados:
    tree.insert('', tk.END, values=(produto, quantidade))

# Botões
btn_cadastrar_produto = tk.Button(
    root, text='Cadastar Produto', command=run_cadastrar_produto, width=20, font=('Arial', 12))
btn_cadastrar_produto.pack(pady=10)

btn_atualizar_estoque = tk.Button(
    root, text='Atualizar Estoque', command=run_atualizar_estoque, width=20, font=('Arial', 12))
btn_atualizar_estoque.pack(pady=10)

btn_voltar = tk.Button(root, text="Voltar",
                       command=root.quit, width=20, font=('Arial', 12))
btn_voltar.pack(pady=10)

# Execução do loop principal da janela
root.mainloop()
