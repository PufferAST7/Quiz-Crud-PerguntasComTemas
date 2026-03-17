
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import json
import random
import pygame
pygame.mixer.init()
 
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
tema_index=0 #0 = escuro, 1 = claro

def cor (chave):
    return temas_cores[tema_index][chave]

def aplicar_tema():
    tema = temas_cores[tema_index]
    janela.config(bg=tema["bg"])

    for widget in janela.winfo_children():
        try:
            # Primeiro: se for botão especial, NÃO MEXE E NEM PINTA
            if isinstance(widget, tk.Button) and hasattr(widget, "tema_especial"):
                continue

            # Agora sim, aplica o tema normal
            widget.config(bg=tema["bg"], fg=tema["fg"])

            # Atualiza o botão de tema
            btn_tema.config(
                text=" Mudar Tema ☾" if temas_cores[tema_index]["tema"] == "escuro" else " Mudar Tema ☀︎",
                bg=tema["btn_bg"],
                fg=tema["btn_fg"]
            )

            # Trata botões normais (não especiais)
            if isinstance(widget, tk.Button):

                texto = widget.cget("text").lower()

                # Trata botões entrar/start/responder
                if "entrar" in texto or "start" in texto or "responder" in texto:
                    widget.config(
                        bg=tema["btn_principal_bg"],
                        fg=tema["btn_principal_fg"]
                    )
                    widget.bind("<Enter>", lambda e, w=widget: w.config(bg="#009BAF" if tema["tema"] == "escuro" else "#302588")) 
                    widget.bind("<Leave>", lambda e, w=widget: w.config(bg=tema["btn_principal_bg"]))

                else:
                    widget.config(
                        bg=tema["btn_bg"],
                        fg=tema["btn_fg"]
                    )
        except:
            pass

def alterar_tema():
    global tema_index
    tema_index = (tema_index + 1) % len(temas_cores)
    aplicar_tema()

# sons
som_clique = "selecionar.wav"
som_start = "start.wav"
som_tema = "tema.wav"

# funçao limpar tela
def limpar_tela():
    for widget in janela.winfo_children():
        widget.destroy()

# funçao tocar som
def tocar_som(arquivo):
    try:
        pygame.mixer.Sound(arquivo).play()
    except Exception as e:
        print(f"Erro ao tocar o som: {e}")

# abre arquivo perguntas.json
with open("perguntas.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
    temas = list(dados["temas"].keys())
    perguntas_temas = dados["temas"]

# cria janela
janela = tk.Tk()
janela.title("QUIZ")
janela.geometry("1500x900")
janela.config(bg=cor("bg"))

rodadas = 0
tema_escolhido = None

# Capa do jogo
lbl_logo = tk.Label(
    janela, 
    text="QUIZ", 
    font=("fixedsys", 80, "bold"), 
    bg=cor("bg"), 
    fg=cor("fg")
)
lbl_logo.pack(pady=100)

lbl_sub = tk.Label(
    janela, 
    text="Prepare-se para o desafio!", 
    font=("fixedsys", 30, "bold"), 
    bg=cor("bg"), 
    fg=cor("fg")
)
lbl_sub.pack(pady=40)

btn_entrar = tk.Button(
    janela, 
    text="🎮 ENTRAR NO JOGO 🎮", 
    bg=cor("btn_principal_bg"), 
    fg=cor("btn_principal_fg"), 
    width=20,
    font=("fixedsys", 22, "bold",), 
    command=lambda: (tocar_som(som_start), escolher_tema())
)
btn_entrar.pack(pady=20)

btn_sair = tk.Button(
        janela,
        text=" SAIR ",
        bg="red",
        fg="white",
        width=12,
        font=("fixedsys", 18, "bold"),
        command= janela.destroy
    )
btn_sair.tema_especial = True
btn_sair.pack(pady=0)

btn_tema = tk.Button(
    janela, 
    text=" Mudar Tema ☾ " if temas_cores[tema_index]["tema"] == "escuro" else " Mudar Tema ☀︎ ", 
    bg=temas_cores[tema_index]["btn_bg"], 
    fg=temas_cores[tema_index]["btn_fg"],  
    width=15,
    font=("fixedsys", 16, "bold",), 
    command=lambda: (tocar_som(som_tema), alterar_tema())
)
btn_tema.pack(pady=20)

lbl = tk.Label(janela, text="", font=(70), bg=cor("bg"))
lbl.pack(pady=140,padx=0)

# Recria a tela inicial
def voltar_inicial():
    limpar_tela()
    global lbl_logo, lbl_sub, btn_entrar, btn_tema, btn_sair,rodadas
    rodadas = 0

    lbl_logo = tk.Label(
        janela,
        text="QUIZ",
        font=("fixedsys", 80, "bold"),
        bg=cor("bg"),
        fg=cor("fg")
    )
    lbl_logo.pack(pady=100)

    lbl_sub = tk.Label(
        janela,
        text="Prepare-se para o desafio!",
        font=("fixedsys", 30, "bold"),
        bg=cor("bg"),
        fg=cor("fg")
    )
    lbl_sub.pack(pady=40)

    btn_entrar = tk.Button(
        janela,
        text="🎮 ENTRAR NO JOGO 🎮",
        bg=cor("btn_principal_bg"),
        fg=cor("btn_principal_fg"),
        width=20,
        font=("fixedsys", 22, "bold"),
        command=lambda: (tocar_som(som_start), escolher_tema())
    )
    btn_entrar.pack(pady=20)

    btn_sair = tk.Button(
        janela,
        text=" SAIR ",
        bg="red",
        fg="white",
        width=12,
        font=("fixedsys", 18, "bold"),
        command=janela.destroy
        )
    btn_sair.tema_especial = True
    btn_sair.pack(pady=0)

    btn_tema = tk.Button(
        janela,
        text=" Mudar Tema ☾ " if temas_cores[tema_index]["tema"] == "escuro" else " Mudar Tema ☀︎ ",
        bg=cor("btn_bg"),
        fg=cor("btn_fg"),
        width=15,
        font=("fixedsys", 16, "bold"),
        command=lambda: (tocar_som(som_tema), alterar_tema())
    )
    btn_tema.pack(pady=20)

# Segunda janela com seleçao de temas
def escolher_tema():
    global lbl_logo, btn_entrar,btn_tema
    limpar_tela()

    lbl_logo = tk.Label(janela, text=" QUIZ ", font=("fixedsys", 70, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_logo.pack(pady=60,padx=0)

    lbl_titulo = tk.Label(janela,text="Escolha um tema:", font=("fixedsys", 40, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_titulo.pack(pady=20)

    temas_dados = [
        ("🧠 GERAIS 🦾", "#CF68C0", "#FFFFFF", "gerais"),
        ("🎬 CINEMA 🎥", "#E82243", "#FFFFFF", "cinema"),
        ("🏀 ESPORTES ⚽", "#14BC52", "#FFFFFF", "esportes"),
        ("🎮 JOGOS 🕹️", "#9333EA", "#FFFFFF", "jogos"),
        ("🌋 GEOGRAFIA 🌍", "#2563EB", "#FFFFFF", "geografia"),
        ("🔥 HISTÓRIA 🗿", "#F59E0B", "#FFFFFF", "historia"),
    ]

    for texto, cor_bg, cor_fg, chave in temas_dados:
        btn = tk.Button(
            janela,
            text=texto,
            bg=cor_bg,
            fg=cor_fg,
            font=("fixedsys", 22, "bold"),
            width=20,
            command=lambda t=chave: (tocar_som(som_clique), selecionar_tema(t))
        )
        btn.tema_especial = True
        btn.pack(pady=10)

    btn_tema = tk.Button(
    janela,
    text=" Mudar Tema ☾ " if temas_cores[tema_index]["tema"] == "escuro" else " Mudar Tema ☀︎ ",
    bg=cor("btn_bg"),
    fg=cor("btn_fg"),
    width=15,
    font=("fixedsys", 16, "bold"),
    command=lambda: (tocar_som(som_tema), alterar_tema())
    )
    btn_tema.pack(pady=10)

def selecionar_tema(tema):
    global tema_escolhido
    tema_escolhido = tema
    selecionar()

# Janela de dados dos jogadores e números de rodadas
def selecionar():
    global lbl_logo, btn_entrar, btn_start, lbl_player1, lbl_player2, entrada_player1, entrada_player2, lbl_contador, lbl_rodadas, btn_mais, btn_menos,rodadas
    limpar_tela()
    rodadas = 0
    
    lbl_logo = tk.Label(janela, text=" QUIZ ", font=("fixedsys", 70, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_logo.pack(pady=60,padx=0)

    lbl_player1 = tk.Label(janela, text="Player1: ", font=("fixedsys", 26, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_player1.pack(pady=5)
    entrada_player1= tk.Entry(janela, width=25, font=("fixedsys", 20, "bold"),bg="#C9BFD9")
    entrada_player1.pack(pady=0)

    lbl_player2 = tk.Label(janela, text="Player2: ", font=("fixedsys", 26, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_player2.pack(pady=5)
    entrada_player2= tk.Entry(janela, width=25, font=("fixedsys", 20, "bold"),bg="#C9BFD9")
    entrada_player2.pack(pady=0)

    # espaço vazio para estética
    lbl = tk.Label(janela, text="", bg=cor("bg"), fg=cor("fg"))
    lbl.pack(pady=5)

    # Frame
    frame = tk.LabelFrame(janela,text="",bg=cor("bg"),bd=0)
    frame.pack(fill="x",pady=5,padx=0)

    # espaço vazio para estética
    lbl = tk.Label(frame, text="", bg=cor("bg"), fg=cor("fg"))
    lbl.grid(row= 1, column=0, padx=335)

    lbl_rodadas = tk.Label(frame, text="Rodadas:", font=("fixedsys", 30, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_rodadas.grid(row= 1, column=3, padx=20)

    lbl_contador = tk.Label(frame, text=str(rodadas), font=("fixedsys", 30, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_contador.grid(row= 1, column=4, padx=20)

    # função para botao mais
    def mais():
        global rodadas
        rodadas += 1
        lbl_contador.config(text=str(rodadas))

    # função para botao menos    
    def menos():
        global rodadas
        if rodadas > 0:
            rodadas -= 1
            lbl_contador.config(text=str(rodadas))
    
    btn_menos=tk.Button(
    frame, 
    text=" - ", 
    bg="#9128D7", 
    fg="#C9BFD9", 
    font=("Arial", 16, "bold",),
    width=3, 
    command= lambda: (tocar_som("selecionar.wav"),menos())
    )
    btn_menos.grid(row= 1, column=2, pady=0)

    btn_mais=tk.Button(
        frame, 
        text=" + ", 
        bg="#9128D7", 
        fg="#C9BFD9", 
        font=("Arial", 16, "bold"), 
        width=3,
        command= lambda: (tocar_som("selecionar.wav"),mais())
        
    )
    btn_mais.grid(row= 1, column=5, pady=0)


    btn_start = tk.Button(
        janela,
        text="START",
        bg=cor("btn_principal_bg"), 
        fg=cor("btn_principal_fg"),
        width=10,
        font=("fixedsys", 20, "bold"),
        command=lambda: (tocar_som(som_start), jogo(entrada_player1.get().strip() or "Player 1",
                                                    entrada_player2.get().strip() or "Player 2"))
    )
    btn_start.pack(pady=100, padx=90)


    cores_temas = {
        "gerais": ("#CF68C0", "#FFFFFF"),
        "cinema": ("#E82243", "#FFFFFF"),
        "esportes": ("#14BC52", "#FFFFFF"),
        "jogos": ("#9333EA", "#FFFFFF"),
        "geografia": ("#2563EB", "#FFFFFF"),
        "historia": ("#F59E0B", "#FFFFFF"),
    }
    cor_bg_tema, cor_fg_tema = cores_temas.get(tema_escolhido, ("#ffffff", "#000000"))

    tk.Label(
        janela,
        text=f" Tema selecionado: {tema_escolhido.upper()} ",
        bg=cor_bg_tema,
        fg=cor_fg_tema,
        font=("fixedsys", 18, "bold"),
        width=30
    ).pack(pady=10)


    btn_voltar_tema = tk.Button(
        janela,
        text="Voltar para temas",
        bg="#AE00FF",
        fg="white",
        font=("fixedsys", 16, "bold"),
        width=22,
        command=lambda: (tocar_som(som_start), escolher_tema())
    )
    btn_voltar_tema.pack(pady=10)

# Função principal do jogo contendo lógica de perguntas, respostas e placar
def jogo(nome,nome2):
    global rodadas
    total_perguntas= len(perguntas_temas[tema_escolhido])
    # Valida número de rodadas: deve ser par e não zero
    if rodadas % 2 != 0:
        messagebox.showwarning("Aviso", "Escolha um número PAR")
        return 
    if rodadas == 0:
        messagebox.showwarning("Aviso", "Escolha um número de rodadas")
        return 
    if rodadas > total_perguntas:
        messagebox.showwarning("Aviso", f"Número maximo atigindo, escolha ate {total_perguntas}")
        return
    limpar_tela()

    pontuacao1 = 0 
    pontuacao2 = 0

    rodada_atual = 0
    perguntas_aleatorias = random.sample(perguntas_temas[tema_escolhido], rodadas)

    jogador_atual = random.choice([1,2])

    # === Widgets do jogo ===

    lbl = tk.Label(janela, text="", bg=cor("bg"), fg=cor("fg"))
    lbl.pack(pady=20, padx=0)

    # Label para mostrar a pergunta
    lbl_pergunta = tk.Label(janela, text="", font=("fixedsys", 25, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_pergunta.pack(pady=15, padx=0)

    # Variável para armazenar qual resposta foi selecionada
    resposta_escolhida = tk.StringVar() 

    # Frame para agrupar os radios buttons
    frame = tk.LabelFrame(janela,text="",bg=cor("bg"),bd=0)
    frame.pack(fill="x",pady=5,padx=0)

    botoes_opcao = []
    for i in range(3):
        botao = tk.Radiobutton(
            frame,
            text="",
            variable=resposta_escolhida,
            value="",
            fg=cor("fg"),
            bg=cor("bg"),
            font=("fixedsys", 17, "bold"),
            selectcolor = "#161616" if temas_cores[tema_index]["tema"] == "escuro" else "#EAE1EE",         
            activebackground=cor("bg"),
            activeforeground=cor("fg")
        )
        botao.pack(anchor="w", pady=10)
        botoes_opcao.append(botao)

    lbl = tk.Label(janela, text="", bg=cor("bg"), fg=cor("fg"))
    lbl.pack(pady=50, padx=0)

    # === NOVA ÁREA DE INFORMAÇÕES DO JOGO ===

    # Título mostrando de quem é a vez
    lbl_info = tk.Label(
        janela,
        text=f"🎯  Vez de: {nome if jogador_atual == 1 else nome2}",
        font=("fixedsys", 32, "bold"),
        bg=cor("bg"),
        fg=cor("fg")
    )
    lbl_info.pack(pady=5)

    # Progresso da rodada
    lbl_progresso = tk.Label(
        janela,
        text=f"Pergunta {rodada_atual+1}/{rodadas}",
        font=("fixedsys", 22, "bold"),
        bg=cor("bg"),
        fg=cor("fg")
    )
    lbl_progresso.pack(pady=0)

    # Box do placar
    frame_placar = tk.Frame(janela, bg=cor("btn_bg"), bd=3)
    frame_placar.pack(pady=25)

    lbl_titulo_placar = tk.Label(
        frame_placar,
        text="🏆  PLACAR  🏆",
        font=("fixedsys", 22, "bold"),
        bg=cor("btn_bg"),
        fg=cor("btn_fg")
    )
    lbl_titulo_placar.pack(pady=(5,0))

    lbl_placar = tk.Label(
        frame_placar,
        text=f"{nome}: {pontuacao1}\n{nome2}: {pontuacao2}",
        font=("fixedsys", 20, "bold"),
        bg=cor("btn_bg"),
        fg=cor("btn_fg"),
        justify="center"
    )
    lbl_placar.pack(pady=10)


    def atualizar_placar():
        lbl_placar.config(text=f"{nome}: {pontuacao1}\n{nome2}: {pontuacao2}")

    # Exibe a pergunta atual, limpa resultado da pergunta anterior e atualiza interface
    def mostrar_pergunta():
        nonlocal rodada_atual, jogador_atual

        lbl_resultado.config(text="")

        if rodada_atual >= len(perguntas_aleatorias):
            total_per_player = len(perguntas_aleatorias)//2  
            total = len(perguntas_aleatorias)

            if pontuacao1 == pontuacao2:
                messagebox.showinfo("Fim do Quiz", f"Empate! Vocês acertaram {pontuacao1 + pontuacao2} de {total} perguntas!")
            elif pontuacao1 > pontuacao2:
                messagebox.showinfo("Fim do Quiz", f"1° - {nome} 🥇 ({pontuacao1}/{total_per_player})\n2° - {nome2} 🥈 ({pontuacao2}/{total_per_player})")
            else:
                messagebox.showinfo("Fim do Quiz", f"1° - {nome2} 🥇 ({pontuacao2}/{total_per_player})\n2° - {nome} 🥈 ({pontuacao1}/{total_per_player})")
            COMMAND = voltar_inicial()

        pergunta_atual = perguntas_aleatorias[rodada_atual]
        lbl_pergunta.config(text=pergunta_atual["pergunta"])
        resposta_escolhida.set("vazio")

        for botao in botoes_opcao:
            botao.deselect()

        for i, opcao in enumerate(pergunta_atual["opcoes"]):
            botoes_opcao[i].config(text=opcao, value=opcao)
            botoes_opcao[i].pack_configure(padx=300)

        # 🔥 ATUALIZAÇÃO CORRETA
        lbl_info.config(
            text=f"🎯  Vez de: {nome if jogador_atual == 1 else nome2}"
        )

        lbl_progresso.config(
            text=f"Pergunta {rodada_atual+1}/{rodadas}"
        )


    # Verifica se a resposta escolhida é correta, atualiza placar e mostra resultado
    def verificar_resposta():
        nonlocal rodada_atual, pontuacao1, pontuacao2, jogador_atual
        
        escolha = resposta_escolhida.get()
        if not escolha or escolha == "vazio" or escolha.strip() == "":
            messagebox.showwarning("Aviso", "Selecione uma opção antes de responder!")
            return

        resposta_correta = perguntas_aleatorias[rodada_atual]["resposta"]

        if escolha.strip().lower() == resposta_correta.strip().lower():  
            if jogador_atual == 1:
                pontuacao1 += 1
            else:
                pontuacao2 += 1
            lbl_resultado.config(text="✅ Correto!", fg="#00FF00")
            tocar_som("correto.wav")
        else:
            lbl_resultado.config(text=f"❌ Errado! Resposta: {resposta_correta}", fg="#FF0000")
            tocar_som("erro.wav")

        atualizar_placar()

        rodada_atual += 1
        jogador_atual = 1 if jogador_atual == 2 else 2
        janela.after(2500, mostrar_pergunta)

    lbl = tk.Label(janela, text="", bg=cor("bg"), fg=cor("fg"))
    lbl.pack(pady=10)

    btn_conferir = tk.Button(
        janela,
        text="Responder",
        bg=cor("btn_principal_bg"), 
        fg=cor("btn_principal_fg"),
        font=("fixedsys", 17, "bold"),
        width=20,
        command=verificar_resposta
    )
    btn_conferir.pack(pady=10, padx=50)

    # Label para mostrar resultado da resposta correta/errada
    lbl_resultado = tk.Label(janela, text="", font=("fixedsys", 15, "bold"), bg=cor("bg"), fg=cor("fg"))
    lbl_resultado.pack(pady=0)

    mostrar_pergunta()

janela.mainloop()