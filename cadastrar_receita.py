import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para criar as tabelas caso não existam


def criar_tabelas():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_receita INTEGER,
            produto TEXT NOT NULL,
            quantidade REAL,
            FOREIGN KEY (id_receita) REFERENCES receitas(id)
        )
    ''')
    conn.commit()
    conn.close()

# Função para carregar produtos da tabela estoque


def carregar_produtos():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute("SELECT produto FROM estoque")
    produtos = cursor.fetchall()
    conn.close()
    return [produto[0] for produto in produtos]

# Função para adicionar campos dinamicamente para ingredientes


def adicionar_ingrediente():
    # Ajusta a linha para incluir espaço para os campos anteriores
    row = len(ingredientes_widgets) + 3
    combo_produto = ttk.Combobox(root, values=produtos, width=30)
    combo_produto.grid(row=row, column=0, padx=10, pady=5)
    entry_quantidade = tk.Entry(root, width=10)
    entry_quantidade.grid(row=row, column=1, padx=10, pady=5)
    ingredientes_widgets.append((combo_produto, entry_quantidade))

# Função para salvar a receita e os ingredientes


def salvar_receita():
    nome_receita = entry_receita.get()
    if not nome_receita:
        messagebox.showwarning("Erro", "Por favor, insira o nome da receita.")
        return

    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Inserindo a receita na tabela receitas
    cursor.execute("INSERT INTO receitas (nome) VALUES (?)", (nome_receita,))
    id_receita = cursor.lastrowid  # Pega o ID da receita recém-criada

    # Inserindo os ingredientes na tabela ingredientes
    for combo_produto, entry_quantidade in ingredientes_widgets:
        produto = combo_produto.get()
        quantidade = entry_quantidade.get()

        if not produto or not quantidade:
            messagebox.showwarning(
                "Erro", "Por favor, preencha todos os campos de produtos e quantidades.")
            return

        cursor.execute("INSERT INTO ingredientes (id_receita, produto, quantidade) VALUES (?, ?, ?)",
                       (id_receita, produto, quantidade))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Sucesso", "Receita e ingredientes cadastrados com sucesso!")
    entry_receita.delete(0, tk.END)
    for combo_produto, entry_quantidade in ingredientes_widgets:
        combo_produto.set('')
        entry_quantidade.delete(0, tk.END)

# Função para fechar o programa


def fechar():
    root.quit()


# Criação da janela principal
root = tk.Tk()
root.title("Cadastro de Receitas")

# Criar tabelas caso não existam
criar_tabelas()

# Carregar os produtos do estoque
produtos = carregar_produtos()

# Lista para armazenar os widgets dos ingredientes (produto e quantidade)
ingredientes_widgets = []

# Botão para fechar o programa
btn_fechar = tk.Button(root, text="Fechar", command=fechar, font=('Arial', 12))
btn_fechar.grid(row=0, column=2, padx=10, pady=10)

# Botão para adicionar mais ingredientes
btn_add_ingrediente = tk.Button(
    root, text="Adicionar Ingrediente", command=adicionar_ingrediente, font=('Arial', 12))
btn_add_ingrediente.grid(row=0, column=0, padx=10, pady=10)

# Botão para salvar a receita
btn_salvar = tk.Button(root, text="Salvar Receita",
                       command=salvar_receita, font=('Arial', 12))
btn_salvar.grid(row=0, column=1, padx=10, pady=10)

# Campo para inserir o nome da receita
tk.Label(root, text="Nome da Receita:", font=('Arial', 12)).grid(
    row=1, column=0, padx=10, pady=10, sticky='w')
entry_receita = tk.Entry(root, width=40, font=('Arial', 12))
entry_receita.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# Título para os ingredientes
tk.Label(root, text="Produto", font=('Arial', 12)).grid(
    row=2, column=0, padx=10, pady=10)
tk.Label(root, text="Quantidade", font=('Arial', 12)).grid(
    row=2, column=1, padx=10, pady=10)

# Adicionar o primeiro ingrediente automaticamente
adicionar_ingrediente()

# Execução do loop principal da janela
root.mainloop()
