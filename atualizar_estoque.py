import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para carregar os produtos do banco de dados


def carregar_produtos():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute("SELECT produto FROM estoque")
    # Retorna uma lista de tuplas (ex: [('Produto1',), ('Produto2',)])
    produtos = cursor.fetchall()
    conn.close()
    # Transforma em uma lista simples (ex: ['Produto1', 'Produto2'])
    return [produto[0] for produto in produtos]

# Função para atualizar a quantidade no banco de dados


def atualizar_quantidade():
    # Pega o produto selecionado no combobox
    produto_selecionado = combo_produto.get()
    quantidade = entry_quantidade.get()  # Pega o valor inserido de quantidade

    if not produto_selecionado:
        messagebox.showwarning("Erro", "Por favor, selecione um produto.")
        return

    if not quantidade.isdigit():
        messagebox.showwarning(
            "Erro", "Por favor, insira um valor numérico válido.")
        return

    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Atualiza a quantidade somando a nova quantidade à existente
    cursor.execute("UPDATE estoque SET quantidade = COALESCE(quantidade, 0) + ? WHERE produto = ?",
                   (int(quantidade), produto_selecionado))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", f"Quantidade de '{
                        produto_selecionado}' atualizada com sucesso!")
    entry_quantidade.delete(0, tk.END)  # Limpa o campo de quantidade


# Criação da janela principal
root = tk.Tk()
root.title("Atualizar Quantidade em Estoque")

# Carrega os produtos do banco de dados
produtos = carregar_produtos()

# Label e combobox para selecionar o produto
label_produto = tk.Label(root, text="Produto:", font=('Arial', 12))
label_produto.pack(pady=10)

combo_produto = tk.StringVar()
# Combobox com os produtos cadastrados
produto_menu = tk.OptionMenu(root, combo_produto, *produtos)
produto_menu.config(width=30, font=('Arial', 12))
produto_menu.pack(pady=10)

# Campo de entrada para a quantidade a ser acrescentada
label_quantidade = tk.Label(
    root, text="Quantidade a acrescentar:", font=('Arial', 12))
label_quantidade.pack(pady=10)

entry_quantidade = tk.Entry(root, width=30, font=('Arial', 12))
entry_quantidade.pack(pady=10)

# Botão para atualizar a quantidade
btn_atualizar = tk.Button(
    root, text="Atualizar", command=atualizar_quantidade, width=20, font=('Arial', 12))
btn_atualizar.pack(pady=20)

btn_close = tk.Button(root, text="Fechar", command=root.quit,
                      width=20, height=3, font=('Arial', 12))
btn_close.pack(pady=20)

# Execução do loop principal da janela
root.mainloop()
