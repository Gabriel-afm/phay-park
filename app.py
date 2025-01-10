import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

# Função para atualizar as cores das barras com base no valor do estoque
def atualizar_grafico():
    global barras
    barras.clear()
    for i, (produto, qtd) in enumerate(estoque.items()):
        cor = "green" if qtd >= 50 else "yellow" if qtd >= 20 else "red"
        barras.append(canvas.create_rectangle(50, 50 + i * 30, 50 + qtd, 70 + i * 30, fill=cor))

# Função para editar um produto
def editar_produto():
    produto = entrada_produto.get()
    nova_qtd = entrada_quantidade.get()
    validade = entrada_validade.get()
    if produto in estoque:
        try:
            estoque[produto] = int(nova_qtd)
            validade_produtos[produto] = datetime.strptime(validade, '%d/%m/%Y')
            atualizar_grafico()
            atualizar_alertas()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade ou validade inválida.")
    else:
        messagebox.showerror("Erro", "Produto não encontrado no estoque.")

# Função para verificar validade dos produtos
def atualizar_alertas():
    alertas.delete(0, tk.END)
    for produto, validade in validade_produtos.items():
        if validade <= datetime.now() + timedelta(days=7):
            alertas.insert(tk.END, f"{produto}: próximo da validade ({validade.strftime('%d/%m/%Y')})")

# Função para mostrar gráfico de pizza
def mostrar_grafico_pizza():
    janela_pizza = tk.Toplevel(root)
    janela_pizza.title("Gráfico de Pizza")
    fig, ax = plt.subplots()
    ax.pie(estoque.values(), labels=estoque.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title("Distribuição do Estoque")
    canvas_pizza = FigureCanvasTkAgg(fig, master=janela_pizza)
    canvas_pizza.get_tk_widget().pack()
    plt.close(fig)

# Dados iniciais
estoque = {"Produto A": 60, "Produto B": 45, "Produto C": 15}
validade_produtos = {"Produto A": datetime(2025, 1, 20), "Produto B": datetime(2025, 1, 15), "Produto C": datetime(2025, 1, 12)}

# Criação da janela principal
root = tk.Tk()
root.title("Gerenciamento de Estoque")

# Canvas para o gráfico de barras
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack()
barras = []
atualizar_grafico()

# Entradas para edição
frame_editar = tk.Frame(root)
frame_editar.pack(pady=10)

tk.Label(frame_editar, text="Produto:").grid(row=0, column=0)
entrada_produto = tk.Entry(frame_editar)
entrada_produto.grid(row=0, column=1)

tk.Label(frame_editar, text="Quantidade:").grid(row=1, column=0)
entrada_quantidade = tk.Entry(frame_editar)
entrada_quantidade.grid(row=1, column=1)

tk.Label(frame_editar, text="Validade (DD/MM/AAAA):").grid(row=2, column=0)
entrada_validade = tk.Entry(frame_editar)
entrada_validade.grid(row=2, column=1)

botao_editar = tk.Button(frame_editar, text="Editar Produto", command=editar_produto)
botao_editar.grid(row=3, columnspan=2, pady=5)

# Lista de alertas
frame_alertas = tk.Frame(root)
frame_alertas.pack(pady=10)

tk.Label(frame_alertas, text="Alertas de Validade:").pack()
alertas = tk.Listbox(frame_alertas, width=50, height=5)
alertas.pack()
atualizar_alertas()

# Botão para mostrar gráfico de pizza
botao_pizza = tk.Button(root, text="Mostrar Gráfico de Pizza", command=mostrar_grafico_pizza)
botao_pizza.pack(pady=10)

root.mainloop()
