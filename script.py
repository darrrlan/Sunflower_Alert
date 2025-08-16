import requests
import datetime
import pytz
import json
import time
from colorama import init, Fore
import telegram
import asyncio
import config_telegram

# 🔹 Inicializa colorama
init(autoreset=True)

# 🔹 URL da fazenda
URL = "https://api.sunflower-land.com/visit/1444484773494499"

# 🔹 Tabela de tempos (em minutos) para crops, árvores, recursos e frutas
TEMPOS_CRESCIMENTO = {
    "Sunflower Crunch": 0,
    "Roast Veggies": 0,
    "Club Sandwich": 0,
    "Fruit salad": 0,
    "Mushroom Jacket Potatoes": 0,
    "Cauliflower Burger": 0,
    "Bumpkin Salad": 0,
    "Goblin's Treat": 0,
    "Pancakes":0,
    "Bumpkin ganoush": 0,
    "Chowder": 0,
    "Tofu Scramble": 0,
    "Fish Burger": 0,
    "Fried Calamari": 0,
    "Fish Omelette": 0,
    "Beetroot Blaze": 0,
    "Ocean's olive": 0,
    "Fish n Chips": 0,
    "Sushi Roll": 0,
    "Seafood Basket": 0,
    "Bumpkin Roast": 0,
    "Goblin Brunch": 0,
    "Steamed Red Rice": 0,
    "Caprese Salad": 0,
    "Spaghetti al Limone": 0,
    "Fried Tofu": 0,
    "Mashed Potato": 0,
    "Rhubarb Tart": 0,
    "Pumpkin Soup": 0,
    "Reindeer Carrot": 0,
    "Mushroom Soup": 0,
    "Boiled Eggs": 0,
    "Bumpkin Broth": 0,
    "Popcorn": 0,
    "Cabbers n Mash": 0,
    "Rapid Rosat": 0,
    "Kale Stew": 0,
    "Gumbo": 0,
    "Kale Omelette": 0,
    "Rice Bun": 0,
    "Antipasto": 0,
    "Pizza Margherita": 0,
    "Sunflower": 1,
    "Potato": 5,
    "Pumpkin": 30,
    "Apple": 12 * 60,
    "Carrot": 60,
    "Cabbage": 2 * 60,
    "Soybean": 3 * 60,
    "Beetroot": 4 * 60,
    "Sprout Mix": 0,
    "Cauliflower": 8 * 60,
    "Fruitful Blend": 8 * 60,
    "Parsnip": 12 * 60,
    "Eggplant": 16 * 60,
    "Corn": 20 * 60,
    "Radish": 24 * 60,
    "Honey": 24 * 60,
    "Red Pansy": 24 * 60,
    "Yellow Pansy": 24 * 60,
    "Purple Pansy": 24 * 60,
    "White Pansy": 24 * 60,
    "Blue Pansy": 24 * 60,
    "Red Cosmos": 24 * 60,
    "Yellow Cosmos": 24 * 60,
    "Purple Cosmos": 24 * 60,
    "White Cosmos": 24 * 60,
    "Blue Cosmos": 24 * 60,
    "Prism Petal": 24 * 60,
    "Wheat": 24 * 60,
    "Kale": 36 * 60,
    "Blueberry": 6 * 60,
    "Tomato" : 2 * 60,
    "Lemon" : 4*60,
    "Celestine": 6 * 60,
    "Lunara": 12 *60,
    "Duskberry": 24 *60,
    "Orange": 8 *60,
    "Banana": 12 * 60,
    "Grape" : 12 * 60,
    "Rice" : 32 * 60,
    "Olive" : 44 * 60,
    "Barley" : 48 * 60,
    "Honey": (21*60) + 50,  # 21h em minutos
}

# 🔹 Fuso horário Brasil
FUSO_BRASIL = pytz.timezone("America/Sao_Paulo")

# 🔹 Bot do Telegram
bot = telegram.Bot(token=config_telegram.TELEGRAM_API_KEY)

async def send_telegram_notification(message):
    try:
        await bot.send_message(chat_id=config_telegram.TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Erro ao enviar notificação Telegram: {e}")

def send_telegram_notification_sync(message):
    asyncio.run(send_telegram_notification(message))

# 🔹 Controle de notificações
def load_notified():
    try:
        with open("notificadas.json", "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_notified(notified):
    with open("notificadas.json", "w") as file:
        json.dump(list(notified), file)

notificadas = load_notified()

# 🔹 Funções auxiliares
def ms_to_datetime_local(ms):
    """Converte timestamp em ms para datetime no fuso Brasil"""
    dt_utc = datetime.datetime.fromtimestamp(ms / 1000, tz=pytz.UTC)
    return dt_utc.astimezone(FUSO_BRASIL)

def process_items(state: dict):
    """Processa crops, fruitPatches e honey"""
    agora = datetime.datetime.now(FUSO_BRASIL)
    lista_itens = []

    # ================== CROPS ==================
    crops = state.get("crops", {})
    for crop_info in crops.values():
        crop_data = crop_info.get("crop", {})
        nome = crop_data.get("name")
        planted_at = crop_data.get("plantedAt")
        if nome and planted_at:
            plantado_em = ms_to_datetime_local(planted_at)
            tempo_crescimento = TEMPOS_CRESCIMENTO.get(nome, 0)
            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
            tempo_faltando = (pronto_em - agora).total_seconds()
            uid = nome
            lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "crops"))

    # ================== FRUIT PATCHES ==================
    fruitPatches = state.get("fruitPatches", {})
    frutas_adicionadas = set()
    for fruit_info in fruitPatches.values():
        fruit_data = fruit_info.get("fruit", {})
        nome = fruit_data.get("name")
        ready_at = fruit_data.get("readyAt") or fruit_data.get("harvestedAt") or fruit_data.get("plantedAt")
        if nome and ready_at and nome not in frutas_adicionadas:
            plantado_em = ms_to_datetime_local(ready_at)
            tempo_crescimento = TEMPOS_CRESCIMENTO.get(nome, 0)
            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
            tempo_faltando = (pronto_em - agora).total_seconds()
            uid = nome
            lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "fruitPatches"))
            frutas_adicionadas.add(nome)
            
     # Processar colmeias
    honey = state.get('beehives', {})
    honey_adicionados = set()
    for beehive_id, beehive_info in honey.items():
        honey_data = beehive_info.get('honey', {})
        nome = f"Honney"
        updated_at = honey_data.get('updatedAt')  # ms
        produced_ms = honey_data.get('produced', 0)  # ms

        if nome and updated_at and nome not in honey_adicionados:

            started_at = updated_at - produced_ms
            plantado_em = ms_to_datetime_local(started_at)
            tempo_crescimento = TEMPOS_CRESCIMENTO.get("Honey", 21 * 60)
            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
            tempo_faltando = (pronto_em - agora).total_seconds()
            uid = nome
            lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "Honey"))
            honey_adicionados.add(nome)
        # Processar flores
        flowers = state.get('flowers', {}).get('flowerBeds', {}) if 'flowers' in state else {}
        flowers_adicionados = set()
        if isinstance(flowers, dict):
            for flower_info in flowers.values():
                flower_data = flower_info.get('flower', {})
                nome = flower_data.get('name')
                planted_at = flower_data.get('plantedAt')

                if nome and planted_at and nome not in flowers_adicionados:
                    plantado_em = ms_to_datetime_local(planted_at)
                    tempo_crescimento = TEMPOS_CRESCIMENTO.get(nome, 0)

                    pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                    tempo_faltando = (pronto_em - agora).total_seconds()
                    uid = nome
                    lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "Flower"))
                    flowers_adicionados.add(nome)

     # Processar Compost Bin e Turbo Composter (mesmo tratamento)
            buildings = state.get('buildings', {})
            compost_bins = buildings.get('Compost Bin', [])
            turbo_composters = buildings.get('Turbo Composter', [])
            buildings_adicionados = set()
            for compost_list in [compost_bins, turbo_composters]:
                for compost_info in compost_list:
                    compost_data = compost_info.get('producing', {})
                    items = compost_data.get('items', {})
                    nome = next(iter(items), None)

                    startedAt = compost_data.get('startedAt')
                    readyAt = compost_data.get('readyAt')

                    if nome and startedAt and readyAt and nome not in buildings_adicionados:
                        plantado_em = ms_to_datetime_local(startedAt)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        uid = nome
                        lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "Compost"))
                        flowers_adicionados.add(nome)
    
     # Processar Fire Pit
            fire_pits = buildings.get('Fire Pit', [])
            fire_pits_adicionados = set()
            for fire_info in fire_pits:
                fire_data = fire_info.get('crafting', [])
                if isinstance(fire_data, list) and len(fire_data) > 0:
                    item = fire_data[0]
                    nome = item.get("name")
                    readyAt = item.get("readyAt")

                    if nome and readyAt and nome not in fire_pits_adicionados:
                        tempo_crescimento_min = TEMPOS_CRESCIMENTO.get(nome, 0)
                        plantado_em = ms_to_datetime_local(readyAt - tempo_crescimento_min * 60 * 1000)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        uid = nome
                        lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "Fire pits"))
                        fire_pits_adicionados.add(nome)
    
    # Processar Kitchen
            kitchen_pits = buildings.get('Kitchen', [])
            kitchen_pits_adicionado = set()
            for kitchen_info in kitchen_pits:
                kitchen_data = kitchen_info.get('crafting', [])
                if isinstance(kitchen_data, list) and len(kitchen_data) > 0:
                    item = kitchen_data[0]
                    nome = item.get("name")
                    readyAt = item.get("readyAt")

                    if nome and readyAt and nome not in kitchen_pits_adicionado:
                        tempo_crescimento_min = TEMPOS_CRESCIMENTO.get(nome, 0)
                        plantado_em = ms_to_datetime_local(readyAt - tempo_crescimento_min * 60 * 1000)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        uid = nome
                        lista_itens.append((uid, nome, plantado_em, pronto_em, tempo_faltando, 0, "Kitchen pits"))
                        kitchen_pits_adicionado.add(nome)
    
    
    # Ordena pelo tempo restante
    lista_itens.sort(key=lambda x: x[4])
    return lista_itens

# 🔹 Loop principal
while True:
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Salva JSON completo localment
            with open("farm_state.json", "w") as f:
                json.dump(data, f, indent=4)

            state = data.get("visitedFarmState", {})
            lista_itens = process_items(state)

            print("\n===> ITENS ATIVOS:\n")

            ids_prontos_atuais = {uid for uid, _, _, _, tempo, _, _ in lista_itens if tempo <= 0}
            notificadas &= ids_prontos_atuais
            save_notified(notificadas)

            exibidos = set()

            for uid, nome, plantado_em, pronto_em, tempo_faltando, produced, categoria in lista_itens:
                if uid in exibidos:
                    continue
                exibidos.add(uid)

                if categoria == "HONEY":
                    # exibe sempre a colmeia em %
                    porcentagem = min(produced, 100)
                    status = f"{porcentagem:.1f}% cheio"
                    cor = Fore.YELLOW if porcentagem < 100 else Fore.GREEN

                    # envia notificação somente quando 100%
                    if porcentagem >= 100 and uid not in notificadas:
                        send_telegram_notification_sync(f"{nome} está cheio! 🍯")
                        notificadas.add(uid)
                        save_notified(notificadas)

                else:
                    if tempo_faltando > 0:
                        horas = int(tempo_faltando // 3600)
                        minutos = int((tempo_faltando % 3600) // 60)
                        status = f"{horas}h {minutos}min restantes"
                        cor = Fore.YELLOW
                    else:
                        status = "🌱 Pronto para colher!"
                        cor = Fore.GREEN
                        if uid not in notificadas:
                            send_telegram_notification_sync(f"{nome} ({categoria}) está pronto para ser colhido! 🌱")
                            notificadas.add(uid)
                            save_notified(notificadas)

                print(f"{cor}{nome} ({categoria})")
                print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Status: {status}\n")

        else:
            print(f"Falha ao acessar a API. Status code: {response.status_code}")

        time.sleep(15.7)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(15.7)
