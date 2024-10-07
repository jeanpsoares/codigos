import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Função para criar a tabela consumo_semanal caso não exista


def criar_tabela_consumo():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute('''''''''
        CREATE TABLE IF NOT EXISTS consumo_semanal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade_usada REAL NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para carregar todas as receitas


def carregar_receitas():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM receitas ORDER BY nome ASC")
    receitas = cursor.fetchall()
    conn.close()
    return [receita[0] for receita in receitas]

# Função para carregar os ingredientes da receita selecionada


def mostrar_ingredientes():
    receita_selecionada = combo_receitas.get()
    if not receita_selecionada:
        messagebox.showwarning("Erro", "Por favor, selecione uma receita.")
        return

    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Busca o ID da receita selecionada
    cursor.execute("SELECT id FROM receitas WHERE nome = ?",
                   (receita_selecionada,))
    id_receita = cursor.fetchone()[0]

    # Busca os ingredientes da receita
    cursor.execute(
        "SELECT produto, quantidade FROM ingredientes WHERE id_receita = ?", (id_receita,))
    ingredientes = cursor.fetchall()
    conn.close()

    # Limpa a Treeview antes de inserir novos dados
    tree.delete(*tree.get_children())

    # Insere os ingredientes na Treeview
    for produto, quantidade in ingredientes:
        tree.insert('', tk.END, values=(produto, quantidade))

# Função para realizar a receita e atualizar o estoque e o consumo semanal


def fazer_receita():
    receita_selecionada = combo_receitas.get()
    if not receita_selecionada:
        messagebox.showwarning("Erro", "Por favor, selecione uma receita.")
        return

    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Busca o ID da receita selecionada
    cursor.execute("SELECT id FROM receitas WHERE nome = ?",
                   (receita_selecionada,))
    id_receita = cursor.fetchone()[0]

    # Busca os ingredientes da receita
    cursor.execute(
        "SELECT produto, quantidade FROM ingredientes WHERE id_receita = ?", (id_receita,))
    ingredientes = cursor.fetchall()

    # Atualiza o estoque e adiciona ao consumo_semanal
    for produto, quantidade in ingredientes:
        # Verifica a quantidade atual no estoque
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto = ?", (produto,))
        estoque_atual = cursor.fetchone()[0]

        if estoque_atual is None:
            estoque_atual = 0

        # Verifica se há quantidade suficiente no estoque
        if estoque_atual < quantidade:
            messagebox.showerror(
                "Erro", f"Estoque insuficiente para o produto: {produto}")
            conn.close()
            return

        # Subtrai a quantidade usada do estoque
        novo_estoque = estoque_atual - quantidade
        cursor.execute(
            "UPDATE estoque SET quantidade = ? WHERE produto = ?", (novo_estoque, produto))

        # Adiciona ao consumo semanal
        data_atual = datetime.now().strftime('%Y-%m-%d')  # Data atual
        cursor.execute("INSERT INTO consumo_semanal (produto, quantidade_usada, data) VALUES (?, ?, ?)",
                       (produto, quantidade, data_atual))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Sucesso", "A receita foi feita e o estoque atualizado!")


# Criação da janela principal
root = tk.Tk()
root.title("Mostrar Ingredientes")

# Criar a tabela consumo_semanal caso não exista
criar_tabela_consumo()

# Carregar todas as receitas
receitas = carregar_receitas()

# ComboBox para selecionar a receita
tk.Label(root, text="Selecione a Receita:", font=(
    'Arial', 12)).grid(row=0, column=0, padx=10, pady=10)
combo_receitas = ttk.Combobox(
    root, values=receitas, width=40, font=('Arial', 12))
combo_receitas.grid(row=0, column=1, padx=10, pady=10)

# Botão para mostrar os ingredientes da receita selecionada
btn_mostrar = tk.Button(root, text="Mostrar Ingredientes",
                        command=mostrar_ingredientes, font=('Arial', 12))
btn_mostrar.grid(row=0, column=2, padx=10, pady=10)

# Criação da Treeview para exibir os ingredientes
tree = ttk.Treeview(root, columns=('Produto', 'Quantidade'),
                    show='headings', height=15)
tree.heading('Produto', text='Produto')
tree.heading('Quantidade', text='Quantidade')
tree.column('Produto', anchor='center', width=200)
tree.column('Quantidade', anchor='center', width=100)
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Botão para realizar a receita e atualizar o estoque e o consumo semanal
btn_fazer_receita = tk.Button(
    root, text="Fazer Receita", command=fazer_receita, font=('Arial', 12))
btn_fazer_receita.grid(row=2, column=1, padx=10, pady=10)

# Botão para fechar a janela
btn_fechar = tk.Button(root, text="Fechar",
                       command=root.quit, width=20, font=('Arial', 12))
btn_fechar.grid(row=3, column=1, padx=10, pady=10)

# Execução do loop principal da janela
root.mainloop()
