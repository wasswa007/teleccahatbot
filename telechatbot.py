import openai
import logging
from telethon import TelegramClient, events

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize OpenAI API key and Telegram client
OPENAI_API_KEY = ""  # Replace with your OpenAI API key
API_ID = ''  # Replace with your Telegram API ID
API_HASH = ''  # Replace with your Telegram API Hash
SESSION_NAME = 'joker'  # Choose a name for your session

openai.api_key = OPENAI_API_KEY

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def get_gpt_response(message_text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_text}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error getting GPT response: {e}")
        return "Sorry, I don't have the ability to answer your question now!"

@client.on(events.NewMessage)
async def handle_message(event):
    if event.is_private:  # Only respond to private messages
        message = event.message.message
        response = await get_gpt_response(message)
        await event.reply(response)
    elif event.is_group or event.is_channel:
        if event.message.message.startswith('//'):
            query = event.message.message[2:]
            response = await get_gpt_response(query)
            await event.reply(response)

def main():
    client.start()
    print("Client is running...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
