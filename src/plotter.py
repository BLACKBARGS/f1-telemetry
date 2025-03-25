import numpy as np
import pandas as pd
import customtkinter as ctk
import mplcursors
import matplotlib.pyplot as plt
from tkinter import filedialog
from config import TEAM_COLORS, TIRE_COLORS
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class F1Plotter:
    """Classe para gerenciar a plotagem de graficos de telemetria."""
    def __init__(self, graph_frame):
        self.graph_frame = graph_frame
        self.canvas = None
        self.current_ax = None
        self.current_fig = None

    def limpar_grafico(self):
        """Limpa o grafico anterior."""
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

    def plot_comparacao(self, data_handler, piloto1, piloto2, volta1_str, volta2_str, tipo_grafico):
        """Plota a comparacao de telemetria entre dois pilotos."""
        try:
            # Carrega telemetria
            success1, msg1, tel1, lap1 = data_handler.get_telemetria(piloto1, volta1_str, 1)
            success2, msg2, tel2, lap2 = data_handler.get_telemetria(piloto2, volta2_str, 2)
            if not success1 or not success2:
                raise ValueError(f"{msg1}\n{msg2}")

            # Pega informacoes dos pilotos
            team1, pos1 = data_handler.get_driver_info(piloto1)
            team2, pos2 = data_handler.get_driver_info(piloto2)
            cor1 = TEAM_COLORS.get(team1, "#FF3333")
            cor2 = TEAM_COLORS.get(team2, "#00FFFF")
            compound1 = lap1.get("Compound", "Desconhecido")
            compound2 = lap2.get("Compound", "Desconhecido")

            # Pega informacoes climaticas
            weather_info = data_handler.get_weather_info()
            temp_track = weather_info["temp_track"]
            temp_air = weather_info["temp_air"]
            rain = weather_info["rain"]
            wind_speed = weather_info["wind_speed"]

            # Configura o layout
            self.limpar_grafico()
            fig = plt.figure(figsize=(8, 6), facecolor="#1a1a1a")
            gs = fig.add_gridspec(1, 4)
            ax = fig.add_subplot(gs[0, :3])
            self.current_ax = ax
            self.current_fig = fig

            # Adiciona fundo com gradiente
            gradient = np.linspace(0, 1, 256)
            gradient = np.vstack((gradient, gradient))
            cmap = LinearSegmentedColormap.from_list("custom_gradient", ["#2a2a2a", "#1a1a1a"])
            ax.imshow(gradient, aspect="auto", cmap=cmap, extent=ax.get_xlim() + ax.get_ylim(), alpha=0.5, zorder=-1)

            # Plota os dados
            if tipo_grafico == "Velocidade":
                y1 = tel1["Speed"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "Speed")
                ylabel = "Velocidade (km/h)"
            elif tipo_grafico == "Delta":
                y1 = data_handler.calcular_delta(tel1, tel2)
                y2 = np.zeros_like(y1)
                ylabel = "Delta (s)"
            elif tipo_grafico == "Acelerador":
                y1 = tel1["Throttle"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "Throttle")
                ylabel = "Acelerador (%)"
            elif tipo_grafico == "Freio":
                y1 = tel1["Brake"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "Brake")
                ylabel = "Freio (%)"
            elif tipo_grafico == "Marcha":
                y1 = tel1["nGear"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "nGear")
                ylabel = "Marcha"
            elif tipo_grafico == "RPM":
                y1 = tel1["RPM"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "RPM")
                ylabel = "RPM"
            elif tipo_grafico == "DRS":
                if "DRS" not in tel1 or "DRS" not in tel2:
                    raise ValueError("Dados de DRS não disponíveis para esta sessão.")
                y1 = tel1["DRS"]
                y2 = data_handler.interpolar_telemetria(tel1, tel2, "DRS")
                ylabel = "DRS (Ativado=1, Desativado=0)"
            elif tipo_grafico == "Velocidade do Vento":
                if wind_speed == "N/A":
                    raise ValueError("Dados de velocidade do vento não disponíveis para esta sessão.")
                y1 = np.full_like(tel1["Distance"], wind_speed)
                y2 = np.full_like(tel1["Distance"], wind_speed)
                ylabel = "Velocidade do Vento (km/h)"
            else:
                raise ValueError("Tipo de gráfico inválido")

            max_idx1 = np.argmax(y1)
            max_idx2 = np.argmax(y2) if tipo_grafico != "Delta" else np.argmax(np.abs(y2))
            max_val1 = y1.iloc[max_idx1] if isinstance(y1, pd.Series) else y1[max_idx1]
            max_val2 = y2[max_idx2]

            line1, = ax.plot(tel1["Distance"], y1, label=f"{piloto1} ({compound1}, P{pos1})", color=cor1, linewidth=2)
            line2, = ax.plot(tel1["Distance"], y2, label=f"{piloto2} ({compound2}, P{pos2})", color=cor2, linestyle="dashed", linewidth=2)

            # Adiciona interatividade
            cursor = mplcursors.cursor([line1, line2], hover=True)
            ax_map = fig.add_subplot(gs[0, 3])
            x = tel1["X"]
            y = tel1["Y"]
            ax_map.plot(x, y, color="white", linewidth=2, alpha=0.3)

            # Destaca setores
            circuit_info = data_handler.session.get_circuit_info()
            sector_distances = []
            if hasattr(circuit_info, "corners"):
                for corner in circuit_info.corners:
                    if "distance" in corner:
                        sector_distances.append(corner["distance"])
                sector_colors = ["#FF5555", "#55FF55", "#5555FF"]
                start_dist = 0
                for i, end_dist in enumerate(sector_distances + [tel1["Distance"].iloc[-1]]):
                    mask = (tel1["Distance"] >= start_dist) & (tel1["Distance"] <= end_dist)
                    ax_map.plot(tel1["X"][mask], tel1["Y"][mask], color=sector_colors[i % len(sector_colors)], linewidth=2)
                    start_dist = end_dist

            # Destaca zonas de DRS
            if "DRS" in tel1:
                drs_zones = tel1["DRS"] > 0
                if drs_zones.any():
                    ax_map.plot(tel1["X"][drs_zones], tel1["Y"][drs_zones], color="#00FF00", linewidth=3, alpha=0.7, label="DRS Zone")

            ax_map.set_aspect("equal")
            ax_map.axis("off")
            ax_map.set_facecolor("#1a1a1a")
            marker, = ax_map.plot([], [], "o", color="yellow", markersize=8)

            @cursor.connect("add")
            def on_add(sel):
                x_dist, y_val = sel.target
                sel.annotation.set_text(f"Distância: {x_dist:.1f}m\nValor: {y_val:.2f}")
                idx = np.argmin(np.abs(tel1["Distance"] - x_dist))
                marker.set_data([tel1["X"].iloc[idx]], [tel1["Y"].iloc[idx]])
                fig.canvas.draw_idle()

            # Adiciona anotacoes nos picos
            ax.annotate(f"{max_val1:.1f}", (tel1["Distance"].iloc[max_idx1], max_val1), textcoords="offset points", xytext=(0, 10), ha="center", color=cor1)
            ax.plot(tel1["Distance"].iloc[max_idx1], max_val1, "o", color=cor1)
            ax.annotate(f"{max_val2:.1f}", (tel1["Distance"].iloc[max_idx2], max_val2), textcoords="offset points", xytext=(0, -15), ha="center", color=cor2)
            ax.plot(tel1["Distance"].iloc[max_idx2], max_val2, "o", color=cor2)

            # Adiciona linhas verticais para os setores
            if sector_distances:
                for dist in sector_distances:
                    ax.axvline(x=dist, color="gray", linestyle="--", alpha=0.5, label="Setor" if dist == sector_distances[0] else "")

            ax.set_xlabel("Distância na Volta (m)", color="white")
            ax.set_ylabel(ylabel, color="white")
            ax.set_title(f"Comparação de {tipo_grafico}: {piloto1} vs {piloto2}\nTemp. Pista: {temp_track}°C, Temp. Ar: {temp_air}°C, Chuva: {rain}", color="white")
            legend = ax.legend(facecolor="#1a1a1a", edgecolor="white", labelcolor="white")
            for text, compound in zip(legend.get_texts(), [compound1, compound2]):
                if compound in TIRE_COLORS:
                    text.set_color(TIRE_COLORS[compound])
            ax.set_facecolor("none")
            ax.tick_params(colors="white")
            ax.grid(True, color="gray", linestyle="--", alpha=0.3)

            plt.tight_layout()
            self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

            return True, "Gráfico plotado com sucesso!"
        except Exception as e:
            return False, f"Falha ao plotar gráfico: {e}"

    def zoom_in(self):
        """Aplica zoom in no grafico."""
        if self.current_ax:
            xlim = self.current_ax.get_xlim()
            ylim = self.current_ax.get_ylim()
            new_xlim = [xlim[0] + (xlim[1] - xlim[0]) * 0.25, xlim[1] - (xlim[1] - xlim[0]) * 0.25]
            new_ylim = [ylim[0] + (ylim[1] - ylim[0]) * 0.25, ylim[1] - (ylim[1] - ylim[0]) * 0.25]
            self.current_ax.set_xlim(new_xlim)
            self.current_ax.set_ylim(new_ylim)
            self.current_fig.canvas.draw()

    def zoom_out(self):
        """Aplica zoom out no grafico."""
        if self.current_ax:
            xlim = self.current_ax.get_xlim()
            ylim = self.current_ax.get_ylim()
            new_xlim = [xlim[0] - (xlim[1] - xlim[0]) * 0.25, xlim[1] + (xlim[1] - xlim[0]) * 0.25]
            new_ylim = [ylim[0] - (ylim[1] - ylim[0]) * 0.25, ylim[1] + (ylim[1] - ylim[0]) * 0.25]
            self.current_ax.set_xlim(new_xlim)
            self.current_ax.set_ylim(new_ylim)
            self.current_fig.canvas.draw()

    def exportar_grafico(self):
        """Exporta o grafico como PNG."""
        if self.current_fig:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.current_fig.savefig(file_path, dpi=300, bbox_inches="tight")
                return True, f"Gráfico exportado como {file_path}"
        return False, "Nenhum gráfico para exportar."
