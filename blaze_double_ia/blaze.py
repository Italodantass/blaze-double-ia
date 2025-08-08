import requests
from datetime import datetime

class BlazeCollector:
    def __init__(self):
        self.url = "https://blaze.com/api/roulette_games/recent"
        self.historico = []

    def coletar_dados(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                dados = response.json()
                jogo = dados[0]
                cor = jogo['color']
                horario = datetime.now().strftime('%H:%M:%S')
                print(f"[{horario}] Última cor: {cor}")
                self.historico.append((horario, cor))
            else:
                print(f"Erro ao coletar dados: {response.status_code}")
        except Exception as e:
            print(f"Exceção: {e}")