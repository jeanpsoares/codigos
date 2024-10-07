import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para criar o banco de dados e a tabela, caso ainda não existam


def create_database():
    # Conecta ao banco de dados (cria se não existir)
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    # Cria a tabela 'estoque' com colunas para produto e quantidade (que pode ser nula)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL UNIQUE,
            quantidade REAL
        )
    ''')
    conn.commit()
    conn.close()

# Função para verificar se o produto já existe no banco de dados


def produto_existe(produto):
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute("SELECT produto FROM estoque WHERE produto = ?", (produto,))
    result = cursor.fetchone()  # Retorna None se o produto não for encontrado
    conn.close()
    return result is not None  # Retorna True se o produto já existe

# Função para cadastrar um produto no banco de dados


def cadastrar_produto():
    produto = entry_produto.get()  # Pega o texto do campo de entrada do produto
    # Pega o texto do campo de entrada da quantidade
    quantidade = entry_quantidade.get()

    # Verifica se o campo de produto não está vazio
    if produto:
        if produto_existe(produto):  # Verifica se o produto já está cadastrado
            messagebox.showwarning("Erro", f"O produto '{
                                   produto}' já está cadastrado!")
        else:
            conn = sqlite3.connect('pd.db')
            cursor = conn.cursor()

            # Insere o produto e a quantidade no banco (a quantidade pode ser nula)
            if quantidade:
                cursor.execute(
                    "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade))
            else:
                cursor.execute(
                    "INSERT INTO estoque (produto, quantidade) VALUES (?, NULL)", (produto,))

            conn.commit()
            conn.close()

            # Exibe uma mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Produto '{
                                produto}' cadastrado com sucesso!")
            # Limpa o campo de entrada de produto
            entry_produto.delete(0, tk.END)
            # Limpa o campo de entrada de quantidade
            entry_quantidade.delete(0, tk.END)
    else:
        # Exibe uma mensagem de erro se o campo de produto estiver vazio
        messagebox.showwarning("Erro", "O campo Produto está vazio!")


# Criação da janela principal
root = tk.Tk()
root.title("Cadastro de Produto")

# Cria o banco de dados e a tabela
create_database()

# Campo de entrada para o nome do produto
label_produto = tk.Label(root, text="Produto:", font=('Arial', 12))
label_produto.pack(pady=10)

entry_produto = tk.Entry(root, width=30, font=('Arial', 12))
entry_produto.pack(pady=10)

# Campo de entrada para a quantidade do produto (opcional)
label_quantidade = tk.Label(
    root, text="Quantidade (opcional):", font=('Arial', 12))
label_quantidade.pack(pady=10)

entry_quantidade = tk.Entry(root, width=30, font=('Arial', 12))
entry_quantidade.pack(pady=10)

# Botão para cadastrar o produto
btn_cadastrar = tk.Button(
    root, text="Cadastrar", command=cadastrar_produto, width=20, font=('Arial', 12))
btn_cadastrar.pack(pady=20)

# Botão para encerrar janela
btn_fechar = tk.Button(root, text='Fechar', command=root.quit,
                       width=20, height=2, font=('Arial', 12))
btn_fechar.pack(pady=20)

# Execução do loop principal da janela
root.mainloop()
