import customtkinter as ctk
from tkinter import messagebox
from config import SESSOES_DISPONIVEIS, TIPOS_GRAFICOS

class F1UI:
    """Gerenciador da interface grafica"""
    def __init__(self, root, data_handler, plotter):
        self.export_button = None
        self.zoom_out_button = None
        self.zoom_in_button = None
        self.zoom_frame = None
        self.graph_frame = None
        self.tipo_dropdown = None
        self.tipo_label = None
        self.volta2_dropdown = None
        self.volta2_label = None
        self.piloto2_dropdown = None
        self.piloto2_label = None
        self.volta1_dropdown = None
        self.volta1_label = None
        self.piloto1_dropdown = None
        self.piloto1_label = None
        self.comparar_button = None
        self.limpar_cache_button = None
        self.carregar_button = None
        self.sessao_dropdown = None
        self.sessao_label = None
        self.gp_entry = None
        self.gp_label = None
        self.ano_entry = None
        self.ano_label = None
        self.controls_frame = None
        self.root = root
        self.data_handler = data_handler
        self.plotter = plotter
        self.setup_ui()

    def setup_ui(self):
        """configura padroes inicias da interface"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.title("Telemetria F1: BLACKGSGO")
        self.root.geometry("1800x1200")

        # Frame para controles
        self.controls_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.controls_frame.pack(pady=20, padx=20, fill="x")

        # Entradas
        self.ano_label = ctk.CTkLabel(self.controls_frame, text="Ano:")
        self.ano_label.grid(row=0, column=0, padx=5, pady=5)
        self.ano_entry = ctk.CTkEntry(self.controls_frame, width=100, placeholder_text="2025")
        self.ano_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ano_entry.insert(0, "2025")

        self.gp_label = ctk.CTkLabel(self.controls_frame, text="GP:")
        self.gp_label.grid(row=0, column=2, padx=5, pady=5)
        self.gp_entry = ctk.CTkEntry(self.controls_frame, width=150, placeholder_text="China")
        self.gp_entry.grid(row=0, column=3, padx=5, pady=5)
        self.gp_entry.insert(0, "China")

        self.sessao_label = ctk.CTkLabel(self.controls_frame, text="Sessão:")
        self.sessao_label.grid(row=0, column=4, padx=5, pady=5)
        self.sessao_dropdown = ctk.CTkComboBox(self.controls_frame, width=150, values=SESSOES_DISPONIVEIS, state="readonly")
        self.sessao_dropdown.grid(row=0, column=5, padx=5, pady=5)
        self.sessao_dropdown.set("R")

        # Botoes
        self.carregar_button = ctk.CTkButton(self.controls_frame, text="Carregar Dados", command=self.carregar_dados, corner_radius=8)
        self.carregar_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.limpar_cache_button = ctk.CTkButton(self.controls_frame, text="Limpar Cache", command=self.limpar_cache, corner_radius=8)
        self.limpar_cache_button.grid(row=1, column=2, columnspan=2, pady=10)

        self.comparar_button = ctk.CTkButton(self.controls_frame, text="Comparar Voltas", command=self.comparar_voltas, corner_radius=8)
        self.comparar_button.grid(row=1, column=4, columnspan=2, pady=10)

        # Dropdowns para pilotos e voltas
        self.piloto1_label = ctk.CTkLabel(self.controls_frame, text="Piloto 1:")
        self.piloto1_label.grid(row=2, column=0, padx=5, pady=5)
        self.piloto1_dropdown = ctk.CTkComboBox(self.controls_frame, width=120, values=[""], state="readonly")
        self.piloto1_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.piloto1_dropdown.bind("<<ComboboxSelected>>", self.atualizar_voltas_piloto1)

        self.volta1_label = ctk.CTkLabel(self.controls_frame, text="Volta 1:")
        self.volta1_label.grid(row=3, column=0, padx=5, pady=5)
        self.volta1_dropdown = ctk.CTkComboBox(self.controls_frame, width=120, values=[""], state="readonly")
        self.volta1_dropdown.grid(row=3, column=1, padx=5, pady=5)

        self.piloto2_label = ctk.CTkLabel(self.controls_frame, text="Piloto 2:")
        self.piloto2_label.grid(row=2, column=2, padx=5, pady=5)
        self.piloto2_dropdown = ctk.CTkComboBox(self.controls_frame, width=120, values=[""], state="readonly")
        self.piloto2_dropdown.grid(row=2, column=3, padx=5, pady=5)
        self.piloto2_dropdown.bind("<<ComboboxSelected>>", self.atualizar_voltas_piloto2)

        self.volta2_label = ctk.CTkLabel(self.controls_frame, text="Volta 2:")
        self.volta2_label.grid(row=3, column=2, padx=5, pady=5)
        self.volta2_dropdown = ctk.CTkComboBox(self.controls_frame, width=120, values=[""], state="readonly")
        self.volta2_dropdown.grid(row=3, column=3, padx=5, pady=5)

        self.tipo_label = ctk.CTkLabel(self.controls_frame, text="Tipo de Gráfico:")
        self.tipo_label.grid(row=2, column=4, padx=5, pady=5)
        self.tipo_dropdown = ctk.CTkComboBox(self.controls_frame, width=150, values=TIPOS_GRAFICOS, state="readonly")
        self.tipo_dropdown.grid(row=2, column=5, padx=5, pady=5)
        self.tipo_dropdown.set("Velocidade")

        # Frame para o grafico de comparacao
        self.graph_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame para botoes de zoom e exportacao do grafico
        self.zoom_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.zoom_frame.pack(pady=5, padx=20, fill="x")

        self.zoom_in_button = ctk.CTkButton(self.zoom_frame, text="Zoom In", command=self.plotter.zoom_in, corner_radius=8)
        self.zoom_in_button.pack(side="left", padx=5)

        self.zoom_out_button = ctk.CTkButton(self.zoom_frame, text="Zoom Out", command=self.plotter.zoom_out, corner_radius=8)
        self.zoom_out_button.pack(side="left", padx=5)

        self.export_button = ctk.CTkButton(self.zoom_frame, text="Exportar Gráfico", command=self.exportar_grafico, corner_radius=8)
        self.export_button.pack(side="left", padx=5)

    def limpar_cache(self):
        """Limpa o cache e exibe mensagem."""
        success, msg = self.data_handler.limpar_cache()
        if success:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)

    def carregar_dados(self):
        """Carrega os dados da sessao."""
        try:
            ano = int(self.ano_entry.get())
            gp = self.gp_entry.get()
            sessao = self.sessao_dropdown.get()
            success, msg, pilotos, _ = self.data_handler.carregar_dados(ano, gp, sessao)
            if success:
                self.piloto1_dropdown.configure(values=pilotos)
                self.piloto2_dropdown.configure(values=pilotos)
                self.piloto1_dropdown.set(pilotos[0] if pilotos else "")
                self.piloto2_dropdown.set(pilotos[1] if len(pilotos) > 1 else "")
                self.volta1_dropdown.configure(values=[""])
                self.volta2_dropdown.configure(values=[""])
                self.atualizar_voltas_piloto1()
                self.atualizar_voltas_piloto2()
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)
        except ValueError as ve:
            messagebox.showerror("Erro", f"Por favor, insira um ano válido: {ve}")

    def atualizar_voltas_piloto1(self, *args):
        """Atualiza as voltas do piloto 1."""
        piloto = self.piloto1_dropdown.get()
        success, msg, voltas = self.data_handler.get_voltas_piloto(piloto, piloto_num=1)
        if success:
            self.volta1_dropdown.configure(values=voltas)
            self.volta1_dropdown.set(voltas[0])
        else:
            messagebox.showwarning("Aviso", msg)
            self.volta1_dropdown.configure(values=[""])
            self.volta1_dropdown.set("")

    def atualizar_voltas_piloto2(self, *args: object) -> None:
        """Atualiza as voltas do piloto 2."""
        piloto = self.piloto2_dropdown.get()
        success, msg, voltas = self.data_handler.get_voltas_piloto(piloto, piloto_num=2)
        if success:
            self.volta2_dropdown.configure(values=voltas)
            self.volta2_dropdown.set(voltas[0])
        else:
            messagebox.showwarning("Aviso", msg)
            self.volta2_dropdown.configure(values=[""])
            self.volta2_dropdown.set("")

    def comparar_voltas(self):
        """Compara as voltas selecionadas."""
        piloto1 = self.piloto1_dropdown.get()
        piloto2 = self.piloto2_dropdown.get()
        volta1_str = self.volta1_dropdown.get()
        volta2_str = self.volta2_dropdown.get()
        tipo_grafico = self.tipo_dropdown.get()

        if not piloto1 or not piloto2:
            messagebox.showwarning("Aviso", "Selecione dois pilotos para comparar.")
            return

        if not volta1_str or not volta2_str or "Nenhuma" in volta1_str or "Nenhuma" in volta2_str or "Erro" in volta1_str or "Erro" in volta2_str:
            messagebox.showwarning("Aviso", "Selecione voltas válidas para ambos os pilotos.")
            return

        success, msg = self.plotter.plot_comparacao(self.data_handler, piloto1, piloto2, volta1_str, volta2_str, tipo_grafico)
        if success:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)

    def exportar_grafico(self):
        """Exporta o grafico atual."""
        success, msg = self.plotter.exportar_grafico()
        if success:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)
