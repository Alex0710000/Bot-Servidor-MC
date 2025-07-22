import discord
import os
import requests
import json

# --- INFORMAÇÕES QUE VOCÊ PRECISA MUDAR ---
GITHUB_USERNAME = "Alequixxx"
CODESPACE_NAME = "ominous-doodle-r4x9v59grqv7c5x5x"  # Ex: humble-doodle-123456
# -----------------------------------------

# Pega os tokens dos Segredos do Replit
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

# Configura o bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)


# Função para iniciar o Codespace via API do GitHub
def start_codespace():
    url = f"https://api.github.com/user/codespaces/{CODESPACE_NAME}/start"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return f"✅ Comando para iniciar o Codespace `{CODESPACE_NAME}` enviado com sucesso! Aguarde alguns minutos para o servidor ficar online."
        else:
            error_info = response.json()
            message = error_info.get('message', 'Erro desconhecido.')
            return f"❌ Falha ao iniciar o Codespace. Código: {response.status_code}. Mensagem: `{message}`"
    except Exception as e:
        return f"❌ Ocorreu um erro de conexão: {e}"


# Comando de barra /ligar
@bot.slash_command(name="ligar_servidor",
                   description="Liga o servidor de Minecraft no Codespace.")
async def ligar(ctx):
    await ctx.respond(
        "🚀 Recebi o comando! Tentando iniciar o servidor no GitHub... Isso pode levar um momento."
    )
    status_message = start_codespace()
    await ctx.send(status_message)


# Evento para confirmar que o bot está online
@bot.event
async def on_ready():
    print(f"{bot.user} está online e pronto!")


# --- CÓDIGO PARA MANTER O BOT ONLINE 24/7 ---
from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Bot esta vivo!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Inicia o servidor web em segundo plano
keep_alive()
# -------------------------------------------

# Roda o bot
bot.run(DISCORD_TOKEN)
