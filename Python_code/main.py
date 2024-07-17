from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio


def read_config(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            name, value = line.strip().split('=')
            config[name] = value
    return config   


# reading data from a file
config = read_config('config.txt')
api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']


async def create_telegram_session():
    try:
        client = TelegramClient(phone_number, api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            try:
                await client.sign_in(
                    phone_number, input("Enter the telegram code: ")
                )
            except SessionPasswordNeededError:
                pw = input('Two-step verification is enabled. Enter your password ')
                await client.sign_in(password=pw)
            print('The session has been created')
        else:
            print(f'A session has already been created for this number ({phone_number})')
    except Exception as e:
        print('An error occurred while creating the session:', e)


asyncio.run(create_telegram_session())
input('Press Enter to finish... ')

