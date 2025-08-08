import asyncio
import websockets
import json
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests

historico = []

def enviar_sinal_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': texto,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=payload)

def analisar_probabilidade():
    if len(historico) < 20:
        return None

    ultimos = historico[-20:]
    vermelhos = ultimos.count('red')
    pretos = ultimos.count('black')
    brancos = ultimos.count('white')

    total = vermelhos + pretos + brancos
    if total == 0:
        return None

    prob_vermelho = (vermelhos / total) * 100
    prob_preto = (pretos / total) * 100
    prob_branco = (brancos / total) * 100

    if prob_vermelho > 70:
        return '🔴 Vermelho', prob_vermelho, prob_branco
    elif prob_preto > 70:
        return '⚫ Preto', prob_preto, prob_branco
    return None

async def conectar_blaze():
    uri = "wss://blaze.com/api/ws"
    async with websockets.connect(uri) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get('event') == 'roulette':
                cor = data['data']['color']
                if cor == 0:
                    historico.append('red')
                elif cor == 1:
                    historico.append('black')
                elif cor == 2:
                    historico.append('white')

                resultado = analisar_probabilidade()
                if resultado:
                    cor_predita, chance, branco = resultado
                    agora = datetime.now().strftime('%H:%M')
                    mensagem = f"""
🎯 <b>Sinal encontrado!</b>
Cor: {cor_predita}
Probabilidade: <b>{chance:.2f}%</b>
Branco: {branco:.2f}%
Estratégia: <i>Probabilidade Alta</i>
Horário previsto: <b>{agora}</b>
"""
                    enviar_sinal_telegram(mensagem)

if __name__ == "__main__":
    try:
        asyncio.run(conectar_blaze())
    except Exception as e:
        print(f"Erro: {e}")
        while True:
            pass  # impede que o processo finalize

