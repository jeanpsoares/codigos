import tkinter as tk
from tkinter import ttk
import sqlite3
from collections import defaultdict
from datetime import datetime

# Função para carregar os dados de consumo total e a quantidade de semanas em que o produto foi consumido


def carregar_consumo_total():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Consulta para buscar produto, quantidade usada e data
    cursor.execute(
        "SELECT produto, quantidade_usada, data FROM consumo_semanal")
    dados_consumo = cursor.fetchall()
    conn.close()

    # Dicionário para armazenar o total de consumo de cada produto e as semanas distintas de consumo
    consumo_total_produto = defaultdict(int)
    semanas_produto = defaultdict(set)

    # Processa os dados e agrupa por produto
    for produto, quantidade_usada, data in dados_consumo:
        # Converte a string para objeto datetime
        data_obj = datetime.strptime(data, '%Y-%m-%d')
        semana = data_obj.strftime('%Y-%U')  # Formata como 'Ano-Semana'

        consumo_total_produto[produto] += quantidade_usada
        # Adiciona a semana ao conjunto (para não repetir)
        semanas_produto[produto].add(semana)

    return consumo_total_produto, semanas_produto

# Função para calcular a média de consumo por semana para cada produto


def calcular_media_semanal(consumo_total_produto, semanas_produto):
    media_semanal = {}
    for produto, consumo_total in consumo_total_produto.items():
        # Número de semanas distintas em que o produto foi consumido
        total_semanas = len(semanas_produto[produto])
        media_semanal[produto] = consumo_total / \
            total_semanas if total_semanas > 0 else 0
    return media_semanal

# Função para exibir os dados na Treeview


def mostrar_consumo_total():
    # Limpa a Treeview antes de inserir novos dados
    tree.delete(*tree.get_children())

    # Carrega os dados de consumo total e semanas de consumo
    consumo_total_produto, semanas_produto = carregar_consumo_total()

    # Calcula a média semanal de consumo
    media_semanal = calcular_media_semanal(
        consumo_total_produto, semanas_produto)

    # Exibe os dados na Treeview
    for produto, total_consumido in consumo_total_produto.items():
        media = f"{media_semanal[produto]:.2f}"
        tree.insert('', tk.END, values=(produto, total_consumido, media))


# Criação da janela principal
root = tk.Tk()
root.title("Relatório de Consumo Total")

# Criação da Treeview para exibir o consumo total e a média semanal
tree = ttk.Treeview(root, columns=(
    'Produto', 'Quantidade Consumida', 'Média Semanal'), show='headings', height=15)
tree.heading('Produto', text='Produto')
tree.heading('Quantidade Consumida', text='Quantidade Consumida')
tree.heading('Média Semanal', text='Média Semanal')

tree.column('Produto', anchor='center', width=200)
tree.column('Quantidade Consumida', anchor='center', width=200)
tree.column('Média Semanal', anchor='center', width=150)

tree.pack(padx=20, pady=20)

# Botão para carregar os dados
btn_carregar = tk.Button(root, text="Carregar Consumo Total",
                         command=mostrar_consumo_total, font=('Arial', 12))
btn_carregar.pack(pady=10)

# Botão para fechar a janela
btn_fechar = tk.Button(root, text="Fechar",
                       command=root.quit, width=20, font=('Arial', 12))
btn_fechar.pack(pady=10)

# Execução do loop principal da janela
root.mainloop()
