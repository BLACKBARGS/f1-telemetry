import fastf1
import numpy as np
import pandas as pd
import os
from config import CACHE_DIR

class F1DataHandler:
    """Classe para gerenciar dados de telemetria da F1."""
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        fastf1.Cache.enable_cache(CACHE_DIR)
        self.session = None
        self.last_session_key = None
        self.laps_piloto1 = None
        self.laps_piloto2 = None

    def limpar_cache(self):
        """Limpa o cache do fastf1."""
        try:
            fastf1.Cache.clear_cache(CACHE_DIR)
            self.last_session_key = None
            return True, "Cache limpo com sucesso!"
        except Exception as e:
            return False, f"Falha ao limpar cache: {e}"

    def carregar_dados(self, ano, gp, sessao):
        """Carrega os dados da sessão F1 escolhida."""
        session_key = (ano, gp, sessao)
        if session_key == self.last_session_key and self.session is not None:
            return True, "Dados já carregados! Usando dados existentes.", None, None
        
        try:
            self.session = fastf1.get_session(ano, gp, sessao)
            self.session.load(telemetry=True, laps=True, weather=True)
            self.last_session_key = session_key
            
            if self.session is None:
                raise ValueError("Sessao nao foi carregada corretamente.")
            
            pilotos = [self.session.get_driver(drv)["Abbreviation"] for drv in self.session.drivers]
            if not pilotos:
                raise ValueError("Nenhum piloto encontrado na sessão.")
            
            if self.session.laps is None or self.session.laps.empty:
                raise ValueError("Nenhuma volta foi carregada para esta sessão.")
            
            self.laps_piloto1 = None
            self.laps_piloto2 = None
            return True, "Dados carregados com sucesso!", pilotos, None
        except Exception as e:
            return False, f"Falha ao carregar dados: {e}", None, None

    def get_voltas_piloto(self, piloto, piloto_num):
        """Retorna as voltas disponiveis para um piloto.

        Args:
            piloto (str): Abreviatura do piloto (ex.: 'VER').
            piloto_num (int): Numero do piloto (1 ou 2) pra determinar onde armazenar as voltas.

        Returns:
            tuple: (success, message, voltas)
        """
        if not piloto or not self.session:
            return False, "Piloto ou sessão nao selecionados.", []
        
        try:
            # Carrega as voltas do piloto
            laps = self.session.laps.pick_drivers(piloto)
            if laps is None or laps.empty:
                return False, f"Nenhuma volta encontrada para {piloto}", []
            
            # Armazena as voltas no atributo correto (piloto 1 ou piloto 2)
            if piloto_num == 1:
                self.laps_piloto1 = laps
            elif piloto_num == 2:
                self.laps_piloto2 = laps
            else:
                raise ValueError("piloto_num deve ser 1 ou 2")
            
            voltas = []
            for _, lap in laps.iterrows():
                lap_number = int(lap["LapNumber"])
                lap_time = lap["LapTime"]
                if pd.isna(lap_time):
                    voltas.append(f"Volta {lap_number} - Sem tempo")
                else:
                    voltas.append(f"Volta {lap_number} - {lap_time.total_seconds():.3f}s")
            
            if not voltas:
                voltas = ["Nenhuma volta disponivel"]
            
            return True, "Voltas carregadas com sucesso!", voltas
        except Exception as e:
            return False, f"Erro ao carregar voltas: {e}", ["Erro ao carregar voltas"]

    def get_telemetria(self, piloto, volta_str, piloto_num):
        """Retorna a telemetria de uma volta especifica de um piloto."""
        try:
            laps = self.laps_piloto1 if piloto_num == 1 else self.laps_piloto2
            volta_num = int(volta_str.split("Volta ")[1].split(" - ")[0])
            lap = laps[laps["LapNumber"] == volta_num].iloc[0]
            tel = lap.get_telemetry()
            if tel.empty:
                raise ValueError("Telemetria vazia para o piloto")
            return True, "Telemetria carregada com sucesso!", tel, lap
        except Exception as e:
            return False, f"Falha ao carregar telemetria: {e}", None, None

    def interpolar_telemetria(self, tel_ref, tel, canal):
        """Interpolar um canal de telemetria pra alinhar com a distancia de referencia."""
        if canal == "Time":
            valores = tel[canal].dt.total_seconds()
        else:
            valores = tel[canal].astype(float)
        return np.interp(tel_ref["Distance"], tel["Distance"], valores.fillna(0))

    def calcular_delta(self, tel1, tel2):
        """Calcula o delta de tempo entre duas telemetrias."""
        time1 = tel1["Time"].dt.total_seconds()
        time2 = self.interpolar_telemetria(tel1, tel2, "Time")
        return time1 - time2

    def get_weather_info(self):
        """Retorna informacoes climaticas da sessao."""
        if not self.session or self.session.weather_data.empty:
            return {"temp_track": "N/A", "temp_air": "N/A", "rain": False, "wind_speed": "N/A"}
        
        weather = self.session.weather_data
        return {
            "temp_track": int(weather["TrackTemp"].mean()) if "TrackTemp" in weather else "N/A",
            "temp_air": int(weather["AirTemp"].mean()) if "AirTemp" in weather else "N/A",
            "rain": weather["Rainfall"].mean() > 0 if "Rainfall" in weather else False,
            "wind_speed": weather["WindSpeed"].mean() if "WindSpeed" in weather else "N/A"
        }

    def get_driver_info(self, piloto):
        """Retorna informacoes do piloto (equipe, posicao)."""
        if not self.session:
            return "Desconhecido", "N/A"
        
        driver_info = self.session.get_driver(piloto)
        team = driver_info["TeamName"] if "TeamName" in driver_info else "Desconhecido"
        results = self.session.results
        position = int(results[results["Abbreviation"] == piloto]["Position"].iloc[0]) if piloto in results["Abbreviation"].values else "N/A"
        return team, position
