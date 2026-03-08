import discord
from discord.ext import commands
import os
import json
import time
import asyncio
from colorama import init, Fore, Style
import random
import logging
logger = logging.getLogger(__name__)
init(autoreset=True)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('raider.log', encoding='utf-8')])
discord_logger = logging.getLogger('discord.webhook.async_')
discord_logger.setLevel(logging.ERROR)
discord_logger.addHandler(logging.FileHandler('raider.log', encoding='utf-8'))
logger.critical("Startup...")
class CustomLoggingHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        if record.levelno == logging.WARNING:
            clear()
            logo()
            status()
handler = CustomLoggingHandler()
logger.addHandler(handler)
def status():
    print(Fore.GREEN + "    Status: Running    ")
    logger.info("Status Display...")
def logo():
    message = [
                                        __     __  __      __  ________ '''
                                       /  |   /  |/  \    /  |/        |
                                       $$ |   $$ |$$  \  /$$/ $$$$$$$$/ 
                                       $$ |   $$ | $$  \/$$/      /$$/  
                                       $$  \ /$$/   $$  $$/      /$$/   
                                        $$  /$$/     $$$$/      /$$/    
                                        $$ $$/       $$ |     /$$/____ 
                                         $$$/        $$ |    /$$      |
                                          $/         $$/     $$$$$$$$/ 
                                                                      by 0xvyz '''
    ]
    logger.info("Logo Display...")
    colors = [
        Fore.BLUE, Fore.BLUE + Style.BRIGHT, Fore.CYAN, 
        Fore.CYAN + Style.BRIGHT, Fore.LIGHTCYAN_EX, 
        Fore.LIGHTCYAN_EX + Style.BRIGHT
    ]
    for i, line in enumerate(message):
        print(colors[i % len(colors)] + line + Style.RESET_ALL)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info("Console cleanup...")
clear()
filename = 'raid_template.json'
def load_template(filename):
    with open(filename, 'r') as file:
        return json.load(file)
def validate_inputs(message_amount):
    if message_amount not in [1, 2, 3, 4, 5]:
        raise ValueError("MESSAGE_AMOUNT must be 1, 2, 3, 4, or 5.")
TOKEN = None
MESSAGE_AMOUNT = None
final_message = None
def get_user_input():
    logger.info("Requesting user input...")
    global TOKEN, MESSAGE_AMOUNT, final_message
    while True:
        TOKEN = input("    Input your bot's token: ")
        logger.info("Requesting token...")
        try:
            MESSAGE_AMOUNT = int(input("    Input the amount of messages to send per command (1-5): "))
            logger.info("Requesting message amount...")
            validate_inputs(MESSAGE_AMOUNT)
            break
        except ValueError as ve:
            print(ve)
    print("    Input your raid messages (separate messages with a semicolon ';' and press Enter when done):")
    logger.info("Requesting raid messages...")
    user_input = input()
    RAID_MESSAGE = [msg.strip() for msg in user_input.split(';')]
    final_message = RAID_MESSAGE
    print("    New template saved successfully.")
    logger.info("Template saved...")

if os.path.exists(filename):
    logger.info("Request template usage...")
    use_last_template = input(Fore.CYAN + "    A previous template exists. Do you want to use the last template? (yes/no): ")
    if use_last_template.lower() == 'yes':
        template_data = load_template(filename)
        TOKEN = template_data['TOKEN']
        MESSAGE_AMOUNT = int(template_data['MESSAGE_AMOUNT'])
        final_message = template_data['final_message']
        logger.info("Last template chosen...")
        print("    Loaded last template:")
        print(template_data)
    else:
        logger.info("Requesting new template...")
        get_user_input()
else:
    get_user_input()
data_to_save = {
    'TOKEN': TOKEN,
    'MESSAGE_AMOUNT': MESSAGE_AMOUNT,
    'final_message': final_message,
}
with open(filename, 'w') as file:
    logger.debug("Template saved as file...")
    json.dump(data_to_save, file, indent=4)
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
logger.debug("Main script startup...")
time.sleep(1)
clear()
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logger.info("Synced command...")
        clear()
        logo()
        status()
    except Exception:
        logger.error("Sync failed...")
        pass
clear()
logo()
print(Fore.GREEN + "Ready to use!")
@bot.tree.command(
    name="spamraid",
    description="This sends out the raid message!"
)
async def send(interaction: discord.Interaction):
    try:
        logger.info("Check channel permissions...")
        if isinstance(interaction.channel, discord.DMChannel) or (
            isinstance(interaction.channel, discord.TextChannel) and
            interaction.channel.permissions_for(interaction.guild.me).send_messages):
            await interaction.response.send_message("Sending message...", ephemeral=True)
            logger.info("Sending messages...")
            for _ in range(MESSAGE_AMOUNT):
                message_to_send = random.choice(final_message)
                await interaction.followup.send(message_to_send)
                await asyncio.sleep(0.02)
        else:
            await interaction.response.send_message(
                "I don't have permission to send messages in this channel!", 
                ephemeral=True)
    except Exception:
        logger.error("Error occurred while sending messages.")
bot.run(TOKEN)
