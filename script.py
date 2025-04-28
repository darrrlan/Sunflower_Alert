import requests
import datetime
import pytz
import json
import time
import os
from pushbullet import Pushbullet
from operator import itemgetter
from colorama import init, Fore

# Inicializar colorama
init(autoreset=True)

url = "https://api.sunflower-land.com/visit/3349809990567285"

tempos_crescimento_minutos = {
    "Sunflower": 1,
    "Potato": 5,
    "Pumpkin": 30,
    "Apple": 12*60,
    "Carrot": 60,
    "Cabbage": 2*60,
    "Soybean": 3*60,
    "Beetroot": 4*60,
    "Cauliflower": 8*60,
    "Parsnip": 12*60,
    "Eggplant": 16*60,
    "Corn": 20*60,
    "Radish": 24*60,
    "Honey": 24*60,
    "Wheat": 24*60,
    "Kale": 36*60,
    "Blueberry": 6*60,
}

fuso_brasil = pytz.timezone('America/Sao_Paulo')

def ms_to_datetime_local(ms):
    dt = datetime.datetime.fromtimestamp(ms / 1000)
    return fuso_brasil.localize(dt)

def send_push_notification(title, message):
    pb = Pushbullet("o.uxbBCN8ez4NQMqOfk6RtTT2baO9fOzcS")
    pb.push_note(title, message)

def get_emoji_for_plant(nome):
    emojis = {
        "Sunflower": "🌻",
        "Potato": "🥔",
        "Pumpkin": "🎃",
        "Apple": "🍎",
        "Carrot": "🥕",
        "Cabbage": "🥬",
        "Soybean": "🌱",
        "Beetroot": "🌰",
        "Cauliflower": "🥦",
        "Parsnip": "🌿",
        "Eggplant": "🍆",
        "Corn": "🌽",
        "Radish": "🌶️",
        "Wheat": "🌾",
        "Kale": "🥬",
        "Honey": "🍯",
        "Blueberry": "🫐",
    }
    return emojis.get(nome, "🌱")

def load_notified():
    try:
        with open('notificadas.json', 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_notified(notified):
    with open('notificadas.json', 'w') as file:
        json.dump(list(notified), file)

notificadas = load_notified()

while True:
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            with open('dados_fazenda.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            crops = data.get('state', {}).get('crops', {})
            fruitPatches = data.get('state', {}).get('fruitPatches', {})
            honey = data.get('state', {}).get('beehives', {})

            lista_itens = []
            agora = datetime.datetime.now(fuso_brasil)
            processados = set()

            # Processar crops
            for crop_info in crops.values():
                crop_data = crop_info.get('crop', {})
                nome = crop_data.get('name')
                planted_at = crop_data.get('plantedAt')

                if nome and planted_at and nome not in processados:
                    processados.add(nome)
                    plantado_em = ms_to_datetime_local(planted_at)
                    tempo_crescimento = tempos_crescimento_minutos.get(nome)

                    if tempo_crescimento:
                        pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                        tempo_faltando = (pronto_em - agora).total_seconds()
                        lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar frutas
            for fruit_info in fruitPatches.values():
                fruit_data = fruit_info.get('fruit')
                if fruit_data:
                    nome = fruit_data.get('name')
                    harvested_at = fruit_data.get('harvestedAt')
                    planted_at = fruit_data.get('plantedAt')

                    if nome and nome not in processados:
                        processados.add(nome)
                        timestamp_base = harvested_at if harvested_at != 0 else planted_at
                        plantado_em = ms_to_datetime_local(timestamp_base)
                        tempo_crescimento = tempos_crescimento_minutos.get(nome)

                        if tempo_crescimento:
                            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                            tempo_faltando = (pronto_em - agora).total_seconds()
                            lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar honey
            for beehive_id, beehive_info in honey.items():
                honey_data = beehive_info.get('honey', {})
                nome = f"Colmeia {beehive_id}"
                planted_at = honey_data.get('updatedAt')

                if planted_at and nome not in processados:
                    processados.add(nome)
                    plantado_em = ms_to_datetime_local(planted_at)
                    tempo_crescimento = tempos_crescimento_minutos.get("Honey")

                    pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                    tempo_faltando = (pronto_em - agora).total_seconds()
                    lista_itens.append(("Honey", plantado_em, pronto_em, tempo_faltando))

            lista_itens.sort(key=itemgetter(3))

            print("\n===> PLANTADOS E FRUTAS:\n")

            for nome, plantado_em, pronto_em, tempo_faltando in lista_itens:
                emoji = get_emoji_for_plant(nome)

                if tempo_faltando > 0:
                    horas = int(tempo_faltando // 3600)
                    minutos = int((tempo_faltando % 3600) // 60)
                    status = f"{horas}h {minutos}min restantes"
                    cor = Fore.YELLOW
                else:
                    status = "🌟 Pronto para colher!"
                    cor = Fore.GREEN
                    if nome not in notificadas:
                        send_push_notification(f"{emoji} {nome} Pronto para Colher!", f"{nome} está pronto para ser colhido!")
                        notificadas.add(nome)
                        save_notified(notificadas)

                print(f"{emoji} {cor}{nome}")
                print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Status: {status}\n")

        else:
            print(f"Falha ao acessar a API. Status code: {response.status_code}")

        time.sleep(10)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        time.sleep(10)
