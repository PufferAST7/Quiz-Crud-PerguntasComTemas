import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------- SISTEMA DE CORES ----------
temas_cores = [
    {
        "tema": "escuro",
        "bg": "#2B0646",
        "fg": "#EDE7F6",
        "btn_bg": "#7C3AED",
        "btn_fg": "#FFFFFF",
        "btn_principal_bg": "#54DFF1",
        "btn_principal_fg": "#1A0033"
    },
    {
        "tema": "claro",
        "bg": "#F8F5FF",
        "fg": "#2E0854",
        "btn_bg": "#D1B3FF",
        "btn_fg": "#2E0854",
        "btn_principal_bg": "#7B0CCA",
        "btn_principal_fg": "#EDE7F6"
    }
]

tema_index = 0

def cor(chave):
    return temas_cores[tema_index][chave]


def aplicar_tema_widget(widget, tema):
    """Aplica as cores do tema em um widget e em todos os filhos dele."""

    # Labels
    if isinstance(widget, tk.Label):
        widget.config(bg=tema["bg"], fg=tema["fg"])

    # Frames e LabelFrames  >>> MUDANÇA AQUI
    if isinstance(widget, tk.LabelFrame):
        widget.config(bg=tema["bg"], fg=tema["fg"])
    elif isinstance(widget, tk.Frame):
        widget.config(bg=tema["bg"])

    # Entrys  (Entry normal, mas NÃO o ttk.Combobox)
    if isinstance(widget, tk.Entry) and not isinstance(widget, ttk.Combobox):
        widget.config(
            bg="#FFFFFF" if tema["tema"] == "claro" else "#3E005B",
            fg=tema["fg"],
            insertbackground=tema["fg"]
        )

    # Botões
    if isinstance(widget, tk.Button):
        texto = widget.cget("text").lower()

        # Botões principais (CRUD)
        if texto in ["adicionar", "atualizar", "excluir", "limpar"]:
            widget.config(
                bg=tema["btn_principal_bg"],
                fg=tema["btn_principal_fg"],
                activebackground=tema["btn_principal_bg"],
                activeforeground=tema["btn_principal_fg"]
            )
        else:
            widget.config(
                bg=tema["btn_bg"],
                fg=tema["btn_fg"],
                activebackground=tema["btn_bg"],
                activeforeground=tema["btn_fg"]
            )

    # Aplica o tema em todos os filhos também
    for child in widget.winfo_children():
        aplicar_tema_widget(child, tema)


def aplicar_tema():
    tema = temas_cores[tema_index]
    janela.config(bg=tema["bg"])

    # -------- ttk (combobox, labelframe, treeview) --------
    style.configure("TLabelframe", background=tema["bg"])
    style.configure("TLabelframe.Label", background=tema["bg"], foreground=tema["fg"])

    style.configure("TLabel", background=tema["bg"], foreground=tema["fg"])
    style.configure("TFrame", background=tema["bg"])

    style.configure(
        "TCombobox",
        fieldbackground="#FFFFFF" if tema["tema"] == "claro" else "#3E005B",
        background=tema["btn_bg"],
        foreground=tema["fg"],
    )

    style.configure(
        "Treeview",
        background=tema["bg"],
        fieldbackground=tema["bg"],
        foreground=tema["fg"],
    )

    style.configure(
        "Treeview.Heading",
        background=tema["btn_bg"],
        foreground=tema["btn_fg"],
    )

    # >>> MUDANÇA: cor da LINHA SELECIONADA (sem hover)
    selected_bg = "#3E1B70" if tema["tema"] == "escuro" else "#D6C4FF"
    selected_fg = "#FFFFFF" if tema["tema"] == "escuro" else "#2B0646"
    style.map(
        "Treeview",
        background=[("selected", selected_bg)],
        foreground=[("selected", selected_fg)]
    )

    # -------- widgets Tk normais (labels, buttons, entries, frames...) --------
    aplicar_tema_widget(janela, tema)

    # Botão de tema
    btn_tema.config(
        text=" Mudar Tema ☾" if tema["tema"] == "escuro" else " Mudar Tema ☀︎",
        bg=tema["btn_bg"],
        fg=tema["btn_fg"],
    )

    # Atualiza Treeview (cores base)
    style.configure(
        "Treeview",
        background=tema["bg"],
        fieldbackground=tema["bg"],
        foreground=tema["fg"],
        font=("fixedsys", 16),
        rowheight=25
    )
    style.configure(
        "Treeview.Heading",
        background=tema["btn_bg"],
        foreground=tema["btn_fg"],
        font=("fixedsys", 17, "bold")
    )

def alterar_tema():
    global tema_index
    tema_index = (tema_index + 1) % len(temas_cores)
    aplicar_tema()

# ---------- ARQUIVO JSON ----------
ARQUIVO_JSON = "perguntas.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_JSON):
        dados = {"temas": {"gerais": [], "cinema": [], "esportes": [], "jogos": [], "geografia": [], "história": []}}
        salvar_dados(dados)
        return dados
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if "temas" not in dados:
                dados = {"temas": {"gerais": [], "cinema": [], "esportes": [], "jogos": [], "geografia": [], "história": []}}
            return dados
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Arquivo JSON corrompido. Criando novo.")
        dados = {"temas": {"gerais": [], "cinema": [], "esportes": [], "jogos": [], "geografia": [], "história": []}}
        salvar_dados(dados)
        return dados

def salvar_dados(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ---------- JANELA PRINCIPAL ----------
janela = tk.Tk()
janela.title("CRUD de Perguntas por Tema")
janela.geometry("1000x600")
janela.config(bg=cor("bg"))

# ---------- DADOS ----------
dados = carregar_dados()
temas = list(dados["temas"].keys())

# ---------- TÍTULO ----------
titulo = tk.Label(
    janela,
    text="Gerenciador de Perguntas do Quiz",
    font=("fixedsys", 30, "bold"),
    bg=cor("bg"),
    fg=cor("fg")
)
titulo.pack(pady=(20, 10))

# ---------- BOTÃO DE TEMA ----------
btn_tema = tk.Button(
    janela,
    text=" Mudar Tema ☾" if temas_cores[tema_index]["tema"] == "escuro" else " Mudar Tema ☀︎",
    bg=temas_cores[tema_index]["btn_bg"],
    fg=temas_cores[tema_index]["btn_fg"],
    width=15,
    font=("fixedsys", 16, "bold"),
    command=alterar_tema
)
btn_tema.pack(pady=(0, 10))

# ---------- FRAME DE CADASTRO / EDIÇÃO ----------
frame = tk.LabelFrame(
    janela,
    text="Cadastro / Edição de Perguntas",
    bd=2,
    font=("fixedsys", 17, "bold"),
    bg=cor("bg"),
    fg=cor("fg"),
    padx=20,
    pady=15
)
frame.pack(pady=20, padx=50, fill="both", expand=True)

# Labels e Entry
tk.Label(frame, text="Pergunta:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=0, column=0, sticky="w", pady=5)
entrada_pergunta = tk.Entry(frame, width=60, font=("fixedsys", 18))
entrada_pergunta.grid(row=0, column=1, columnspan=3, sticky="ew", pady=5, padx=5)

tk.Label(frame, text="Opção 1:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=1, column=0, sticky="w", pady=5)
entrada_op1 = tk.Entry(frame, font=("fixedsys", 18))
entrada_op1.grid(row=1, column=1, sticky="ew", padx=5)

tk.Label(frame, text="Opção 2:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=1, column=2, sticky="w")
entrada_op2 = tk.Entry(frame, font=("fixedsys", 18))
entrada_op2.grid(row=1, column=3, sticky="ew", padx=5)

tk.Label(frame, text="Opção 3:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=2, column=0, sticky="w", pady=5)
entrada_op3 = tk.Entry(frame, font=("fixedsys", 18))
entrada_op3.grid(row=2, column=1, sticky="ew", padx=5)

tk.Label(frame, text="Resposta:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=2, column=2, sticky="w")
entrada_resposta = tk.Entry(frame, font=("fixedsys", 18))
entrada_resposta.grid(row=2, column=3, sticky="ew", padx=5)

tk.Label(frame, text="Tema:", font=("fixedsys", 18), bg=cor("bg"), fg=cor("fg")).grid(row=3, column=0, sticky="w", pady=5)
combo_tema = ttk.Combobox(frame, values= temas, font=("fixedsys", 18), width=10)
combo_tema.current(0)
combo_tema.grid(row=3, column=1, sticky="w", pady=5, padx=5)

# Configura colunas para expandir
for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

# ---------- FUNÇÕES CRUD ----------
def atualizar_lista():
    tema = combo_tema.get()
    tree.delete(*tree.get_children())
    for i, p in enumerate(dados["temas"][tema]):
        tree.insert("", "end", iid=i, values=(p["pergunta"], ", ".join(p["opcoes"]), p["resposta"]))

def limpar():
    entrada_pergunta.delete(0, tk.END)
    entrada_op1.delete(0, tk.END)
    entrada_op2.delete(0, tk.END)
    entrada_op3.delete(0, tk.END)
    entrada_resposta.delete(0, tk.END)
    tree.selection_remove(tree.selection())

def adicionar():
    tema = combo_tema.get()
    pergunta = entrada_pergunta.get().strip()
    op1, op2, op3 = entrada_op1.get().strip(), entrada_op2.get().strip(), entrada_op3.get().strip()
    resposta = entrada_resposta.get().strip()
    if not all([pergunta, op1, op2, op3, resposta]):
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    dados["temas"][tema].append({"pergunta": pergunta, "opcoes": [op1, op2, op3], "resposta": resposta})
    salvar_dados(dados)
    atualizar_lista()
    limpar()

def atualizar():
    tema = combo_tema.get()
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma pergunta para atualizar!")
        return
    idx = int(selecionado[0])
    dados["temas"][tema][idx] = {
        "pergunta": entrada_pergunta.get().strip(),
        "opcoes": [entrada_op1.get().strip(), entrada_op2.get().strip(), entrada_op3.get().strip()],
        "resposta": entrada_resposta.get().strip()
    }
    salvar_dados(dados)
    atualizar_lista()
    limpar()

def excluir():
    tema = combo_tema.get()
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma pergunta para excluir!")
        return
    idx = int(selecionado[0])
    confirm = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta pergunta?")
    if confirm:
        del dados["temas"][tema][idx]
        salvar_dados(dados)
        atualizar_lista()
        limpar()

def carregar_para_edicao(event):
    tema = combo_tema.get()
    # Tupla que pega os IDS
    selecionado = tree.selection()
    if not selecionado:
        return
    idx = int(selecionado[0])

    # Acha a pergunta no dicionário
    p = dados["temas"][tema][idx]

    entrada_pergunta.delete(0, tk.END)
    entrada_pergunta.insert(0, p["pergunta"])
    entrada_op1.delete(0, tk.END)
    entrada_op1.insert(0, p["opcoes"][0])
    entrada_op2.delete(0, tk.END)
    entrada_op2.insert(0, p["opcoes"][1])
    entrada_op3.delete(0, tk.END)
    entrada_op3.insert(0, p["opcoes"][2])
    entrada_resposta.delete(0, tk.END)
    entrada_resposta.insert(0, p["resposta"])

# ---------- BOTÕES CRUD ----------
framebtn = tk.Frame(janela, bg=cor("bg"))
framebtn.pack(pady=10)
tk.Button(framebtn, text="Adicionar", font=("fixedsys"), command=adicionar, width=15, bg=cor("btn_principal_bg"), fg=cor("btn_principal_fg")).grid(row=0, column=0, padx=10)
tk.Button(framebtn, text="Atualizar", font=("fixedsys"),command=atualizar, width=15, bg=cor("btn_principal_bg"), fg=cor("btn_principal_fg")).grid(row=0, column=1, padx=10)
tk.Button(framebtn, text="Excluir", font=("fixedsys"),command=excluir, width=15, bg=cor("btn_principal_bg"), fg=cor("btn_principal_fg")).grid(row=0, column=2, padx=10)
tk.Button(framebtn, text="Limpar", font=("fixedsys"),command=limpar, width=15, bg=cor("btn_principal_bg"), fg=cor("btn_principal_fg")).grid(row=0, column=3, padx=10)

# ---------- TREEVIEW ----------
framelist = tk.LabelFrame(janela, text="Lista de Perguntas", font=("fixedsys", 15), bd=0, bg=cor("bg"), fg=cor("fg"))
framelist.pack(fill="both", expand=True, padx=10, pady=10)

colunas = ("pergunta", "opcoes", "resposta")
tree = ttk.Treeview(framelist, columns=colunas, show="headings", height=10)
tree.heading("pergunta", text="Pergunta")
tree.heading("opcoes", text="Opções")
tree.heading("resposta", text="Resposta")
tree.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("default")

# Sem hover no cabeçalho
style.map("Treeview.Heading", background=[], foreground=[])
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

tree.bind("<<TreeviewSelect>>", carregar_para_edicao)

def trocar_tema(event):
    atualizar_lista()

combo_tema.bind("<<ComboboxSelected>>", trocar_tema)

# ---------- INICIALIZAÇÃO ----------
aplicar_tema()
atualizar_lista()
janela.mainloop()