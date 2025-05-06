import requests
import datetime
import pytz
import json
import time
import os
from operator import itemgetter
from colorama import init, Fore
from config_telegram import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

init(autoreset=True)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def load_notified():
    try:
        with open('notificadas.json', 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_notified(notified):
    with open('notificadas.json', 'w') as file:
        json.dump(list(notified), file)

def ms_to_datetime_local(ms):
    dt = datetime.datetime.fromtimestamp(ms / 1000)
    return fuso_brasil.localize(dt)

tempos_crescimento_minutos = {
    "Sunflower": 1,
    "Potato": 5,
    "Pumpkin": 30,
    "Carrot": 60,
    "Cabbage": 120,
    "Beetroot": 240,
    "Cauliflower": 480,
    "Parsnip": 720,
    "Eggplant": 960,
    "Corn": 1200,
    "Radish": 1440,
    "Honey": 1440,
    "Bot do Telegram": 1440,
}

url = "https://api.sunflower-land.com/visit/3349809990567285"
fuso_brasil = pytz.timezone('America/Sao_Paulo')
notificadas = load_notified()

while True:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erro ao acessar API: {response.status_code}")
            continue

        data = response.json()
        crops = data.get('state', {}).get('crops', {})
        agora = datetime.datetime.now(fuso_brasil)
        lista_itens = []

        for crop_info in crops.values():
            crop = crop_info.get('crop', {})
            nome = crop.get('name')
            planted_at = crop.get('plantedAt')

            if nome and planted_at:
                plantado_em = ms_to_datetime_local(planted_at)
                tempo_min = tempos_crescimento_minutos.get(nome)

                if tempo_min:
                    pronto_em = plantado_em + datetime.timedelta(minutes=tempo_min)
                    tempo_faltando = (pronto_em - agora).total_seconds()
                    lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

        lista_itens.sort(key=itemgetter(3))

        for nome, plantado_em, pronto_em, tempo_faltando in lista_itens:
            if tempo_faltando <= 0 and nome not in notificadas:
                mensagem = f"{nome} está pronto para ser colhido!\nPlantado em: {plantado_em.strftime('%H:%M')}"
                send_telegram_message(mensagem)
                notificadas.add(nome)
                save_notified(notificadas)

        for nome, _, pronto_em, tempo_faltando in lista_itens:
            status = f"{int(tempo_faltando // 60)} min restantes" if tempo_faltando > 0 else "Pronto!"
            print(f"{Fore.GREEN if tempo_faltando <= 0 else Fore.YELLOW}{nome}: {status} - Pronto às {pronto_em.strftime('%H:%M')}")

        time.sleep(9.7)
        os.system('cls' if os.name == 'nt' else 'clear')

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(10)
