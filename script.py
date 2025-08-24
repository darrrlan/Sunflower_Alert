import requests
import datetime
import pytz
import json
import time
from operator import itemgetter
from colorama import init, Fore
import telegram
import asyncio
import config_telegram

init(autoreset=True)

url = "https://api.sunflower-land.com/visit/1444484773494499"

tempos_crescimento_minutos = {
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
    "Onion"  : 20 * 60,
    "Blue Lotus" : 5*24*60,
}

fuso_brasil = pytz.timezone('America/Sao_Paulo')


def ms_to_datetime_local(ms):
    """Converte timestamp em milissegundos para datetime local com fuso horário correto"""
    dt_utc = datetime.datetime.fromtimestamp(ms / 1000, tz=pytz.UTC)
    dt_local = dt_utc.astimezone(fuso_brasil)
    return dt_local



def send_telegram_notification_sync(message):
    """Função síncrona para enviar mensagem via Telegram usando asyncio.run internamente"""
    async def send():
        bot = telegram.Bot(token=config_telegram.TELEGRAM_API_KEY)
        chat_id = config_telegram.TELEGRAM_CHAT_ID
        await bot.send_message(chat_id=chat_id, text=message)

    try:
        asyncio.run(send())
    except Exception as e:
        print(f"Erro ao enviar notificação Telegram: {e}")


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

# send_telegram_notification_sync("Bot iniciado e funcionando!")

while True:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            with open('dados_fazenda.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            state = data.get('visitedFarmState', {})
            crops = state.get('crops', {})
            fruitPatches = state.get('fruitPatches', {})
            honey = state.get('beehives', {})
            flowers = state.get('flowers', {}).get('flowerBeds', {}) if 'flowers' in state else {}
            buildings = state.get('buildings', {})
            compost_bins = buildings.get('Compost Bin', [])
            turbo_composters = buildings.get('Turbo Composter', [])
            fire_pits = buildings.get('Fire Pit', [])
            kitchen_pits = buildings.get('Kitchen', [])

            lista_itens = []
            agora = datetime.datetime.now(fuso_brasil)
            processados = set()

            # Processar plantações
            for crop_info in crops.values():
                crop_data = crop_info.get('crop', {})
                nome = crop_data.get('name')
                planted_at = crop_data.get('plantedAt')

                if nome and planted_at and nome not in processados:
                    processados.add(nome)
                    plantado_em = ms_to_datetime_local(planted_at)
                    tempo_crescimento = tempos_crescimento_minutos.get(nome, 0)

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
                        timestamp_base = harvested_at if harvested_at and harvested_at != 0 else planted_at
                        if timestamp_base:
                            plantado_em = ms_to_datetime_local(timestamp_base)
                            tempo_crescimento = tempos_crescimento_minutos.get(nome, 0)

                            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                            tempo_faltando = (pronto_em - agora).total_seconds()
                            lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar colmeias
            for beehive_id, beehive_info in honey.items():
                honey_data = beehive_info.get('honey', {})
                nome = f"Colmeia {beehive_id}"
                updated_at = honey_data.get('updatedAt')  # ms
                produced_ms = honey_data.get('produced', 0)  # ms

                if updated_at and nome not in processados:
                    processados.add(nome)

                    started_at = updated_at - produced_ms
                    plantado_em = ms_to_datetime_local(started_at)
                    tempo_crescimento = tempos_crescimento_minutos.get("Honey", 24 * 60)
                    pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                    tempo_faltando = (pronto_em - agora).total_seconds()

                    lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar flores
            if isinstance(flowers, dict):
                for flower_info in flowers.values():
                    flower_data = flower_info.get('flower', {})
                    nome = flower_data.get('name')
                    planted_at = flower_data.get('plantedAt')

                    if nome and planted_at and nome not in processados:
                        processados.add(nome)
                        plantado_em = ms_to_datetime_local(planted_at)
                        tempo_crescimento = tempos_crescimento_minutos.get(nome, 0)

                        pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                        tempo_faltando = (pronto_em - agora).total_seconds()
                        lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar Compost Bin e Turbo Composter (mesmo tratamento)
            for compost_list in [compost_bins, turbo_composters]:
                for compost_info in compost_list:
                    compost_data = compost_info.get('producing', {})
                    items = compost_data.get('items', {})
                    nome = next(iter(items), None)

                    startedAt = compost_data.get('startedAt')
                    readyAt = compost_data.get('readyAt')

                    if nome and startedAt and readyAt and nome not in processados:
                        processados.add(nome)
                        plantado_em = ms_to_datetime_local(startedAt)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            # Processar Fire Pit
            for fire_info in fire_pits:
                fire_data = fire_info.get('crafting', [])
                if isinstance(fire_data, list) and len(fire_data) > 0:
                    item = fire_data[0]
                    nome = item.get("name")
                    readyAt = item.get("readyAt")

                    if nome and readyAt and nome not in processados:
                        processados.add(nome)
                        tempo_crescimento_min = tempos_crescimento_minutos.get(nome, 0)
                        plantado_em = ms_to_datetime_local(readyAt - tempo_crescimento_min * 60 * 1000)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))




            # Processar Kitchen
            for kitchen_info in kitchen_pits:
                kitchen_data = kitchen_info.get('crafting', [])
                if isinstance(kitchen_data, list) and len(kitchen_data) > 0:
                    item = kitchen_data[0]
                    nome = item.get("name")
                    readyAt = item.get("readyAt")

                    if nome and readyAt and nome not in processados:
                        processados.add(nome)
                        tempo_crescimento_min = tempos_crescimento_minutos.get(nome, 0)
                        plantado_em = ms_to_datetime_local(readyAt - tempo_crescimento_min * 60 * 1000)
                        pronto_em = ms_to_datetime_local(readyAt)

                        tempo_faltando = (pronto_em - agora).total_seconds()
                        lista_itens.append((nome, plantado_em, pronto_em, tempo_faltando))

            lista_itens.sort(key=itemgetter(3))

            print("\n===> PLANTADOS E FRUTAS:\n")

            # Limpeza das notificações antigas que não estão mais na lista de prontos
            nomes_prontos_atuais = {nome for nome, _, _, tempo_faltando in lista_itens if tempo_faltando <= 0}
            notificadas_para_remover = notificadas - nomes_prontos_atuais

            if notificadas_para_remover:
                for nome in notificadas_para_remover:
                    notificadas.remove(nome)
                save_notified(notificadas)

            for nome, plantado_em, pronto_em, tempo_faltando in lista_itens:
                if tempo_faltando > 0:
                    horas = int(tempo_faltando // 3600)
                    minutos = int((tempo_faltando % 3600) // 60)
                    status = f"{horas}h {minutos}min restantes"
                    cor = Fore.YELLOW
                else:
                    status = "Pronto para colher!"
                    cor = Fore.GREEN

                    if nome not in notificadas:
                        send_telegram_notification_sync(f"{nome} está pronto para ser colhido!")
                        notificadas.add(nome)
                        save_notified(notificadas)

                print(f"{cor}{nome}")
                print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"   - Status: {status}\n")

        else:
            print(f"Falha ao acessar a API. Status code: {response.status_code}")

        time.sleep(15.7)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(15.7)