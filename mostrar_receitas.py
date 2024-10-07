import tkinter as tk
from tkinter import ttk
import sqlite3

# Função para carregar todas as receitas do banco de dados


def carregar_receitas():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()
    cursor.execute("SELECT FROM receitas ORDER BY nome ASC")
    receitas = cursor.fetchall()
    conn.close()
    return [receita[0] for receita in receitas]


# Criação da janela principal
root = tk.Tk()
root.title("Mostrar Receitas")

# Criação da Treeview para exibir as receitas
tree = ttk.Treeview(root, columns=('Nome da Receita'),
                    show='headings', height=15)
tree.heading('Nome da Receita', text='Nome da Receita')
tree.column('Nome da Receita', anchor='center', width=300)
tree.pack(pady=20)

# Carrega as receitas e insere na Treeview
receitas = carregar_receitas()
for receita in receitas:
    tree.insert('', tk.END, values=(receita,))

# Botão para fechar a janela
btn_fechar = tk.Button(root, text="Fechar",
                       command=root.quit, width=20, font=('Arial', 12))
btn_fechar.pack(pady=10)

# Execução do loop principal da janela
root.mainloop()
