from typing import Any, Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN', 'None')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
keyword = '!'
games: dict[str, Any] = {}

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('No Intents')
        return

    user_message = user_message.lower()

    if is_private := user_message[0] =='?':
        user_message = user_message[1:]
    
    if user_message[:len(keyword)] != keyword:
        print('Uninvolved')
        return
    
    user_message = user_message[len(keyword):]

    try:
        response: str = get_response(user_message, str(message.author), games)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
        
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()