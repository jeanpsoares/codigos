import tkinter as tk
from tkinter import ttk
import sqlite3
from collections import defaultdict

# Função para carregar os dados de consumo semanal


def carregar_consumo_semanal():
    conn = sqlite3.connect('pd.db')
    cursor = conn.cursor()

    # Consulta para buscar produto, quantidade usada e data
    cursor.execute(
        "SELECT produto, quantidade_usada, data FROM consumo_semanal")
    dados_consumo = cursor.fetchall()
    conn.close()

    # Dicionário para armazenar o consumo por semana e produto
    consumo_por_semana = defaultdict(lambda: defaultdict(int))

    # Dicionário para armazenar o total de consumo de cada produto
    consumo_total_produto = defaultdict(int)

    # Processa os dados e agrupa por semana e produto
    for produto, quantidade_usada, data in dados_consumo:
        # Agrupa por semana do ano
        semana = f"{data[:4]}-W{int(data[5:7]) // 7}"
        consumo_por_semana[produto][semana] += quantidade_usada
        consumo_total_produto[produto] += quantidade_usada

    return consumo_por_semana, consumo_total_produto

# Função para calcular a média de consumo por semana


def calcular_media_semanal(consumo_por_semana):
    media_semanal = {}
    for produto, semanas in consumo_por_semana.items():
        total_semanas = len(semanas)
        total_consumo = sum(semanas.values())
        media_semanal[produto] = total_consumo / \
            total_semanas if total_semanas > 0 else 0
    return media_semanal

# Função para exibir os dados na Treeview


def mostrar_consumo_semanal():
    # Limpa a Treeview antes de inserir novos dados
    tree.delete(*tree.get_children())

    # Carrega os dados de consumo semanal
    consumo_por_semana, consumo_total_produto = carregar_consumo_semanal()

    # Calcula a média semanal de consumo
    media_semanal = calcular_media_semanal(consumo_por_semana)

    # Exibe os dados na Treeview
    for produto, semanas in consumo_por_semana.items():
        for semana, quantidade in semanas.items():
            media = f"{media_semanal[produto]:.2f}"
            tree.insert('', tk.END, values=(
                produto, semana, quantidade, media))


# Criação da janela principal
root = tk.Tk()
root.title("Relatório de Consumo Semanal")

# Criação da Treeview para exibir o consumo semanal
tree = ttk.Treeview(root, columns=('Produto', 'Semana',
                    'Quantidade Consumida', 'Média Semanal'), show='headings', height=15)
tree.heading('Produto', text='Produto')
tree.heading('Semana', text='Semana')
tree.heading('Quantidade Consumida', text='Quantidade Consumida')
tree.heading('Média Semanal', text='Média Semanal')

tree.column('Produto', anchor='center', width=150)
tree.column('Semana', anchor='center', width=100)
tree.column('Quantidade Consumida', anchor='center', width=150)
tree.column('Média Semanal', anchor='center', width=150)

tree.pack(padx=20, pady=20)

# Botão para carregar os dados
btn_carregar = tk.Button(root, text="Carregar Consumo Semanal",
                         command=mostrar_consumo_semanal, font=('Arial', 12))
btn_carregar.pack(pady=10)

# Botão para fechar a janela
btn_fechar = tk.Button(root, text="Fechar",
                       command=root.quit, width=20, font=('Arial', 12))
btn_fechar.pack(pady=10)

# Execução do loop principal da janela
root.mainloop()
