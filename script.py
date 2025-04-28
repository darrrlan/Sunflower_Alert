import requests
import datetime
import pytz
import json
import time
import os
from pushbullet import Pushbullet

# API da sua fazenda
url = "https://api.sunflower-land.com/visit/3349809990567285"

# Tempo de crescimento para cada planta (em minutos ou segundos)
tempos_crescimento_minutos = {
    "Sunflower": 1, # 1 min
    "Potato": 5, #5min
    "Pumpkin": 30,  # 30 min
    "Apple": 12*60,  # 12hr
    "Carrot" : 60, #1 hr
    "Cabbage" : 2*60,#2hr
    "Soybean": 3*60, # 3hrs
    "Beetroot":4*60, #4hrs
    "Cauliflower": 8*60, #8hrs
    "Parsnip": 12*60, #12hrs
    "Eggplant": 16*60, #16hr
    "Corn": 20*60, #
    "Radish": 24*60, #24hrs
    "Honey": 24 * 60,  # 24h para o mel
    "Wheat": 24 * 60,  # 24hr
    "Kale": 36*60, #36hrs
}

# Fuso horário Brasil
fuso_brasil = pytz.timezone('America/Sao_Paulo')

# Função para converter com fuso extra
def ms_to_datetime_local(ms):
    dt = datetime.datetime.fromtimestamp(ms / 1000)
    return dt

# Função para enviar notificação pelo Pushbullet
def send_push_notification(title, message):
    pb = Pushbullet("o.uxbBCN8ez4NQMqOfk6RtTT2baO9fOzcS")  # Substitua pela sua API key do Pushbullet
    push = pb.push_note(title, message)

# Armazenar plantas já notificadas
notificadas = set()

# Armazenar plantas já processadas para evitar duplicação
processadas = set()

# Função para determinar o emoji com base no nome da planta ou fruta
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
    }
    return emojis.get(nome, "🌱")  # Emoji padrão se não houver correspondência


while True:
    try:
        # Buscar dados
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            with open('dados_fazenda.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            crops = data.get('state', {}).get('crops', {})
            fruitPatches = data.get('state', {}).get('fruitPatches', {})
            honey = data.get('state', {}).get('beehives', {})


            if not crops and not fruitPatches:
                print("Nenhuma cultura ou fruta encontrada.")
            else:
                print("\n===> PLANTADOS E FRUTAS:\n")

                # Agora, pegar o horário atual no Brasil
                agora = datetime.datetime.now(fuso_brasil)

                # Processando as culturas (crops)
                for crop_id, crop_info in crops.items():
                    crop_data = crop_info.get('crop', {})
                    nome = crop_data.get('name')
                    planted_at = crop_data.get('plantedAt')

                    if nome and planted_at and nome not in processadas:
                        # Marca a planta como processada
                        processadas.add(nome)

                        # E converte o plantado para o timezone do Brasil
                        plantado_em = ms_to_datetime_local(planted_at)

                        # Converte para o timezone do Brasil
                        plantado_em = fuso_brasil.localize(plantado_em)

                        tempo_crescimento = tempos_crescimento_minutos.get(nome)

                        if tempo_crescimento:
                            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                            tempo_faltando = pronto_em - agora

                            horas_faltando = int(tempo_faltando.total_seconds() // 3600)
                            minutos_faltando = int((tempo_faltando.total_seconds() % 3600) // 60)

                            if tempo_faltando.total_seconds() > 0:
                                status = f"{horas_faltando}h {minutos_faltando}min restantes"
                            else:
                                status = "🌟 Pronto para colher!"
                                if nome not in notificadas:
                                    # Envia notificação quando a planta estiver pronta para colher
                                    send_push_notification(f"{get_emoji_for_plant(nome)} {nome} Pronto para Colher!", f"A planta {nome} está pronta para ser colhida!")
                                    notificadas.add(nome)  # Marcar a planta como notificada

                            emoji = get_emoji_for_plant(nome)
                            print(f"{emoji} {nome}")
                            print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                            print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                            print(f"   - Status: {status}\n")
                        else:
                            emoji = get_emoji_for_plant(nome)
                            print(f"{emoji} {nome}")
                            print(f"   - Não sei o tempo de crescimento dessa planta ainda.\n")

                # Processando os patches de frutas (fruitPatches)
                for patch_id, patch_info in fruitPatches.items():
                    fruit_data = patch_info.get('fruit', {})
                    nome = fruit_data.get('name')
                    harvestedAt = fruit_data.get('harvestedAt')

                    if nome and harvestedAt and nome not in processadas:
                        # Marca a fruta como processada
                        processadas.add(nome)

                        # E converte o plantado para o timezone do Brasil
                        plantado_em = ms_to_datetime_local(harvestedAt)

                        # Converte para o timezone do Brasil
                        plantado_em = fuso_brasil.localize(plantado_em)

                        tempo_crescimento = tempos_crescimento_minutos.get(nome)

                        if tempo_crescimento:
                            pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                            tempo_faltando = pronto_em - agora

                            horas_faltando = int(tempo_faltando.total_seconds() // 3600)
                            minutos_faltando = int((tempo_faltando.total_seconds() % 3600) // 60)

                            if tempo_faltando.total_seconds() > 0:
                                status = f"{horas_faltando}h {minutos_faltando}min restantes"
                            else:
                                status = "🌟 Pronto para colher!"
                                if nome not in notificadas:
                                    # Envia notificação quando a fruta estiver pronta para colher
                                    send_push_notification(f"{get_emoji_for_plant(nome)} {nome} Pronto para Colher!", f"A fruta {nome} está pronta para ser colhida!")
                                    notificadas.add(nome)  # Marcar a fruta como notificada

                            emoji = get_emoji_for_plant(nome)
                            print(f"{emoji} {nome}")
                            print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                            print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                            print(f"   - Status: {status}\n")
                        else:
                            emoji = get_emoji_for_plant(nome)
                            print(f"{emoji} {nome}")
                            print(f"   - Não sei o tempo de crescimento dessa fruta ainda.\n")
                        
                # Processando as colmeias (honey)
                if honey:
                    for beehive_id, beehive_info in honey.items():
                        honey_data = beehive_info.get('honey', {})
                        nome = f"Colmeia {beehive_id}"  # Usando o ID da colmeia como nome
                        planted_at = honey_data.get('updatedAt')  # Ajustando para o timestamp correto

                        if nome and planted_at and nome not in processadas:
                            # Marca a colmeia como processada
                            processadas.add(nome)

                            # Converte o plantado para o timezone do Brasil
                            plantado_em = ms_to_datetime_local(planted_at)

                            # Converte para o timezone do Brasil
                            plantado_em = fuso_brasil.localize(plantado_em)

                            tempo_crescimento = tempos_crescimento_minutos.get("Honey")  # Usando o tempo de crescimento do mel

                            if tempo_crescimento:
                                pronto_em = plantado_em + datetime.timedelta(minutes=tempo_crescimento)
                                tempo_faltando = pronto_em - agora

                                horas_faltando = int(tempo_faltando.total_seconds() // 3600)
                                minutos_faltando = int((tempo_faltando.total_seconds() % 3600) // 60)

                                if tempo_faltando.total_seconds() > 0:
                                    status = f"{horas_faltando}h {minutos_faltando}min restantes"
                                else:
                                    status = "🌟 Pronto para colher!"
                                    if nome not in notificadas:
                                        # Envia notificação quando a colmeia estiver pronta para colher
                                        send_push_notification(f"{get_emoji_for_plant(nome)} Honey Pronto para Colher!", f"O Honey está pronta para ser colhida!")
                                        notificadas.add(nome)  # Marcar a colmeia como notificada

                                emoji = get_emoji_for_plant("Honey")
                                print(f"{emoji} Honey")
                                print(f"   - Plantado em: {plantado_em.strftime('%d/%m/%Y %H:%M:%S')}")
                                print(f"   - Ficará pronto em: {pronto_em.strftime('%d/%m/%Y %H:%M:%S')}")
                                print(f"   - Status: {status}\n")
                            else:
                                emoji = get_emoji_for_plant("Honey")
                                print(f"{emoji} Honey")
                                print(f"   - Não sei o tempo de crescimento dessa colmeia ainda.\n")
                else:
                    print("Nenhuma colmeia encontrada.")
                # Limpar as plantas processadas depois de notificar
                processadas.clear()

        else:
            print(f"Falha ao acessar a API. Status code: {response.status_code}")

        # Aguardar 10 segundos antes de nova requisição em caso de falha
        time.sleep(10)
        os.system('cls')
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        time.sleep(10)  # Continuar tentando após 10 segundos mesmo em caso de erro
